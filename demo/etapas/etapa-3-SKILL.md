---
name: fim-de-semana
description: Planeia o próximo fim de semana numa cidade e entrega uma página HTML.
argument-hint: <cidade>
---

Planeia o fim de semana em **$ARGUMENTS**:

1. Corre `python3 ferramentas/tempo.py "$ARGUMENTS"`.
2. Procura eventos na web para essas datas (máx. 2 pesquisas). Sem nada fiável?
   Sugestões gerais marcadas "confirmar".
3. Máximo 3 atividades por dia. Respeita o orçamento e a sesta.
4. Escreve `saida/plano-<cidade>.json` no formato de
   `python3 ferramentas/pagina.py --exemplo` e corre
   `python3 ferramentas/pagina.py saida/plano-<cidade>.json`.
5. Abre a página e resume em 3 linhas.
