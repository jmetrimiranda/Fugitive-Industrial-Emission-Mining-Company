# Apresentação animada — Média aritmética vs. média vetorial

Material didático em Manim explicando por que a média aritmética **falha** ao calcular a direção média de ângulos circulares (ventos, correntes, bússola) e por que a **média vetorial** é o método correto.

Convenção adotada em todas as cenas: rosa dos ventos meteorológica.

- 0° / 360° = Norte (eixo +y)
- 90° = Leste (eixo +x)
- 180° = Sul (eixo −y)
- 270° = Oeste (eixo −x)
- Ângulos crescem no sentido **horário**.

Fórmulas:

- u = V · sen(θ)
- v = V · cos(θ)
- Direção resultante: atan2(ū, v̄), normalizada para [0°, 360°).
- Magnitude (consistência): |R| = √(ū² + v̄²).

---

## 1) Ativar o ambiente

A partir da **raiz do projeto**:

```bash
source .venv/bin/activate
```

Verifique:

```bash
which python    # deve apontar para .venv/bin/python
python -c "import manim; print(manim.__version__)"
```

## 2) Instalar dependências (se ainda não instalou)

```bash
pip install -r requirements_manim.txt
```

O arquivo `requirements_manim.txt` está na **raiz** do projeto. Dependências transitivas (pycairo, manimpango, etc.) podem exigir pacotes de sistema: `ffmpeg`, `pkg-config`, `libcairo2-dev`, `libpango1.0-dev`, `python3-dev`. Além de LaTeX: `texlive-latex-extra`, `texlive-science`, `texlive-latex-recommended`, `dvisvgm`.

## 3) Rodar uma cena individual

A partir desta pasta:

```bash
cd references/manim_media_vetorial
manim -ql media_vetorial.py Cena1_RosaDosVentos    # low quality (smoke test)
manim -qm media_vetorial.py Cena2_Paradoxo350_10   # media quality (720p30)
manim -qh media_vetorial.py Cena2_Paradoxo350_10   # high quality (1080p60)
```

Flags úteis:

- `-ql` 480p15 (rápido, só para debug)
- `-qm` 720p30 (padrão do pipeline)
- `-qh` 1080p60 (alta qualidade)
- `-p`  abre o player ao terminar

Os vídeos ficam em `media/videos/media_vetorial/<qualidade>/`.

## 4) Rodar o pipeline completo

Renderiza todas as cenas e concatena num único MP4 em `reports/media_vetorial_final.mp4`.

A partir de **qualquer diretório**:

```bash
bash references/manim_media_vetorial/render_all.sh
```

Em alta qualidade (1080p60):

```bash
bash references/manim_media_vetorial/render_all.sh --hq
```

## 5) Cenas

| # | Classe | Conteúdo |
| --- | --- | --- |
| 0 | `Cena0_Abertura` | Créditos: Gerência e Otimização — Samarco + ícone de IA + autoria |
| 1 | `Cena1_RosaDosVentos` | Título + rosa dos ventos 8 pontos + seta girando 360° horário |
| 2 | `Cena2_Paradoxo350_10` | Paradoxo de 350° e 10°: aritmética dá Sul; vetorial dá Norte |
| 3 | `Cena3_AngulosNotaveis` | Casos 90°/270°, 45°/135°, 315°/45° |
| 4 | `Cena4_AngulosQuebrados` | Casos não notáveis (37°, 128°, 253°, 341° etc.) |
| 5 | `Cena5_Magnitude` | \|R\| como medida de consistência (concentrado vs. disperso) |
| 6 | `Cena6_Ponderacao` | Média vetorial ponderada por velocidade |
| 7 | `Cena7_Resumo` | Checklist visual: falhas da aritmética vs. vantagens da vetorial |

## 6) Limpeza de saídas

Os arquivos em `media/` são gerados e **ignorados pelo git**. Para limpar:

```bash
rm -rf references/manim_media_vetorial/media/
```
