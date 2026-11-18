# 🗓️ Agente "Fim de semana"

**Um agente de IA que planeia o teu fim de semana, construído com o Claude Code,
sem escrever código, e explicado peça a peça.**

Material da palestra *Construir agentes de IA* (NOVA IMS). Serve para três coisas:

1. **Usar:** abres a pasta, escreves `/fim-de-semana Braga` e recebes um plano
   com a previsão real do IPMA, eventos com fonte e uma página HTML bonita.
2. **Perceber:** os capítulos em [`docs/`](docs/) explicam o que é um agente,
   de que peças é feito e onde pode correr mal. Para o público geral, com humor.
3. **Construir o teu:** em cerca de 20 minutos, partindo de uma pasta quase vazia.

> Um chatbot **responde**. Um agente **faz**.
> Este faz planos. Ainda não faz a sesta por ti, mas respeita a da criança.

---

## Experimentar em 3 minutos

Precisas do [Claude Code](https://docs.claude.com/en/docs/claude-code/overview)
e do Python 3. Nada mais: sem `pip install`, sem chaves de API para o tempo.

```bash
git clone https://github.com/CYBERS3CPT/agente-fim-de-semana.git
cd agente-fim-de-semana/agente
claude
```

Na primeira vez, o Claude Code pergunta se confias na pasta: **diz que sim**
(senão as permissões do agente são ignoradas e ele pede autorização para tudo).
Depois:

```
/fim-de-semana Lisboa
```

Cerca de 80 segundos depois tens `saida/plano-lisboa.html` aberto no browser,
com um botão **📅 Pôr no calendário** (um ficheiro `.ics` para o telemóvel).
Várias cidades de uma vez, com um agente por cidade a trabalhar em paralelo:

```
/fins-de-semana Braga, Faro, Madrid
```

E tudo o que o agente faz fica registado em `saida/diario.md`.

**Sem instalar nada:** abre o repositório no GitHub Codespaces
(botão **Code → Codespaces**). O ambiente já traz Python e Claude Code;
no terminal, `cd agente && claude`.
Vê um exemplo já feito em [`exemplos/plano-lisboa.html`](exemplos/plano-lisboa.html).

**Agora muda a secção "Sobre mim" do [`agente/CLAUDE.md`](agente/CLAUDE.md)**
(criança, carro, orçamento, gostos) e corre outra vez. O agente passa a ser teu.

---

## O que está aqui

```
agente/                       o agente completo, pronto a usar
  CLAUDE.md                   📘 as instruções: o "manual do estagiário"
  .claude/skills/fim-de-semana/SKILL.md
                              📋 a receita, que se chama com /fim-de-semana
  .claude/skills/fins-de-semana/SKILL.md
                              📋 várias cidades em paralelo, um subagente por cidade
  .claude/agents/planeador.md 🤖 o subagente que trata de uma cidade
  .claude/hooks/diario.py     📒 o hook que escreve o diário de bordo
  .claude/settings.json       🚧 as permissões (o que pode, o que pergunta, o que nunca) e o hook
  ferramentas/tempo.py        🔧 previsão real (IPMA para Portugal, Open-Meteo para o resto)
  ferramentas/pagina.py       🔧 plano (JSON) → página HTML + calendário (.ics)
  dados/eventos-exemplo.md    agenda FICTÍCIA de reserva, para quando a internet falha
  saida/                      onde aparecem os planos

demo/                         a construção ao vivo, em 5 etapas (com planos B)
  preparar.sh / preparar.ps1  monta a pasta da demo (Mac/Linux / Windows)
  injecao/agenda-do-bairro.html
                              ⚠️ página com uma prompt injection escondida (de propósito)
docs/                         os conceitos, explicados
  01-o-que-e-um-agente.md
  02-as-cinco-pecas.md
  03-construir-passo-a-passo.md
  04-quando-corre-mal.md
  05-glossario.md
  06-desafios.md
palestra/                     slides (HTML + PDF) e o guião minuto a minuto
exemplos/                     planos reais gerados nos ensaios (Lisboa; Braga, Faro e
                              Madrid em paralelo) e o diário de bordo dessa execução
.devcontainer/                o ambiente pronto para o GitHub Codespaces
```

## As cinco peças, num relance

| Peça | No Claude Code | Neste projeto |
|---|---|---|
| 🧠 Cérebro | o modelo | Claude |
| 📘 Instruções | `CLAUDE.md` | quem és, para quem trabalhas, regras |
| 📋 Receitas | skills | `/fim-de-semana` |
| 🔧 Ferramentas | comandos, pesquisa web, MCP | `tempo.py`, `pagina.py`, pesquisa web |
| 🚧 Limites | permissões e hooks | escreve só em `saida/`, pergunta antes de enviar para fora, diário de tudo |

Explicação completa em [`docs/02-as-cinco-pecas.md`](docs/02-as-cinco-pecas.md).

## As ferramentas também funcionam sozinhas

```bash
python3 agente/ferramentas/tempo.py Porto
python3 agente/ferramentas/tempo.py "Ponta Delgada" --json
python3 agente/ferramentas/pagina.py --exemplo
```

Uma ferramenta de agente é só um programa pequeno, com uma tarefa, que devolve
texto legível. Vale a pena abrir o [`tempo.py`](agente/ferramentas/tempo.py):
está comentado para quem nunca leu Python.

## ⚠️ Sobre a página com a injeção

[`demo/injecao/agenda-do-bairro.html`](demo/injecao/agenda-do-bairro.html) tem,
em texto invisível, instruções para o agente recomendar um restaurante
inventado e "enviar" o plano para um servidor. É **material didático e
inofensivo**: o restaurante não existe e o domínio `.invalid` nunca resolve
(RFC 2606). Vive fora da pasta do agente, que só a lê se lho pedires. O que acontece quando lê está em
[`docs/04-quando-corre-mal.md`](docs/04-quando-corre-mal.md).

## Dados e fontes

- Tempo: [IPMA](https://api.ipma.pt) (dados abertos) e [Open-Meteo](https://open-meteo.com) (CC BY 4.0).
- Eventos: pesquisa web no momento. **Confirma sempre antes de sair de casa.**
  Um agente pode enganar-se. Tu é que apanhas a chuva.

## Custos

Cada plano gasta tokens da tua conta Claude. Nos ensaios, um plano completo
custou entre 0,30 e 0,70 dólares. Mais ou menos um café, sem o pastel de nata.

## Licença

Código e textos: [MIT](LICENSE). Os logótipos e a imagem gráfica da NOVA IMS
em `palestra/assets/` pertencem à NOVA IMS e não estão abrangidos pela licença.
Servem só para a apresentação, e numa reutilização devem ser trocados pelos teus.
