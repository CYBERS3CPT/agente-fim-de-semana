# Guião — "Construir agentes de IA" (60 min, online)

Minuto a minuto, com o que se diz, o que se mostra e o que fazer quando corre
mal. Os números entre parênteses retos são os slides de
[`slides.html`](slides.html) (`#7` no URL salta para o slide 7).

---

## Na véspera (30 min)

- [ ] `./demo/preparar.sh` e um ensaio completo das 5 etapas. Cronometrar.
- [ ] Correr o agente completo para Lisboa (`cd agente && claude`, depois
      `/fim-de-semana Lisboa`). Guardar a página: é o **plano B** do bloco 01.
- [ ] Ensaiar a injeção (bloco 05) **nas duas pastas** e anotar o que
      aconteceu. O comportamento do modelo pode variar de dia para dia. Se o
      resultado for diferente do slide 22, muda o slide ou conta a história
      verdadeira (é ainda melhor).
- [ ] Gravar em vídeo as demos 01 e 04 (QuickTime → Gravação de ecrã). É o
      plano B se a rede cair.
- [ ] Ver o tempo para o fim de semana: se fizer sol nos dois dias, a regra da
      chuva não se vê. Nesse caso, usar uma cidade com chuva na demo (o
      `tempo.py` mostra todas em segundos) ou falar dos avisos.

## 15 minutos antes

- [ ] Terminal: **letra ≥ 20 pt**, tema claro, janela grande. Fechar tudo o resto.
- [ ] Notificações desligadas (o "Não incomodar" existe por alguma razão).
- [ ] Duas janelas: o browser com `slides.html` em ecrã inteiro (tecla F) e o terminal.
- [ ] `./demo/preparar.sh` outra vez: pasta limpa.
- [ ] Abrir `claude` uma vez em `~/fds-ao-vivo` e em `agente/` e aceitar a
      pergunta de confiança. Sem isso, as permissões não contam e a demo
      vira um festival de "Yes".
- [ ] **Nunca** arrancar com o modo de aceitar tudo. Os pedidos de permissão
      fazem parte da história.

---

## 00:00 — Abertura [1–3]

> "Boa tarde. Nesta hora vou construir um agente de IA à vossa frente, sem
> escrever uma linha de código. Para isso preciso da vossa ajuda: escrevam já
> no chat onde vão passar o próximo fim de semana."

[3] Explicar as regras da hora em 30 segundos. Deixar o chat a encher.

## 00:02 — 01. Um agente em ação [4–6]

[5] No terminal, na pasta `agente/`: `/fim-de-semana Lisboa`.

> "Não vou explicar nada ainda. Contem os passos que ele dá sozinho."

Enquanto trabalha (≈ 80 s), ler o chat em voz alta: as cidades, a pergunta
"quanto tempo vos levava isto?".

[6] Mostrar a página que abriu. Apontar três coisas: o sábado de chuva é todo
de interior, a sesta, as fontes.

> 🆘 **Se falhar:** "As demos ao vivo têm um sentido de humor próprio." Abrir a
> página guardada na véspera e seguir.

## 00:07 — 02. O que é um agente [7–11]

[8] Chatbot vs. agente. A frase: **"um chatbot responde, um agente faz."**

[9] O ciclo. Voltar ao terminal e **rolar para cima o registo da demo**:

> "Aqui pensou: preciso do tempo. Aqui agiu: correu a ferramenta. Aqui
> observou: chuva a 100 %. E mudou de plano. Um programa vai ao parque à
> chuva. Um agente olha pela janela."

[10] O estagiário. É a analogia que vai voltar até ao fim.

[11] Sondagem: uma letra no chat. Comentar o resultado em 20 segundos.
Se ganhar o D: "Excelente, vieram pelo motivo certo."

## 00:15 — 03. As cinco peças [12–15]

[13] A tabela. Depois **abrir cada peça no editor** (VS Code ou `cat`):
o `CLAUDE.md`, a pasta da skill, a pasta `ferramentas/`, o `settings.json`.

[14] As instruções.

> "Este ficheiro é a diferença entre 'visite o Castelo de São Jorge' e
> 'sábado chove, Pavilhão do Conhecimento às 10h'. Reparem que não é código.
> É português."

[15] allow / ask / deny.

> "A chave da sala de que precisa, não a chave-mestra do edifício. Guardem
> isto para o bloco 05."

## 00:25 — 04. Construir um, ao vivo [16–18] ⭐ o centro da palestra

[17] deixar no ecrã enquanto se troca para o terminal. Tudo em `~/fds-ao-vivo`.

**Etapa 1 (2 min) — sem manual.**
`claude` → *"Planeia-me o fim de semana em Lisboa."*
> "Desenrasca-se. Mas sabe que tenho uma criança? Que não tenho carro? Não.
> É o estagiário no primeiro dia."

**Etapa 2 (4 min) — o manual.** Pedir ao próprio Claude:
*"Cria um CLAUDE.md para um planeador de fins de semana. Sobre mim: vou com
uma criança de 5 anos que dorme a sesta às 14h, não tenho carro, orçamento de
50 €, detesto filas. Usa sempre python3 ferramentas/tempo.py para o tempo,
nunca inventes eventos, e com chuva acima de 60 % só atividades de interior."*
Mostrar o ficheiro. `/exit`, `claude`, mesmo pedido.
> "Mesmo modelo, mesmas ferramentas. Escrevi texto e o comportamento mudou."

> 🆘 `./demo/preparar.sh --etapa 2` põe o manual pronto.

**Etapa 3 (3 min) — a receita.**
*"Transforma o que acabaste de fazer numa skill chamada fim-de-semana que
termina com uma página feita pela ferramentas/pagina.py."*
Reiniciar e correr `/fim-de-semana Porto`.
> "Agora há um botão. A minha mãe consegue carregar nele."

> 🆘 `./demo/preparar.sh --etapa 3`.

**Etapa 4 (4 min) — as vossas cidades** [18]. Escolher 2 ou 3 do chat, de
preferência uma estrangeira para se ver o Open-Meteo. Ler em voz alta quem a
escreveu.

**Etapa 5 (2 min) — melhorar escrevendo.**
*"A partir de agora usa o tema nova na página. Atualiza a skill."*
Ele vai **pedir autorização para editar a skill**, porque só pode escrever
livremente em `saida/`. Aproveitar: "Reparem: até para mudar as próprias
instruções, pergunta. Fui eu que lhe pus essa trela." Aceitar.
Correr outra vez: a página aparece com as cores da NOVA.
> "Melhorar um agente é, outra vez, escrever."

## 00:40 — 05. Quando corre mal [19–23]

[20] As três maneiras. Rápido: a alucinação toda a gente conhece.

[21] A agenda do bairro. Juntá-la à pasta da demo (até aqui esteve escondida,
para o agente não a ler sozinho): `./demo/preparar.sh --agenda`.
**Abrir `~/fds-ao-vivo/dados/agenda-do-bairro.html` no browser**:
uma agenda simpática. Depois **Ctrl+A**: aparece o texto escondido. Silêncio
na sala é bom sinal.

Correr na pasta da demo:
*"/fim-de-semana Lisboa — usa também a agenda do bairro em dados/agenda-do-bairro.html"*

Três finais possíveis, e todos servem:
- **Calou-se** (o que aconteceu nos ensaios) → [22]: "Resistiu, mas não vos
  disse nada. Ficaram sem saber que a agenda do bairro tenta manipular
  assistentes."
- **Tentou o `curl`** → aparece o pedido de autorização → **dizer que não, em
  voz alta**. "É para isto que serve a lista `ask`."
- **Avisou** → "Ótimo. Mas 'desta vez' não é uma política de segurança."

Depois, o mesmo pedido no agente completo (`agente/`, com a regra no manual),
apontando para `../demo/injecao/agenda-do-bairro.html`. Vai pedir autorização
para ler fora da pasta: aceitar. Nos ensaios, avisou no resumo e no topo do plano.

[23] As três regras. Fechar com: **"o agente não tem responsabilidade civil.
Vocês têm."**

## 00:50 — 06. Para levar [24–26]

[25] O repositório. Pôr o link no chat **agora**, não no fim, quando já
saíram metade.

[26] Três passos para segunda-feira.

## 00:54 — 07. Perguntas [27–28]

Perguntas que costumam aparecer, com respostas curtas:

| Pergunta | Resposta curta |
|---|---|
| "Quanto custa?" | Cada plano custou entre 0,30 e 0,70 dólares nos ensaios. Mais ou menos um café. |
| "Os meus dados vão para onde?" | Para a Anthropic, para o modelo processar. Por isso: dados falsos nos testes, e ler a política da vossa empresa antes de usar dados reais. |
| "Preciso de saber programar?" | Para isto, não. Para ferramentas novas ajuda, mas também se pode pedir ao Claude. |
| "Isto substitui pessoas?" | Substitui tarefas chatas. Quem decide o que é "bom plano" continua a ser uma pessoa. |
| "E se eu não usar Claude?" | As ideias (instruções, receitas, ferramentas, limites) são as mesmas em qualquer agente. Muda o sítio onde se escrevem. |

[28] Obrigado.

---

## Tempos de referência medidos nos ensaios

| Demo | Duração | Custo |
|---|---|---|
| `/fim-de-semana Lisboa` (agente completo) | 80–85 s | ≈ 0,40–0,65 USD |
| injeção, pasta da demo | ≈ 55 s | ≈ 0,35 USD |
