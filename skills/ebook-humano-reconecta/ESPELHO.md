# Este diretório é um espelho versionado

A skill viva mora em `~/.claude/skills/ebook-humano-reconecta/`, fora de qualquer
repositório. Este espelho existe porque o que ela guarda — as réguas de
`referencias/` e os scripts de medição — é o resultado mais reaproveitável do
projeto do Script 715, e estava numa pasta sem backup nenhum.

**Editar a skill viva, não este espelho.** Para atualizar aqui depois de mexer lá:

```bash
rsync -a --exclude 'refs/' --exclude '__pycache__/' \
  ~/.claude/skills/ebook-humano-reconecta/ ~/reconecta/skills/ebook-humano-reconecta/
```

O que NÃO vem no espelho: `refs/`, que são 39 MB de seis repositórios MIT clonados
(blader e jooray humanizer, conorbronsdon avoid-ai-writing, luquiluke
claude-book-skill, gregorymm humanize-text, ThomasHoussin Claude-Book) mais a
Wikipedia "Signs of AI writing". São material de leitura de terceiros, recuperável.

A peça mais importante daqui é `referencias/padrao-de-refinamento.md`: oito seções
que saíram de erro medido, não de opinião. Ler antes de começar qualquer livro.
