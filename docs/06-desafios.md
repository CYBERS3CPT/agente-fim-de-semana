# 6. Desafios para casa

Por ordem de dificuldade. Os primeiros só pedem escrita, os últimos pedem
coragem. Nenhum precisa de saber programar, mas todos ficam mais fáceis se
pedires ajuda ao próprio Claude.

## 🟢 Só escrita

1. **O teu "Sobre mim".** Reescreve a secção do `CLAUDE.md` para a tua vida.
   Corre `/fim-de-semana` para a tua cidade. O plano parece teu?
2. **Outro público.** Faz uma versão para "dois amigos de 25 anos, orçamento
   de 80 €, adoram concertos e detestam acordar cedo". Compara os dois planos
   para a mesma cidade. Mudaste uma secção de texto e mudou tudo.
3. **Uma regra nova.** Acrescenta "nunca mais de 20 minutos de deslocação
   entre atividades". O agente cumpre? Como é que sabes?

## 🟡 Uma receita nova

4. **`/dia-de-chuva`.** Uma skill que só sugere atividades de interior, para
   uma tarde, para quando o plano original foi por água abaixo (literalmente).
5. **`/jantar-de-amigos`.** Recebe o número de pessoas e as restrições
   alimentares e devolve uma ementa e a lista de compras. Pista: não precisa
   do `tempo.py`... a não ser que seja um churrasco.
6. **Lista de verificação.** A skill `/fim-de-semana` termina com uma lista
   "antes de entregar, confirma". Acrescenta um item que te importe e testa se
   o agente o respeita.

## 🟠 Mexer nas ferramentas

7. **Marés e ondas.** O IPMA também publica previsões para o mar. Pede ao
   Claude que faça uma `ferramentas/mar.py` no estilo da `tempo.py` (só
   biblioteca padrão, erros em português que dizem o que fazer) e ensina o
   agente a usá-la para dias de praia.
8. **Tema novo.** A `pagina.py` tem três temas (`sol`, `nova`, `noite`).
   Acrescenta o teu.

## 🔴 Segurança (o capítulo 4 na prática)

9. **Injeção mais esperta.** Escreve a tua própria "agenda" com uma instrução
   escondida mais subtil, sem palavras como "ignora" ou "IA". Por exemplo,
   uma "nota da organização" a dizer que um evento "foi transferido" para um
   local que escolhes. O agente apanha? Regista o que aconteceu, com a versão
   do modelo e a data.
10. **Fecha a porta.** Muda o `curl` de `ask` para `deny` no `settings.json`
    e repete o desafio 9. O que muda na experiência? Quando preferes cada um?

> Se fizeres algum destes e quiseres partilhar, abre um *pull request* no
> repositório. As melhores injeções vão para o hall da fama, com o devido
> crédito e alguma vergonha alheia.
