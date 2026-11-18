# 5. Glossário (para sobreviver a um jantar com engenheiros)

| Termo | Em português corrente |
|---|---|
| **Agente** | Um modelo de linguagem num ciclo, com ferramentas e um objetivo. Faz, não só responde. |
| **Alucinação** | Quando o modelo inventa com confiança. Não é mentira (não há intenção), é "texto plausível" que por acaso é falso. |
| **API** | A porta pela qual um programa fala com outro. O `tempo.py` usa a API do IPMA. |
| **Ciclo do agente** | Pensar → agir → observar → repetir. Também se ouve *agent loop*. |
| **`CLAUDE.md`** | O manual do agente no Claude Code: um ficheiro de texto lido sempre que abres a pasta. |
| **Claude Code** | A ferramenta da Anthropic que põe o Claude a trabalhar no teu computador, com ficheiros e comandos. Nasceu para programadores, mas serve para qualquer tarefa com ficheiros. |
| **Contexto** | Tudo o que o modelo "tem à frente" num dado momento: instruções, conversa, resultados das ferramentas. Tem tamanho limitado, como a memória de curto prazo. |
| **Ferramenta** (*tool*) | Algo que o agente pode usar para agir: correr um comando, pesquisar, ler um ficheiro. Sem ferramentas, só fala. |
| **Headless** | Correr o agente sem conversa, de uma vez: `claude -p "/fim-de-semana Porto"`. Útil para automatizar. |
| **Hook** | Uma regra automática que corre antes ou depois de uma ação do agente (ex.: "antes de qualquer comando, regista-o num ficheiro"). |
| **JSON** | Um formato de texto para dados estruturados, com chavetas. O plano do agente é um JSON antes de ser página. |
| **MCP** (*Model Context Protocol*) | A "tomada universal" que liga agentes a serviços (email, calendário, bases de dados) sem código à medida. |
| **Modelo de linguagem** (LLM) | O "cérebro": um programa treinado em muito texto que prevê a continuação mais útil. |
| **Permissões** | O que o agente pode fazer sem perguntar (`allow`), perguntando (`ask`) ou nunca (`deny`). |
| **Prompt** | O que escreves ao agente. Um bom prompt diz o objetivo, o contexto e o porquê. |
| **Prompt injection** | Instruções escondidas em conteúdo que o agente lê, a tentar mandar nele. Ver [capítulo 4](04-quando-corre-mal.md). |
| **Skill** | Uma receita reutilizável que se chama com `/nome`. Fica em `.claude/skills/<nome>/SKILL.md`. |
| **Menor privilégio** | Dar só os acessos necessários. A chave da sala, não a chave-mestra. |
