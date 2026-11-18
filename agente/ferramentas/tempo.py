#!/usr/bin/env python3
"""
tempo.py — a ferramenta meteorológica do agente "Fim de semana".

Uma ferramenta de agente é só isto: um programa pequeno, com UMA tarefa,
que devolve texto que o modelo consegue ler. Esta vai buscar a previsão do
próximo fim de semana para uma cidade e diz se há avisos.

    python3 ferramentas/tempo.py Lisboa
    python3 ferramentas/tempo.py "Vila Real"
    python3 ferramentas/tempo.py Madrid          # fora de Portugal também serve
    python3 ferramentas/tempo.py Porto --json    # para quem prefere chavetas

Fontes (as duas gratuitas, as duas sem chave, as duas melhores a prever o
tempo do que o teu joelho):
  - IPMA (api.ipma.pt)       — cidades portuguesas, com avisos meteorológicos
  - Open-Meteo (open-meteo.com) — o resto do mundo, ou quando o IPMA ainda
                                  não chega ao fim de semana (prevê só 5 dias)

Só usa a biblioteca padrão do Python. Nada de `pip install`: numa palestra
ao vivo, cada dependência é uma oportunidade de humilhação pública.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import unicodedata
import urllib.parse
import urllib.request

TIMEOUT = 10  # segundos. Se o IPMA demorar mais do que isto, está a chover lá dentro.
UA = {"User-Agent": "agente-fim-de-semana/1.0 (demo educativa)"}

IPMA_LOCAIS = "https://api.ipma.pt/open-data/distrits-islands.json"
IPMA_PREVISAO = "https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/{id}.json"
IPMA_TIPOS = "https://api.ipma.pt/open-data/weather-type-classe.json"
IPMA_AVISOS = "https://api.ipma.pt/open-data/forecast/warnings/warnings_www.json"
OM_GEO = "https://geocoding-api.open-meteo.com/v1/search?name={nome}&count=1&language=pt"
OM_PREVISAO = (
    "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
    "&daily=weather_code,temperature_2m_min,temperature_2m_max,"
    "precipitation_probability_max,wind_speed_10m_max"
    "&timezone=auto&forecast_days=16"
)

# Códigos WMO usados pelo Open-Meteo, traduzidos para gente.
WMO = {
    0: "Céu limpo", 1: "Céu pouco nublado", 2: "Céu parcialmente nublado",
    3: "Céu nublado", 45: "Nevoeiro", 48: "Nevoeiro com geada",
    51: "Chuvisco fraco", 53: "Chuvisco", 55: "Chuvisco forte",
    56: "Chuvisco gelado", 57: "Chuvisco gelado forte",
    61: "Chuva fraca", 63: "Chuva", 65: "Chuva forte",
    66: "Chuva gelada", 67: "Chuva gelada forte",
    71: "Neve fraca", 73: "Neve", 75: "Neve forte", 77: "Grãos de neve",
    80: "Aguaceiros fracos", 81: "Aguaceiros", 82: "Aguaceiros fortes",
    85: "Aguaceiros de neve", 86: "Aguaceiros de neve fortes",
    95: "Trovoada", 96: "Trovoada com granizo", 99: "Trovoada com granizo forte",
}

# Classes de vento do IPMA (1 a 4) em palavras.
VENTO_IPMA = {1: "fraco", 2: "moderado", 3: "forte", 4: "muito forte"}

NIVEL_AVISO = {"yellow": "AMARELO", "orange": "LARANJA", "red": "VERMELHO"}


def obter(url: str):
    """Pede um URL e devolve o JSON. Falha alto e em português."""
    pedido = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(pedido, timeout=TIMEOUT) as resposta:
        return json.loads(resposta.read().decode("utf-8"))


def normalizar(texto: str) -> str:
    """'Évora ' -> 'evora'. Porque ninguém escreve acentos no chat."""
    sem_acentos = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return " ".join(sem_acentos.lower().replace("-", " ").split())


def proximo_fim_de_semana(hoje: dt.date) -> tuple[dt.date, dt.date]:
    """Sábado e domingo. Se hoje já é sábado ou domingo, é este."""
    if hoje.weekday() == 6:  # domingo: o fim de semana é... hoje e ontem. Fica só hoje.
        return hoje - dt.timedelta(days=1), hoje
    sabado = hoje + dt.timedelta(days=(5 - hoje.weekday()) % 7)
    return sabado, sabado + dt.timedelta(days=1)


def ipma(cidade: str, dias: list[dt.date]):
    """Tenta o IPMA. Devolve None se a cidade não for portuguesa ou se o
    fim de semana ainda estiver para lá dos 5 dias de previsão."""
    locais = obter(IPMA_LOCAIS)["data"]
    alvo = normalizar(cidade)
    local = next((l for l in locais if normalizar(l["local"]) == alvo), None)
    if local is None:
        return None

    previsao = obter(IPMA_PREVISAO.format(id=local["globalIdLocal"]))["data"]
    por_data = {p["forecastDate"]: p for p in previsao}
    if not all(d.isoformat() in por_data for d in dias):
        return None  # o IPMA ainda não vê tão longe; o Open-Meteo vê

    tipos = {t["idWeatherType"]: t["descWeatherTypePT"] for t in obter(IPMA_TIPOS)["data"]}
    resultado = []
    for d in dias:
        p = por_data[d.isoformat()]
        resultado.append({
            "data": d.isoformat(),
            "estado": tipos.get(p["idWeatherType"], "Sem informação"),
            "t_min": round(float(p["tMin"])),
            "t_max": round(float(p["tMax"])),
            "prob_chuva": round(float(p["precipitaProb"])),
            "vento": VENTO_IPMA.get(p.get("classWindSpeed"), "sem informação"),
        })

    avisos = []
    try:
        for a in obter(IPMA_AVISOS):
            if a["idAreaAviso"] != local["idAreaAviso"] or a["awarenessLevelID"] not in NIVEL_AVISO:
                continue
            inicio, fim = a["startTime"][:10], a["endTime"][:10]
            if any(inicio <= d.isoformat() <= fim for d in dias):
                avisos.append(f"{NIVEL_AVISO[a['awarenessLevelID']]} — {a['awarenessTypeName']}"
                              f" ({a['startTime'][:16].replace('T', ' ')} a {a['endTime'][:16].replace('T', ' ')})"
                              + (f": {a['text']}" if a.get("text") else ""))
    except Exception:  # sem avisos não é motivo para estragar o fim de semana
        avisos = ["(não foi possível consultar os avisos do IPMA)"]

    return {"cidade": local["local"], "fonte": "IPMA (api.ipma.pt)", "dias": resultado, "avisos": avisos}


def open_meteo(cidade: str, dias: list[dt.date]):
    """Plano B mundial: geocodifica a cidade e pede a previsão."""
    geo = obter(OM_GEO.format(nome=urllib.parse.quote(cidade))).get("results") or []
    if not geo:
        return None
    g = geo[0]
    dados = obter(OM_PREVISAO.format(lat=g["latitude"], lon=g["longitude"]))["daily"]
    resultado = []
    for d in dias:
        if d.isoformat() not in dados["time"]:
            continue
        i = dados["time"].index(d.isoformat())
        resultado.append({
            "data": d.isoformat(),
            "estado": WMO.get(dados["weather_code"][i], "Sem informação"),
            "t_min": round(dados["temperature_2m_min"][i]),
            "t_max": round(dados["temperature_2m_max"][i]),
            "prob_chuva": dados["precipitation_probability_max"][i],
            "vento": f"até {round(dados['wind_speed_10m_max'][i])} km/h",
        })
    nome = ", ".join(x for x in (g.get("name"), g.get("country")) if x)
    return {
        "cidade": nome,
        "fonte": "Open-Meteo (open-meteo.com)",
        "dias": resultado,
        "avisos": ["(o Open-Meteo não publica avisos oficiais — confirma no serviço meteorológico local)"],
    }


DIAS_PT = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]


def como_texto(r: dict) -> str:
    linhas = [f"Previsão para {r['cidade']} — fonte: {r['fonte']}", ""]
    for d in r["dias"]:
        data = dt.date.fromisoformat(d["data"])
        chuva = "?" if d["prob_chuva"] is None else f"{d['prob_chuva']}%"
        linhas.append(
            f"  {DIAS_PT[data.weekday()].capitalize():8} {data:%d/%m}: {d['estado']}, "
            f"{d['t_min']}–{d['t_max']} °C, chuva {chuva}, vento {d['vento']}"
        )
    linhas.append("")
    linhas.append("Avisos meteorológicos: " + ("; ".join(r["avisos"]) if r["avisos"] else "nenhum (verde em todo o lado)"))
    return "\n".join(linhas)


def main() -> int:
    ap = argparse.ArgumentParser(description="Previsão do próximo fim de semana para uma cidade.")
    ap.add_argument("cidade", nargs="+", help='nome da cidade, ex.: Lisboa, "Vila Real", Madrid')
    ap.add_argument("--json", action="store_true", help="devolve JSON em vez de texto")
    ap.add_argument("--hoje", help="finge que hoje é AAAA-MM-DD (para ensaios)")
    args = ap.parse_args()

    cidade = " ".join(args.cidade)
    hoje = dt.date.fromisoformat(args.hoje) if args.hoje else dt.date.today()
    dias = list(proximo_fim_de_semana(hoje))
    if dias[0] < hoje:  # é domingo: sábado já passou
        dias = dias[1:]

    try:
        r = ipma(cidade, dias) or open_meteo(cidade, dias)
    except Exception as e:
        print(f"ERRO: não consegui falar com o serviço meteorológico ({e}). "
              "Sem dados, não há previsão — não inventes uma.", file=sys.stderr)
        return 2
    if r is None:
        print(f"ERRO: não encontrei a cidade '{cidade}'. Experimenta outro nome "
              "(ex.: 'Porto' em vez de 'Invicta').", file=sys.stderr)
        return 1
    if not r["dias"]:
        print("ERRO: ainda não há previsão para esse fim de semana.", file=sys.stderr)
        return 1

    print(json.dumps(r, ensure_ascii=False, indent=2) if args.json else como_texto(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
