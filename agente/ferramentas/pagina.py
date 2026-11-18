#!/usr/bin/env python3
"""
pagina.py — transforma o plano do agente (JSON) numa página HTML bonita.

Porquê uma ferramenta em vez de pedir ao modelo que escreva o HTML todo?
Três razões, por ordem de importância numa palestra ao vivo:

  1. Rapidez: o modelo escreve 60 linhas de JSON em vez de 400 de HTML.
  2. Consistência: a página sai sempre igual, com o mesmo cuidado.
  3. Divisão de trabalho: o modelo DECIDE (o que fazer, quando, porquê);
     o código FORMATA. Cada um faz aquilo em que é bom. Como num casamento
     que funciona.

    python3 ferramentas/pagina.py saida/plano-lisboa.json
    python3 ferramentas/pagina.py saida/plano-lisboa.json --tema nova
    python3 ferramentas/pagina.py --exemplo        # mostra o formato esperado
    python3 ferramentas/pagina.py --indice saida   # página-resumo de vários planos

Escreve o .html (e um .ics para o calendário) ao lado do .json e diz onde ficaram.
O .ics é o "um agente FAZ" mais palpável que há: abre-se no telemóvel e o
fim de semana aparece no calendário, sesta incluída.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import pathlib
import re
import sys

TEMAS = {
    # nome: (fundo, texto, destaque, destaque2, cartão, linha)
    "sol":   ("#FFF8EE", "#2A1E14", "#E8572A", "#F2B134", "#FFFFFF", "#F0E3CF"),
    "nova":  ("#F4F7FF", "#0B0B0B", "#3676FE", "#0DDF70", "#FFFFFF", "#DCE5FA"),
    "noite": ("#14161C", "#ECEEF3", "#8AB4FF", "#7CE0A3", "#1E2129", "#2C303A"),
}

ICONES = [  # (palavra no estado do tempo, ícone)
    ("trovoada", "⛈️"), ("neve", "🌨️"), ("aguaceiro", "🌦️"), ("chuvisco", "🌦️"),
    ("chuva", "🌧️"), ("nevoeiro", "🌫️"), ("neblina", "🌫️"), ("limpo", "☀️"),
    ("pouco nublado", "🌤️"), ("parcialmente", "⛅"), ("nublado", "☁️"),
]

EXEMPLO = {
    "cidade": "Lisboa",
    "fim_de_semana": "21 e 22 de novembro",
    "resumo": "Sábado molhado, domingo de sol: museus primeiro, jardins depois.",
    "orcamento": 50,
    "avisos": [],
    "dias": [
        {
            "dia": "Sábado 21/11",
            "data": "2026-11-21",
            "tempo": {"estado": "Chuva/aguaceiros", "t_min": 14, "t_max": 19, "prob_chuva": 100},
            "atividades": [
                {
                    "hora": "10:00",
                    "titulo": "Pavilhão do Conhecimento",
                    "onde": "Parque das Nações",
                    "porque": "Interior, interativo, e a criança gasta energia sem se molhar.",
                    "custo": 12,
                    "interior": True,
                    "fonte": "https://www.pavconhecimento.pt",
                    "confirmar": "horário e preço no site",
                    "duracao_min": 150,
                }
            ],
        }
    ],
    "custos_extra": [{"o_que": "transportes (2 dias)", "custo": 8}],
    "levar": ["guarda-chuva", "casaco leve para domingo"],
    "notas": ["Eventos sem fonte encontrada não entram no plano."],
}


def icone(estado: str) -> str:
    e = estado.lower()
    if ("chuva" in e or "aguaceiro" in e) and "fraco" not in e and "trovoada" not in e:
        return "🌧️"  # chuva a sério: nada de sol a espreitar no ícone
    return next((i for chave, i in ICONES if chave in e), "🌡️")


def esc(x) -> str:
    return html.escape(str(x)) if x is not None else ""


def validar(p: dict) -> list[str]:
    """Erros que impedem a página. O agente lê isto e corrige — é o ciclo
    pensar → agir → OBSERVAR a funcionar."""
    erros = []
    for campo in ("cidade", "dias"):
        if campo not in p:
            erros.append(f"falta o campo '{campo}'")
    for i, d in enumerate(p.get("dias", [])):
        if "dia" not in d or "atividades" not in d:
            erros.append(f"dias[{i}] precisa de 'dia' e 'atividades'")
        for j, a in enumerate(d.get("atividades", [])):
            for campo in ("hora", "titulo", "porque"):
                if campo not in a:
                    erros.append(f"dias[{i}].atividades[{j}] sem '{campo}'")
    return erros


def data_do_dia(d: dict, hoje: dt.date | None = None) -> dt.date | None:
    """A data de um dia do plano: o campo 'data' (AAAA-MM-DD) ou, se faltar,
    o 'dd/mm' escrito em 'dia'. O ano adivinha-se (é o fim de semana mais
    próximo, não o de 1987)."""
    if d.get("data"):
        try:
            return dt.date.fromisoformat(d["data"])
        except ValueError:
            pass
    m = re.search(r"(\d{1,2})/(\d{1,2})", d.get("dia", ""))
    if not m:
        return None
    hoje = hoje or dt.date.today()
    dia, mes = int(m.group(1)), int(m.group(2))
    try:
        data = dt.date(hoje.year, mes, dia)
    except ValueError:
        return None
    if data < hoje - dt.timedelta(days=60):  # dezembro a planear janeiro
        data = dt.date(hoje.year + 1, mes, dia)
    return data


def _ics_texto(x) -> str:
    """Escapa texto para iCalendar (RFC 5545): \\ ; , e quebras de linha."""
    return (str(x or "").replace("\\", "\\\\").replace(";", "\\;")
            .replace(",", "\\,").replace("\n", "\\n"))


def _ics_dobrar(linha: str) -> str:
    """Linhas de iCalendar têm no máximo 75 octetos; o resto continua na
    linha seguinte, começada por um espaço. Sim, é um formato de 1998."""
    b = linha.encode("utf-8")
    if len(b) <= 75:
        return linha
    partes, atual = [], b""
    for ch in linha:
        c = ch.encode("utf-8")
        if len(atual) + len(c) > (75 if not partes else 74):
            partes.append(atual.decode("utf-8"))
            atual = b""
        atual += c
    partes.append(atual.decode("utf-8"))
    return "\r\n ".join(partes)


def gerar_ics(p: dict) -> str | None:
    """Um evento por atividade. Hora local 'flutuante' (sem fuso), que o
    calendário de cada pessoa interpreta como hora local. Devolve None se
    nenhum dia tiver data."""
    agora = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    eventos = []
    for d in p["dias"]:
        data = data_do_dia(d)
        if not data:
            continue
        acts = d["atividades"]
        for k, a in enumerate(acts):
            m = re.match(r"(\d{1,2})[:h](\d{2})", str(a.get("hora", "")))
            if not m:
                continue
            inicio = dt.datetime.combine(data, dt.time(int(m.group(1)), int(m.group(2))))
            dur = a.get("duracao_min")
            if not dur and k + 1 < len(acts):
                m2 = re.match(r"(\d{1,2})[:h](\d{2})", str(acts[k + 1].get("hora", "")))
                if m2:
                    seguinte = dt.datetime.combine(data, dt.time(int(m2.group(1)), int(m2.group(2))))
                    dur = min(180, max(30, int((seguinte - inicio).total_seconds() // 60)))
            fim = inicio + dt.timedelta(minutes=int(dur or 90))
            descricao = a.get("porque", "")
            if a.get("confirmar"):
                descricao += f"\nConfirmar: {a['confirmar']}"
            if a.get("fonte"):
                descricao += f"\nFonte: {a['fonte']}"
            linhas = [
                "BEGIN:VEVENT",
                f"UID:{data:%Y%m%d}-{m.group(1)}{m.group(2)}-{k}-{hashlib.sha1(a['titulo'].encode()).hexdigest()[:8]}@agente-fim-de-semana",
                f"DTSTAMP:{agora}",
                f"DTSTART:{inicio:%Y%m%dT%H%M%S}",
                f"DTEND:{fim:%Y%m%dT%H%M%S}",
                f"SUMMARY:{_ics_texto(a['titulo'])}",
                f"DESCRIPTION:{_ics_texto(descricao)}",
            ]
            if a.get("onde"):
                linhas.append(f"LOCATION:{_ics_texto(a['onde'])}")
            if a.get("fonte"):
                linhas.append(f"URL:{a['fonte']}")
            linhas.append("END:VEVENT")
            eventos.extend(linhas)
    if not eventos:
        return None
    cal = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//agente-fim-de-semana//PT",
           "CALSCALE:GREGORIAN", f"X-WR-CALNAME:Fim de semana em {_ics_texto(p['cidade'])}",
           *eventos, "END:VCALENDAR"]
    return "\r\n".join(_ics_dobrar(l) for l in cal) + "\r\n"


def construir_indice(planos: list[tuple[str, dict]], tema: str) -> str:
    """Página-resumo para quando o agente planeia várias cidades de uma vez."""
    fundo, texto, dest, dest2, cartao, linha = TEMAS[tema]
    cartoes = []
    for nome_html, p in planos:
        extras = p.get("custos_extra") or []
        total = (sum(float(a.get("custo") or 0) for d in p["dias"] for a in d["atividades"])
                 + sum(float(x.get("custo") or 0) for x in extras))
        tempos = " · ".join(
            f"{icone((d.get('tempo') or {}).get('estado', ''))} {esc(d['dia'].split()[0])}"
            for d in p["dias"])
        cartoes.append(f"""
    <a class="c" href="{esc(nome_html)}">
      <h2>{esc(p['cidade'])}</h2>
      <p class="t">{tempos}</p>
      <p>{esc(p.get('resumo', ''))}</p>
      <p class="e">{total:.0f} € · ver o plano →</p>
    </a>""")
    return f"""<!doctype html>
<html lang="pt"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fins de semana — {len(planos)} cidades</title>
<style>
  body {{ margin:0; background:{fundo}; color:{texto}; font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; }}
  main {{ max-width:1000px; margin:0 auto; padding:40px 16px 64px; }}
  .kicker {{ text-transform:uppercase; letter-spacing:.14em; font-size:12px; font-weight:700; color:{dest}; margin:0; }}
  h1 {{ font-size:clamp(30px,5vw,46px); margin:.2em 0 .6em; letter-spacing:-.02em; }}
  .g {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:18px; }}
  .c {{ display:block; text-decoration:none; color:inherit; background:{cartao}; border:1px solid {linha};
        border-top:6px solid {dest2}; border-radius:16px; padding:20px 22px; }}
  .c:hover {{ border-color:{dest}; }}
  .c h2 {{ margin:0 0 4px; font-size:26px; }}
  .t {{ font-size:15px; opacity:.85; margin:0 0 8px; }}
  .e {{ font-weight:700; color:{dest}; margin:10px 0 0; }}
</style></head><body><main>
  <p class="kicker">Vários agentes, ao mesmo tempo, um por cidade</p>
  <h1>Fins de semana em {len(planos)} cidades</h1>
  <div class="g">{''.join(cartoes)}
  </div>
</main></body></html>
"""


def construir(p: dict, tema: str, ics_nome: str | None = None) -> str:
    fundo, texto, dest, dest2, cartao, linha = TEMAS[tema]
    extras = p.get("custos_extra") or []
    total = (sum(float(a.get("custo") or 0) for d in p["dias"] for a in d["atividades"])
             + sum(float(x.get("custo") or 0) for x in extras))
    orc = p.get("orcamento")
    estoirou = orc is not None and total > float(orc)

    dias_html = []
    for d in p["dias"]:
        t = d.get("tempo") or {}
        tempo_html = ""
        if t:
            tempo_html = (
                f'<div class="tempo"><span class="ic">{icone(t.get("estado", ""))}</span>'
                f'<span>{esc(t.get("estado"))}</span>'
                f'<span class="num">{esc(t.get("t_min"))}–{esc(t.get("t_max"))} °C</span>'
                f'<span class="num">☔ {esc(t.get("prob_chuva"))}%</span></div>'
            )
        acts = []
        for a in d["atividades"]:
            custo = a.get("custo")
            custo_txt = "grátis" if not custo else f"{float(custo):.0f} €".replace(".0 €", " €")
            fonte = a.get("fonte")
            fonte_html = (f'<a href="{esc(fonte)}" target="_blank" rel="noopener">fonte</a>'
                          if fonte else '<span class="semfonte">sem fonte — sugestão geral</span>')
            confirmar = (f'<span class="conf">⚠ confirmar: {esc(a["confirmar"])}</span>'
                         if a.get("confirmar") else "")
            sitio = "🏠 interior" if a.get("interior") else "🌳 exterior"
            acts.append(f"""
      <li class="act">
        <div class="hora">{esc(a['hora'])}</div>
        <div class="corpo">
          <h3>{esc(a['titulo'])}</h3>
          <p class="onde">{esc(a.get('onde', ''))} · {sitio} · <b>{custo_txt}</b></p>
          <p class="porque">{esc(a['porque'])}</p>
          <p class="meta">{fonte_html} {confirmar}</p>
        </div>
      </li>""")
        dias_html.append(f"""
  <section class="dia">
    <header><h2>{esc(d['dia'])}</h2>{tempo_html}</header>
    <ol>{''.join(acts)}
    </ol>
  </section>""")

    avisos = p.get("avisos") or []
    avisos_html = ("".join(f'<p class="aviso">⚠️ {esc(a)}</p>' for a in avisos)) if avisos else ""
    levar = p.get("levar") or []
    notas = p.get("notas") or []
    orc_txt = (f"{total:.0f} € de {float(orc):.0f} €" if orc is not None else f"{total:.0f} €")
    if extras:
        orc_txt += " (inclui " + ", ".join(f"{esc(x.get('o_que', 'extra'))} {float(x.get('custo') or 0):.0f} €" for x in extras) + ")"

    return f"""<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fim de semana em {esc(p['cidade'])}</title>
<style>
  :root {{ --fundo:{fundo}; --texto:{texto}; --dest:{dest}; --dest2:{dest2}; --cartao:{cartao}; --linha:{linha}; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--fundo); color:var(--texto);
         font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; }}
  main {{ max-width:880px; margin:0 auto; padding:40px 16px 64px; }}
  .kicker {{ text-transform:uppercase; letter-spacing:.14em; font-size:12px; font-weight:700; color:var(--dest); margin:0; }}
  h1 {{ font-size:clamp(32px,6vw,52px); line-height:1.05; margin:.2em 0 .3em; letter-spacing:-.02em; }}
  .resumo {{ font-size:20px; margin:0 0 20px; }}
  .barra {{ display:flex; flex-wrap:wrap; gap:8px; margin-bottom:28px; }}
  .pill {{ background:var(--cartao); border:1px solid var(--linha); border-radius:999px; padding:6px 14px; font-size:14px; }}
  .pill.cal {{ background:var(--dest); color:#fff; border-color:var(--dest); text-decoration:none; font-weight:700; }}
  .pill.mau {{ border-color:#C62828; color:#C62828; font-weight:700; }}
  .aviso {{ background:#FFF3C4; color:#5C4400; border-left:5px solid #F2B134; padding:10px 14px; border-radius:6px; }}
  .dia {{ background:var(--cartao); border:1px solid var(--linha); border-radius:18px; padding:22px 24px; margin:0 0 22px; }}
  .dia header {{ display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:10px;
                border-bottom:3px solid var(--dest2); padding-bottom:12px; margin-bottom:6px; }}
  .dia h2 {{ margin:0; font-size:24px; }}
  .tempo {{ display:flex; gap:12px; align-items:center; font-size:15px; }}
  .tempo .ic {{ font-size:28px; }}
  .num {{ font-variant-numeric:tabular-nums; font-weight:600; }}
  ol {{ list-style:none; margin:0; padding:0; }}
  .act {{ display:grid; grid-template-columns:70px 1fr; gap:14px; padding:16px 0; border-bottom:1px dashed var(--linha); }}
  .act:last-child {{ border-bottom:0; }}
  .hora {{ font-weight:800; font-size:18px; color:var(--dest); font-variant-numeric:tabular-nums; }}
  .act h3 {{ margin:0 0 2px; font-size:19px; }}
  .act p {{ margin:2px 0; }}
  .onde {{ font-size:14px; opacity:.8; }}
  .meta {{ font-size:13px; }}
  .meta a {{ color:var(--dest); font-weight:600; }}
  .semfonte {{ opacity:.7; font-style:italic; }}
  .conf {{ margin-left:8px; color:#9A5B00; }}
  .extra {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:16px; }}
  .extra div {{ background:var(--cartao); border:1px solid var(--linha); border-radius:14px; padding:16px 20px; }}
  .extra h4 {{ margin:0 0 6px; }}
  .extra ul {{ margin:0; padding-left:18px; }}
  footer {{ margin-top:28px; font-size:13px; opacity:.7; }}
  @media (max-width:520px) {{ .act {{ grid-template-columns:1fr; gap:2px; }} }}
</style>
</head>
<body>
<main>
  <p class="kicker">Plano feito por um agente · confirma antes de sair de casa</p>
  <h1>Fim de semana em {esc(p['cidade'])}</h1>
  <p class="resumo">{esc(p.get('resumo', ''))}</p>
  <div class="barra">
    <span class="pill">📅 {esc(p.get('fim_de_semana', ''))}</span>
    <span class="pill{' mau' if estoirou else ''}">💶 {orc_txt}{' — passa do orçamento!' if estoirou else ''}</span>
    {f'<a class="pill cal" href="{esc(ics_nome)}" download>📅 Pôr no calendário</a>' if ics_nome else ''}
  </div>
  {avisos_html}
  {''.join(dias_html)}
  <div class="extra">
    <div><h4>🎒 Levar</h4><ul>{''.join(f'<li>{esc(x)}</li>' for x in levar) or '<li>boa disposição</li>'}</ul></div>
    <div><h4>📝 Notas do agente</h4><ul>{''.join(f'<li>{esc(x)}</li>' for x in notas) or '<li>nada a acrescentar</li>'}</ul></div>
  </div>
  <footer>Gerado pelo agente “Fim de semana” · Tempo: dados oficiais · Eventos: só os que têm fonte.
  Um agente pode enganar-se; tu é que vais apanhar a chuva.</footer>
</main>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Plano (JSON) -> página HTML.")
    ap.add_argument("plano", nargs="?", help="ficheiro JSON do plano")
    ap.add_argument("--tema", choices=sorted(TEMAS), default="sol", help="aspeto da página (default: sol)")
    ap.add_argument("--exemplo", action="store_true", help="imprime um plano de exemplo e sai")
    ap.add_argument("--indice", metavar="PASTA", help="cria PASTA/index.html com todos os planos que lá estão")
    args = ap.parse_args()

    if args.exemplo:
        print(json.dumps(EXEMPLO, ensure_ascii=False, indent=2))
        return 0
    if args.indice:
        pasta = pathlib.Path(args.indice)
        planos = []
        for f in sorted(pasta.glob("plano-*.json")):
            try:
                p = json.loads(f.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                print(f"AVISO: {f} tem JSON partido, fica de fora.", file=sys.stderr)
                continue
            if not validar(p):
                planos.append((f.with_suffix(".html").name, p))
        if not planos:
            print(f"ERRO: não há planos válidos (plano-*.json) em {pasta}", file=sys.stderr)
            return 1
        destino = pasta / "index.html"
        destino.write_text(construir_indice(planos, args.tema), encoding="utf-8")
        print(f"Índice criado: {destino} ({len(planos)} planos)")
        return 0
    if not args.plano:
        ap.error("indica o ficheiro JSON do plano (ou usa --exemplo para ver o formato)")

    origem = pathlib.Path(args.plano)
    try:
        plano = json.loads(origem.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERRO: não existe {origem}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"ERRO: o JSON está partido ({e}). Corrige e corre outra vez.", file=sys.stderr)
        return 1

    erros = validar(plano)
    if erros:
        print("ERRO: o plano não está completo:\n  - " + "\n  - ".join(erros), file=sys.stderr)
        return 1

    ics = gerar_ics(plano)
    ics_nome = None
    if ics:
        ics_destino = origem.with_suffix(".ics")
        ics_destino.write_bytes(ics.encode("utf-8"))
        ics_nome = ics_destino.name
    destino = origem.with_suffix(".html")
    destino.write_text(construir(plano, args.tema, ics_nome), encoding="utf-8")
    print(f"Página criada: {destino}")
    if ics_nome:
        print(f"Calendário criado: {origem.with_suffix('.ics')}")
    else:
        print("Sem calendário: nenhum dia tem 'data' (AAAA-MM-DD) nem 'dd/mm' no nome.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
