# Ortotipografia PT-BR do livro

Régua de pontuação. Ela é independente da régua de voz: a voz pode ser falada e
solta, a pontuação tem que estar certa. Texto correto e leve, não formal.

## Aspas

- **Duplas curvas `“ ”`** no corpo do texto. Nunca `"` reta, que é de máquina de
  escrever e aparece feio no PDF.
- **Simples curvas `‘ ’`** só para citação dentro de citação.
- `«...»` **não é aspas**: é a marcação de ênfase dourada do design. Não trocar.
- **Front matter YAML usa aspas retas.** É configuração, não prosa. O parser do
  `render_pdf.py` tolera as duas, mas o padrão é reta.

Quando pôr aspas:
- fala reproduzida que seja oração inteira, sempre. Falando dá pra ouvir onde a
  fala do outro acaba; no papel, não dá;
- palavra citada como palavra (uso metalinguístico): *ela disse “rosto flácido”*;
- mensagem de WhatsApp reproduzida dentro do parágrafo.

Fragmento curtíssimo e óbvio pode ficar sem.

## Discurso direto

Verbo de dizer + **dois-pontos** + aspas. Nunca vírgula antes da aspa:

> Aí uma outra falou: “é porque eu acho que os pacientes estão procurando
> profissionais mais jovens do que eu.”

O ponto final fica **dentro** das aspas quando o que foi citado é uma frase
inteira. Minúscula depois dos dois-pontos é aceitável e mantém o texto leve,
mas tem que ser consistente no livro inteiro.

Não misturar indireto e direto no mesmo período. Isto está errado:

> ~~Ao passo que a outra falou que morava numa cidade grande, “eu acho que é
> porque aqui tem muita gente.”~~

## O que NÃO é erro (não corrigir)

"pra", "pro", "tá", "tô", "cê", "né", "viu", "ó"; frase abrindo com E, Mas,
Porque, Então, Só que, Agora; fragmento sem verbo como frase; período longo
emendado com vírgula e "e"; repetição de palavra sem sinônimo; "a gente" no
lugar de "nós". Endurecer isso arruína o livro.

## Proibido

Travessão (`—`), sempre. Regra da casa, vale para todo o material.

## Como medir

`scripts/revisor_pontuacao.py <projeto>` acha aspa reta, aspa que não fecha,
fala reportada sem aspas e espaço antes de pontuação. Ele tem falso positivo em
"pergunta"/"responde" como substantivo e em declarativa começando com "O que" ou
"Quem": conferir antes de aplicar.

Verificação final que sempre tem que passar:

```
abre “ == fecha ”  ·  abre ‘ == fecha ’  ·  zero " no corpo  ·  zero —
aspa simples só dentro de aspa dupla
```

## Armadilha registrada (08/set)

Converter aspas em massa pegou o front matter YAML junto, e o HUD de todas as
129 páginas saiu com aspas em volta. Converter só o corpo, e conferir uma prova
renderizada depois. O mesmo cuidado vale para a lista numerada: item de dois
dígitos não cabia no recuo de 44px e era cortado pelo `overflow:hidden`.
