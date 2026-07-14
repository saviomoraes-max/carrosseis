# premiere-automation — RECONECTA

Protótipo mínimo e **testável** de automação de edição de anúncios em vídeo para
o **Adobe Premiere Pro (macOS, Apple Silicon)**. O objetivo é montar a edição
programaticamente em Python e abrir o resultado como uma **sequência EDITÁVEL**
no Premiere, mantendo o projeto editável depois.

Duas rotas:

- **Rota A (recomendada, 100% offline):** Python monta a timeline com
  **OpenTimelineIO** e escreve um **FCP7 XML (`.xml`, formato `xmeml`)**. Você só
  dá **File > Import** no Premiere. **Não precisa de extensão, nem CEP, nem
  Premiere aberto** pra gerar o arquivo.
- **Rota B (opcional):** **pymiere** controla o Premiere **aberto** por fora
  (via a extensão CEP "Pymiere Link") e insere os clips na sequência ativa.
  Mais frágil: exige a extensão, `PlayerDebugMode` e é dívida técnica de prazo
  curto (ExtendScript/CEP têm suporte até ~set/2026).

> **Por que FCP7 `.xml` e não `.fcpxml`?** O Premiere atual importa o legado
> **Final Cut Pro 7 XML (`.xml` / `xmeml`)** nativamente e cria uma sequência
> editável. Ele **NÃO importa** `.fcpxml` (Final Cut Pro X) direto. Logo, a rota
> segura usa o adapter **`fcp_xml`**, nunca `fcpx_xml`.

---

## Arquivos

| Arquivo | O que é |
|---|---|
| `requirements.txt` | Dependências fixadas (OTIO + adapters + pymiere). |
| `ad_spec.json` | Spec do anúncio: `fps` + lista de clips `{arquivo, in, out, duracao_s, posicao_s, track}`. Caminhos relativos a `media/`. |
| `otio_assemble.py` | **Rota A.** Lê o spec, monta a timeline e gera `<nome>.xml` (FCP7) — e `.fcpxml` se o adapter existir. |
| `pymiere_insert.py` | **Rota B.** Com o Premiere aberto + Pymiere Link, importa os 3 clips e os insere na sequência ativa. |
| `make_test_media.sh` | Gera `media/clip1..3.mp4` com ffmpeg (3 clipes 5s, 30fps, 1920×1080, cores distintas). |

---

## Pré-requisito de versão do Python (importante)

O OpenTimelineIO 0.18.1 publica wheels para **CPython 3.9–3.13**. **Não há wheel
para Python 3.14** e o build a partir do fonte **falha** nele. Este Mac tem o
Python 3.14 como `python3` padrão (Homebrew), então **use o Python 3.13** para a
Rota A:

```bash
python3.13 --version   # tem que existir; se não, brew install python@3.13
```

ffmpeg também é necessário para gerar a mídia de teste:

```bash
ffmpeg -version | head -1   # se faltar: brew install ffmpeg
```

---

## Rota A — OTIO → FCP7 XML → File > Import (testável SEM extensão)

Roda 100% offline: gera a mídia e gera o XML; você só importa no Premiere.

### 1. Criar o ambiente e instalar

```bash
cd premiere-automation
python3.13 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

> Se quiser o mínimo, sem pymiere/fcpxml:
> `pip install OpenTimelineIO-Plugins==0.18.1`
> (já traz o core 0.18.1 + o adapter `fcp_xml`).

Confirme que o adapter `fcp_xml` está ativo:

```bash
python -c "import opentimelineio as otio; print('fcp_xml' in [a.name for a in otio.plugins.ActiveManifest().adapters])"
# deve imprimir: True
```

### 2. Gerar a mídia de teste

```bash
bash make_test_media.sh
# cria media/clip1.mp4, clip2.mp4, clip3.mp4 (5s cada, 30fps, 1920x1080)
```

> O script usa o filtro `drawtext` quando disponível; em builds de ffmpeg sem
> ele (caso do Homebrew sem libfreetype) cai pra `testsrc2` tingido — cada clip
> fica com cor dominante diferente e um contador embutido, dá pra ver o corte.

### 3. Montar a timeline e gerar o XML

```bash
python otio_assemble.py
# [OK] FCP7 XML (Premiere): .../anuncio_reconecta_teste.xml
```

Gera `anuncio_reconecta_teste.xml` na mesma pasta do spec. Se o adapter
`fcpx_xml` estiver instalado, gera **também** um `.fcpxml` (útil para DaVinci
Resolve / Final Cut, **não** para o Premiere).

> Spec alternativo: `python otio_assemble.py outro_spec.json --out-dir saida/`

### 4. Importar no Premiere Pro

1. Abra o Premiere Pro (2025/2026) e crie/abra um projeto `.prproj`.
2. **File > Import…** (Cmd+I).
3. Selecione `anuncio_reconecta_teste.xml` e confirme. O Premiere reconhece o
   formato FCP7 XML automaticamente (não há item de menu separado "Import FCP
   XML"; é o File > Import comum).
4. O Premiere cria uma **nova Sequence** com o nome da timeline e um **Bin** com
   os 3 clips. Abra a sequência (duplo clique) e confira a track **V1** com os 3
   clips em ordem, cada um com in/out e posição corretos no timecode @ 30 fps.
5. Se algum clip aparecer **Media Offline** (vermelho): clique direito > **Link
   Media…** e aponte para o arquivo.

> **Evitar Media Offline:** o `.xml` usa caminhos **absolutos** `file://`. Mantenha
> a mídia onde estava no momento da geração. Se mover tudo pra outra pasta/volume,
> regenere o XML ou use Link Media. Em volume externo (`/Volumes/SSD kenipe`),
> garanta que esteja montado com o **mesmo nome**.

> **Atenção a fps / DF vs NDF:** este protótipo trava tudo em **30 fps NDF**
> (`timebase=30`, `ntsc=FALSE`). O Premiere reinterpreta DF/NDF por conta própria
> (29.97 sempre vira DF; 24/23.976/59.94 sempre NDF). Se o alvo final for 29.97,
> **gere em 29.97** (mude `fps` no `ad_spec.json`), não em 30, e confira o timecode
> da sequência logo após importar.

**Limitação da rota:** o adapter `fcp_xml` transfere **corte/montagem** (clips,
in/out, posição, tracks, gaps, markers). **Transições e efeitos A/V NÃO
atravessam** — aplique-os manualmente no Premiere depois.

---

## Rota B — pymiere (Premiere aberto + extensão CEP)

Use só se precisar dirigir o Premiere **ao vivo**. Tem mais partes móveis.

> **Python para a Rota B:** o pymiere 1.4.1 (2023, não mantido) tem classifiers
> até Python 3.9. Rode-o num venv **Python 3.10** para evitar surpresas, separado
> do venv 3.13 da Rota A:
> ```bash
> python3.10 -m venv .venv-pymiere && source .venv-pymiere/bin/activate
> pip install pymiere
> ```

### 1. Habilitar PlayerDebugMode (extensão não-assinada)

A extensão "Pymiere Link" não é assinada, então o Premiere só a carrega com o
debug mode ligado. Use a chave **CSXS da sua versão**:

```bash
# Premiere 2025+ (CEP 12):
defaults write com.adobe.CSXS.12 PlayerDebugMode 1
# Premiere 2023/2024 (CEP 11):
defaults write com.adobe.CSXS.11 PlayerDebugMode 1

# Forçar o macOS a reler o plist (sem isso a mudança é "engolida" pelo cache):
killall cfprefsd
killall Finder
```

### 2. Instalar a extensão "Pymiere Link"

Método mais simples (instalador do repo):

```bash
curl -L -o extension_installer_mac.sh https://raw.githubusercontent.com/qmasingarbe/pymiere/master/extension_installer_mac.sh
chmod +x extension_installer_mac.sh
./extension_installer_mac.sh
```

A extensão fica em
`~/Library/Application Support/Adobe/CEP/extensions/com.pymiere.link/`
(path de usuário, não pede senha de admin). Se na versão 25.x o painel não
carregar mesmo com PlayerDebugMode, reinstale neste path de usuário e reinicie
Finder + Premiere.

### 3. Abrir o Premiere e o painel

1. Abra o **Adobe Premiere Pro**.
2. **Window > Extensions** (Janela > Extensões) e clique em **Pymiere Link** —
   isso sobe o servidor HTTP local que o Python usa. Deixe o Premiere aberto.
3. Crie/abra um projeto e deixe **uma sequência ativa** na Timeline.

### 4. Gerar a mídia (se ainda não gerou) e rodar o script

```bash
bash make_test_media.sh
python pymiere_insert.py
```

O script:
- conecta ao Premiere (falha com mensagem clara se o painel não estiver no ar);
- importa cada clip do `ad_spec.json`;
- insere cada um na track de vídeo indicada, no `posicao_s` do spec (via
  `insertClip`, que empurra o resto pra frente — ripple);
- salva o projeto.

Confira na Timeline que os 3 clips aparecem nas posições corretas.

> **Limitações da Rota B (dos fatos verificados):** áudio linkado pode não
> acompanhar o `insertClip`; cada chamada é um round-trip HTTP (lento); pymiere
> foi testado oficialmente até o Premiere 23.1 — em 25.x validar caso a caso; e
> ExtendScript/CEP têm suporte só até ~set/2026 (planeje migração para UXP).

---

## Resumo das decisões

- **Formato mais confiável para o Premiere hoje:** FCP7 XML (`.xml` / `xmeml`),
  adapter `fcp_xml`. **Nunca** `.fcpxml` para importar no Premiere.
- **fps:** um único valor, frames inteiros (`round(segundos * fps)`), o mesmo em
  `available_range`, `source_range` e `global_start_time`.
- **Rota A não depende do Premiere** para gerar o arquivo — testa offline e é a
  primeira a validar. A Rota B é o plano para automação ao vivo, com mais risco.
