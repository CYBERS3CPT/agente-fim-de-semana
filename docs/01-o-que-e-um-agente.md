# 1. O que é um agente (e porque não é só um chatbot com a mania)

## A diferença numa frase

> Um **chatbot responde**. Um **agente faz**.

Pergunta a um chatbot "que tempo vai fazer sábado em Lisboa?" e ele responde
com o que *acha* que sabe, que pode ser a previsão de 2023. Pede a um agente
"planeia-me o sábado" e ele vai **buscar** a previsão, **procura** o que há
para fazer, **decide**, **escreve** o plano e **mostra-to**. Dá-se ao trabalho.

## O ciclo: pensar → agir → observar

Todo o agente, do mais simples ao mais caro, faz isto em loop:

```
        ┌──────────────┐
        │   PENSAR     │  "Para planear, preciso primeiro do tempo."
        └──────┬───────┘
               ▼
        ┌──────────────┐
        │    AGIR      │  corre: python3 ferramentas/tempo.py Lisboa
        └──────┬───────┘
               ▼
        ┌──────────────┐
        │  OBSERVAR    │  "Sábado: chuva 100 %. Domingo: sol."
        └──────┬───────┘
               │
               └──────► volta a PENSAR: "Então sábado é museu…"
                        …até o objetivo estar cumprido.
```

A parte interessante é o **observar**. Um programa normal segue uma receita
fixa: se a receita diz "parque", vai ao parque à chuva. Um agente olha para o
resultado de cada passo e **muda de plano**. É por isso que, quando a
`pagina.py` devolve "falta o campo 'dias'", o agente corrige o ficheiro e tenta
outra vez, sem ninguém lhe dizer nada.

## A analogia que vamos usar o tempo todo: o estagiário

Imagina um estagiário novo:

- **É muito inteligente e muito rápido.** Leu a internet inteira.
- **Não sabe nada sobre ti nem sobre a tua empresa.** Nem que tens uma
  criança, nem que detestas filas, nem que o orçamento é 50 €.
- **Faz exatamente o que lhe dizes.** Inclusive coisas que não querias dizer.
- **Às vezes, para não parecer mal, inventa.** Com muita confiança.

Construir um agente é, em grande parte, **fazer o acolhimento deste estagiário**:
escrever-lhe o manual, dar-lhe os acessos certos (e só esses) e dizer-lhe o que
fazer quando não sabe.

## Então o que é, tecnicamente?

```
agente = modelo de linguagem
       + instruções (quem és, o que queres)
       + ferramentas (o que ele pode fazer no mundo)
       + um ciclo (repete até acabar)
       + limites (o que ele NÃO pode fazer sem perguntar)
```

No próximo capítulo abrimos cada uma destas peças no Claude Code:
[2. As cinco peças](02-as-cinco-pecas.md).

## Três ideias erradas que convém deixar à porta

| Ideia errada | Na verdade |
|---|---|
| "Um agente é uma IA que pensa sozinha." | É um modelo num ciclo, com ferramentas que **tu** escolheste. Se não lhe deres a ferramenta, não a tem. |
| "Para fazer um agente tenho de programar." | Neste projeto, o agente é **um ficheiro de texto** (`CLAUDE.md`) e uma **receita** (`SKILL.md`). As ferramentas Python já vêm feitas. |
| "Se é IA, está sempre certo." | É um estagiário brilhante e inventivo. **Inventivo** é a parte preocupante. |
