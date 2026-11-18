# 3. Construir o teu agente, passo a passo (≈ 20 minutos)

É exatamente o que se faz ao vivo na palestra, agora ao teu ritmo e sem
ninguém a ver os teus erros de digitação.

## Antes de começar

- **Claude Code instalado.** Instruções oficiais em
  <https://docs.claude.com/en/docs/claude-code/overview>. Precisas de uma conta Claude.
- **Python 3** (já vem no macOS e no Linux; no Windows, instala-o da Microsoft Store).
  Nada de `pip install`: as ferramentas só usam a biblioteca padrão.
- Este repositório descarregado (botão verde **Code → Download ZIP** no GitHub, ou `git clone`).

## Etapa 1: uma pasta quase vazia

```bash
./demo/preparar.sh            # cria ~/fds-ao-vivo só com as ferramentas e os dados
cd ~/fds-ao-vivo
claude                         # na primeira vez: "confias nesta pasta?" → sim
```

No Windows sem bash, copia à mão as pastas `agente/ferramentas` e `agente/dados`
e o ficheiro `agente/.claude/settings.json` para uma pasta nova.

Escreve:

```
Planeia-me o fim de semana em Lisboa.
```

👀 **Repara:** ele desenrasca-se. Talvez até descubra a ferramenta do tempo
sozinho, porque está ali na pasta. Mas o plano é **genérico**: não sabe que vais
com uma criança, que não tens carro, nem quanto queres gastar. É um estagiário
no primeiro dia, sem manual.

## Etapa 2: o manual (`CLAUDE.md`)

Cria um ficheiro `CLAUDE.md` na pasta. Podes escrevê-lo tu ou, muito mais
divertido, **pedir ao próprio Claude que o escreva**:

```
Cria um CLAUDE.md para um planeador de fins de semana. Sobre mim: vou com uma
criança de 5 anos que dorme a sesta às 14h, não tenho carro, orçamento de 50 €,
detesto filas. Usa sempre python3 ferramentas/tempo.py para o tempo, nunca
inventes eventos, e com chuva acima de 60 % só atividades de interior.
```

(Se preferires copiar: [`demo/etapas/etapa-2-CLAUDE.md`](../demo/etapas/etapa-2-CLAUDE.md).)

Sai do Claude (`/exit`), volta a entrar (`claude`) e pede o mesmo plano.

👀 **Repara:** o mesmo modelo, as mesmas ferramentas, e um plano completamente
diferente. **Escreveste texto e o comportamento mudou.** É esta a ideia central.

## Etapa 3: a receita (skill)

Cria `.claude/skills/fim-de-semana/SKILL.md` (copia de
[`demo/etapas/etapa-3-SKILL.md`](../demo/etapas/etapa-3-SKILL.md), ou pede ao Claude:
"transforma o que acabaste de fazer numa skill chamada fim-de-semana, que
termina com uma página HTML feita pela ferramentas/pagina.py").

Reinicia e experimenta:

```
/fim-de-semana Porto
```

👀 **Repara:** agora há um **botão**. Qualquer pessoa da tua família pode
carregar nele sem saber o que é um `CLAUDE.md`.

## Etapa 4: outras cidades

```
/fim-de-semana Funchal
/fim-de-semana Bragança
/fim-de-semana Madrid
```

Fora de Portugal, o `tempo.py` muda sozinho do IPMA para o Open-Meteo.
O agente é o mesmo e os resultados são diferentes, porque **os dados são
diferentes**.

## Etapa 5: melhorar escrevendo

Acrescenta ao `CLAUDE.md` (ou copia [`etapa-5-avisos.md`](../demo/etapas/etapa-5-avisos.md)):

```markdown
## Avisos do IPMA
- Se houver aviso amarelo ou pior, só atividades de interior nesse dia,
  e o aviso vai para o topo do plano.
```

E agora o momento vaidoso:

```
A partir de agora a página usa o tema "nova" (python3 ferramentas/pagina.py ... --tema nova).
Atualiza a skill.
```

👀 **Repara:** o agente **editou a própria receita**. Melhorar um agente é,
outra vez, escrever.

## Etapa 6: agora é teu

Muda a secção "Sobre mim" para a tua vida real. Sem criança? Tira a sesta.
Tens cão? "Só sítios onde entram cães." Orçamento de 200 €? Que inveja.

Depois, ideias em [6. Desafios para casa](06-desafios.md).

## Se alguma coisa correr mal

| Sintoma | Causa provável | Remédio |
|---|---|---|
| Pergunta autorização para tudo | ainda não confiaste na pasta | sai, volta a entrar, aceita a pergunta inicial |
| `/fim-de-semana` não existe | a skill está no sítio errado ou o Claude não foi reiniciado | confirma `.claude/skills/fim-de-semana/SKILL.md` e reinicia |
| "não encontrei a cidade" | nome invulgar | experimenta o nome oficial: "Vila Nova de Gaia", não "Gaia" |
| a previsão não chega ao fim de semana | o IPMA só prevê 5 dias | o `tempo.py` passa sozinho para o Open-Meteo; se nem esse tiver, espera um dia |
| inventou um evento | aconteceu | é por isso que cada atividade tem `fonte` ou `confirmar`. Vai ao [capítulo 4](04-quando-corre-mal.md) |
