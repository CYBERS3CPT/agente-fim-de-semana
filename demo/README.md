# demo/ — a construção ao vivo

Materiais para o bloco 04 da palestra: construir o agente do zero, em cinco
etapas, numa pasta que começa quase vazia.

```
preparar.sh              monta ~/fds-ao-vivo (só ferramentas e dados)
etapas/
  etapa-2-CLAUDE.md      o manual, versão curta (plano B da etapa 2)
  etapa-3-SKILL.md       a receita, versão curta (plano B da etapa 3)
  etapa-5-avisos.md      a regra dos avisos do IPMA (acrescenta-se ao manual)
injecao/
  agenda-do-bairro.html  a página com a prompt injection (bloco 05)
```

## Uso

```bash
./demo/preparar.sh                # pasta limpa em ~/fds-ao-vivo
./demo/preparar.sh --etapa 3      # salta para o fim da etapa 3
./demo/preparar.sh ~/ensaio       # noutro sítio
./demo/preparar.sh --agenda       # bloco 05: junta a agenda com a injeção
```

No Windows (PowerShell): `.\demo\preparar.ps1`, com `-Etapa 3`, `-Destino` e `-Agenda`.

> ⚠️ Ensaia numa pasta dentro da tua pasta pessoal (como `~/fds-ao-vivo`), não
> em `/tmp`. Nos nossos testes, o Claude Code não carregou o `CLAUDE.md` numa
> pasta temporária, e a etapa 2 parecia não funcionar.

Correr outra vez **apaga e recria** a pasta. Entre ensaios, voltas ao zero num
segundo.

## Porque é que as ferramentas já vêm feitas

Porque a mensagem da palestra é **"construir um agente é escrever bem"**, e
15 minutos não chegam para isso e para programar ao mesmo tempo. As ferramentas
são as mãos, e as mãos compram-se feitas. O cérebro (o `CLAUDE.md`) e as
receitas (as skills) escrevem-se ao vivo.

## Porque é que as etapas existem em ficheiro

Ao vivo pede-se ao próprio Claude que escreva o `CLAUDE.md` e a skill: é mais
impressionante e mostra o agente a construir o agente. Mas o modelo pode
escrever coisas diferentes de cada vez. Se a etapa sair torta, `--etapa N` põe a
versão ensaiada e segue-se em frente. O público nunca sabe. (Agora vocês sabem.
Guardem segredo.)

O guião completo, minuto a minuto, está em [`../palestra/guiao.md`](../palestra/guiao.md).
