# Carrossel estilo Twitter

Um tweet da Ana por card: fundo branco, avatar, nome "Ana, da RECONECTA", selo de verificado e linha de data e hora.
O processo inteiro está na skill [`.claude/skills/carrossel-tweet/SKILL.md`](../../../.claude/skills/carrossel-tweet/SKILL.md).
No Claude Code, basta pedir "faz um post estilo twitter sobre …".

```bash
pip install playwright pillow && playwright install chromium   # uma vez por máquina

python3 carrosseis/_template/tweet/tweet.py novo "Título do Post" --data 2026-11-04 --hora 12:00
# escrever os cards no tweets.json, pôr img/capa.png e img/prova-1.png, escrever a legenda.txt
python3 carrosseis/_template/tweet/tweet.py render "<pasta do post>"
python3 carrosseis/_template/tweet/tweet.py exportar "<pasta do post>"
```

Sem o SSD, os posts ficam em `./producao/SEM{xx}/`, que é gitignorada.
