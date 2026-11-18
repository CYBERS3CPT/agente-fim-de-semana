# 2. As cinco peças de um agente (e onde estão no Claude Code)

| Peça | Para que serve | No Claude Code | Neste projeto | O estagiário |
|---|---|---|---|---|
| 🧠 **Cérebro** | raciocinar e decidir | o modelo (Claude) | — vem incluído | a cabeça |
| 📘 **Instruções** | quem és, para quem trabalhas, regras | `CLAUDE.md` | [`agente/CLAUDE.md`](../agente/CLAUDE.md) | o manual de acolhimento |
| 📋 **Receitas** | como se faz *uma* tarefa, sempre igual | skills (`.claude/skills/<nome>/SKILL.md`) | [`/fim-de-semana`](../agente/.claude/skills/fim-de-semana/SKILL.md) | "quando te pedirem X, faz assim" |
| 🔧 **Ferramentas** | agir no mundo: ler, procurar, escrever | ferramentas internas, comandos, MCP | [`tempo.py`](../agente/ferramentas/tempo.py), [`pagina.py`](../agente/ferramentas/pagina.py), pesquisa web | os acessos e o portátil |
| 🚧 **Limites** | o que pode fazer sozinho e o que tem de perguntar | permissões (`.claude/settings.json`) e hooks | [`settings.json`](../agente/.claude/settings.json) | "isto pergunta-me sempre antes" |

Vamos a cada uma.

---

## 🧠 Cérebro: o modelo

É o que lê, raciocina e decide o próximo passo. Não o constróis: escolhes-o.
Um modelo mais capaz erra menos e decide melhor quando a coisa é ambígua. Um
mais pequeno é mais rápido e mais barato. Para um plano de fim de semana,
qualquer um serve. Para decidir quem recebe um crédito bancário, pensa duas vezes
(e depois pensa uma terceira, com um advogado).

## 📘 Instruções: o `CLAUDE.md`

Um ficheiro de texto normal que o Claude Code lê **sempre** que abres a pasta.
É aqui que o agente deixa de ser genérico e passa a ser **teu**:

```markdown
## Sobre mim (muda isto!)
- Vou com uma criança de 5 anos. Às 14h há sesta, ou há birra.
- Não tenho carro.
- Orçamento: 50 €.
```

**A lição mais importante deste projeto inteiro:** a diferença entre um plano
genérico ("visite o Castelo de São Jorge!") e um plano útil ("sábado chove,
Pavilhão do Conhecimento às 10h, antes das filas, 18 €") **não é programação.
É escrita.** Quem escreve bem instruções para pessoas escreve bem instruções
para agentes.

Boas instruções são como boas instruções para um colega:
- dizem **o objetivo**, não só os passos;
- explicam **porquê** ("um evento inventado é pior do que nenhum: alguém vai lá estar às 10h");
- dizem **o que fazer quando algo falha** ("se a ferramenta falhar, diz isso");
- são **curtas**. Ninguém lê um manual de 40 páginas, nem o estagiário.

## 📋 Receitas: as skills

O `CLAUDE.md` diz **quem** és. Uma skill diz **como** se faz **uma tarefa**.
Fica numa pasta própria e ativa-se com `/nome`:

```
.claude/skills/fim-de-semana/SKILL.md   →   /fim-de-semana Porto
```

Porquê separar? Porque um agente pode ter várias receitas (`/fim-de-semana`,
`/jantar-de-amigos`, `/ferias-de-verao`) e só carrega a que precisa. É como
ter um livro de receitas em vez de decorar todas.

A receita deste projeto tem uma **lista de verificação no fim**. É o truque
mais barato para melhorar um agente: pedir-lhe que confirme o próprio trabalho
antes de o entregar. Funciona com estagiários e funciona com modelos.

## 🔧 Ferramentas: as mãos

Sem ferramentas, o modelo só consegue **falar**. Com ferramentas consegue
**fazer**. Neste projeto:

| Ferramenta | O que faz | Porque existe |
|---|---|---|
| `tempo.py` | previsão real (IPMA / Open-Meteo) | o modelo não sabe o tempo de sábado; ninguém sabe sem perguntar a quem mede |
| pesquisa web | encontra eventos | a agenda muda todas as semanas |
| `pagina.py` | JSON → página bonita | o modelo decide, o código formata: cada um faz aquilo em que é bom |

Uma ferramenta de agente é **um programa pequeno com uma só tarefa, que devolve
texto legível**. Abre o [`tempo.py`](../agente/ferramentas/tempo.py): tem
comentários a explicar cada decisão. Repara nas mensagens de erro, que dizem ao
agente **o que fazer a seguir** ("Sem dados, não há previsão — não inventes uma.").
Os erros de uma ferramenta também são instruções.

> **E o MCP?** O *Model Context Protocol* é a "tomada universal" para
> ferramentas: liga o agente ao email, ao calendário, a uma base de dados, sem
> escrever código à medida para cada um. Este projeto não precisa de MCP (o
> tempo vem de um script), mas é o passo natural seguinte: o teu agente de fim
> de semana a marcar o evento no teu calendário.

## 🚧 Limites: permissões

O ficheiro [`.claude/settings.json`](../agente/.claude/settings.json) diz o que o
agente pode fazer **sem perguntar**, o que **tem de perguntar** e o que está
**proibido**:

```jsonc
"allow": [ "Bash(python3 ferramentas/tempo.py:*)", "Write(./saida/**)", "WebSearch" ],
"ask":   [ "Bash(curl:*)" ],          // enviar coisas para a internet? pergunta-me.
"deny":  [ "Read(~/.ssh/**)" ]        // as minhas chaves? nem pensar.
```

É o **princípio do menor privilégio**: dar ao estagiário a chave da sala de que
precisa, não a chave-mestra do edifício. No [capítulo 4](04-quando-corre-mal.md)
vês porquê. Spoiler: há páginas web que tentam dar ordens ao teu agente.

> ⚠️ **Armadilha clássica:** o Claude Code só aplica as permissões de uma pasta
> depois de lhe dizeres que **confias** nela (a pergunta que aparece na primeira
> vez que abres o `claude` lá). Até lá, pergunta tudo. É chato, mas é uma
> excelente ideia: imagina descarregar uma pasta da internet que se dava a si
> própria permissão para tudo.

---

Próximo: [3. Construir o teu, passo a passo](03-construir-passo-a-passo.md).
