---
name: fins-de-semana
description: Planeia o fim de semana em VÁRIAS cidades ao mesmo tempo, com um subagente "planeador" por cidade a trabalhar em paralelo, e junta tudo numa página-índice. Usar com /fins-de-semana Braga, Faro, Madrid.
argument-hint: <cidade>, <cidade>, ...
---

# /fins-de-semana — vários agentes, ao mesmo tempo

Cidades pedidas: **$ARGUMENTS**

Em vez de planear uma cidade de cada vez (≈ 80 s cada), lança **um subagente
`planeador` por cidade, todos na mesma resposta**, para trabalharem em paralelo.
É como mandar três estagiários tratar de três cidades em vez de um estagiário
fazer as três: mais rápido, desde que cada um não precise do trabalho do outro.

## Passos

1. Separa as cidades (vírgulas ou "e"). Máximo 5. Com mais, avisa e fica com as 5 primeiras.
2. **Na mesma mensagem**, lança um subagente `planeador` por cidade, com o
   prompt a dizer só o nome da cidade. Lançá-los um a seguir ao outro, à
   espera de cada um, estraga o objetivo.
3. Quando todos responderem, corre:
   `python3 ferramentas/pagina.py --indice saida`
4. Abre `saida/index.html` (`open` no macOS, `xdg-open` no Linux).
5. No terminal, uma linha por cidade com o resumo que o subagente devolveu, e
   no fim quanto tempo levou o conjunto. Se algum falhou, diz qual e porquê.
