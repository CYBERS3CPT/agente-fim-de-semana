#!/usr/bin/env bash
# preparar.sh — monta a pasta da demo "construir um agente do zero".
#
# A pasta nasce QUASE vazia: só as ferramentas (as "mãos", que já vêm feitas)
# e os dados. Não há CLAUDE.md nem skill — isso é o que se escreve ao vivo.
#
#   ./demo/preparar.sh                 # cria ~/fds-ao-vivo
#   ./demo/preparar.sh ~/ensaio        # ou onde quiseres (evita /tmp)
#   ./demo/preparar.sh --etapa 3       # salta para o fim da etapa 3 (plano B)
#   ./demo/preparar.sh --agenda        # bloco 05: só junta a agenda com a injeção
#                                      # à pasta que já existe (não apaga nada)
#
# Correr outra vez apaga a pasta e começa de novo. É esse o objetivo:
# entre ensaios, voltar ao zero em 1 segundo.

set -euo pipefail

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
ETAPA=1
DESTINO="$HOME/fds-ao-vivo"
AGENDA=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --etapa) ETAPA="$2"; shift 2 ;;
    --agenda) AGENDA=1; shift ;;
    -h|--help) sed -n '2,15p' "$0"; exit 0 ;;
    *) DESTINO="$1"; shift ;;
  esac
done

# Bloco 05: a agenda com a prompt injection entra só agora. Se estivesse na
# pasta desde o início, o agente lia-a sozinho ao explorar e estragava a surpresa.
if (( AGENDA )); then
  if [[ ! -f "$DESTINO/.fds-ao-vivo" ]]; then
    echo "Primeiro cria a pasta: ./demo/preparar.sh"; exit 1
  fi
  cp "$RAIZ/demo/injecao/agenda-do-bairro.html" "$DESTINO/dados/"
  echo "Agenda do bairro em $DESTINO/dados/agenda-do-bairro.html. Que comece o teatro."
  exit 0
fi

# Só apagamos pastas que este script criou (têm a marca .fds-ao-vivo).
# Assim, um "./preparar.sh ~/" distraído não leva a tua pasta pessoal.
MARCA=".fds-ao-vivo"
if [[ -e "$DESTINO" ]]; then
  if [[ ! -f "$DESTINO/$MARCA" ]]; then
    echo "'$DESTINO' já existe e não foi criada por este script. Não lhe toco."
    echo "Escolhe outra pasta, ou apaga-a tu se tiveres a certeza."
    exit 1
  fi
  rm -rf "$DESTINO"
fi
mkdir -p "$DESTINO"/{ferramentas,dados,saida,.claude}
touch "$DESTINO/$MARCA"

cp "$RAIZ/agente/ferramentas/"*.py "$DESTINO/ferramentas/"
cp "$RAIZ/agente/dados/"* "$DESTINO/dados/"
cp "$RAIZ/agente/.claude/settings.json" "$DESTINO/.claude/settings.json"
cp -R "$RAIZ/agente/.claude/hooks" "$DESTINO/.claude/hooks"      # o diário de bordo
cp -R "$RAIZ/agente/.claude/agents" "$DESTINO/.claude/agents"    # o planeador (para /fins-de-semana)

# Plano B: avançar até ao fim de uma etapa, se o ao vivo correr mal.
if (( ETAPA >= 2 )); then cp "$RAIZ/demo/etapas/etapa-2-CLAUDE.md" "$DESTINO/CLAUDE.md"; fi
if (( ETAPA >= 3 )); then
  mkdir -p "$DESTINO/.claude/skills/fim-de-semana"
  cp "$RAIZ/demo/etapas/etapa-3-SKILL.md" "$DESTINO/.claude/skills/fim-de-semana/SKILL.md"
fi
if (( ETAPA >= 5 )); then cat "$RAIZ/demo/etapas/etapa-5-avisos.md" >> "$DESTINO/CLAUDE.md"; fi

cat <<MSG

Pasta pronta: $DESTINO  (etapa $ETAPA)

  cd $DESTINO && claude

Na primeira vez o Claude Code pergunta se confias na pasta: diz que sim.
Sem isso, as permissões de .claude/settings.json são ignoradas e vais
passar a demo a carregar em "Yes". O público vai achar que é de propósito.
MSG
