Crie uma apresentação animada em Manim que explique por que NÃO se deve usar a média aritmética em direções vetoriais (ângulos de vento/bússola), usando a convenção da rosa dos ventos (0°=Norte, 90°=Leste, 180°=Sul, 270°=Oeste, sentido horário).

## CONFIGURAÇÃO DO AMBIENTE

Estou usando um virtualenv chamado .venv na raiz do projeto. Antes de começar:

1. Ative o .venv (source .venv/bin/activate no Linux/Mac ou .venv\Scripts\activate no Windows)
2. Instale as dependências necessárias:
   - pip install manim
   - pip install numpy
   - Verifique dependências de sistema do Manim (ffmpeg, LaTeX/MiKTeX, Cairo, Pango). Se faltar alguma no sistema, me avise com as instruções de instalação apropriadas ao SO antes de prosseguir.
3. Confirme a instalação rodando: manim --version

## CONVENÇÃO MATEMÁTICA A SER USADA (IMPORTANTE)

Use SEMPRE a convenção da rosa dos ventos em todas as animações e cálculos:
- 0° / 360° = Norte (eixo +y)
- 90° = Leste (eixo +x)
- 180° = Sul (eixo -y)
- 270° = Oeste (eixo -x)
- Ângulos crescem no sentido HORÁRIO

Fórmulas de conversão para componentes retangulares (convenção meteorológica):
- u (componente Leste-Oeste) = V · sen(θ)
- v (componente Norte-Sul) = V · cos(θ)
- Direção média = atan2(ū, v̄), depois ajustar para [0°, 360°)

## ESTRUTURA DA APRESENTAÇÃO (crie um arquivo chamado media_vetorial.py com múltiplas cenas)

### Cena 1 — Abertura e Rosa dos Ventos
- Título: "Por que a média aritmética FALHA em direções?"
- Desenhe uma rosa dos ventos completa (N, NE, L, SE, S, SO, O, NO) com marcações de graus
- Mostre a convenção horária com uma seta animada girando de 0° a 360°

### Cena 2 — O Paradoxo dos 350° e 10° (ângulo notável)
- Mostre dois vetores: um a 350° (quase Norte, ligeiramente a Oeste) e outro a 10° (quase Norte, ligeiramente a Leste)
- Calcule a média aritmética animadamente: (350 + 10)/2 = 180° → aponte para o SUL
- Destaque visualmente o ABSURDO: "A média de duas direções quase-Norte dá Sul?!"
- Agora calcule a média vetorial passo a passo:
  * u = [sen(350°) + sen(10°)] / 2 ≈ 0
  * v = [cos(350°) + cos(10°)] / 2 ≈ 0.985
  * atan2(0, 0.985) → 0° = NORTE ✓
- Mostre o vetor resultante apontando corretamente para o Norte

### Cena 3 — Ângulos Notáveis (múltiplos exemplos)
Crie sub-cenas curtas para cada caso, mostrando lado a lado: média aritmética (ERRADA) vs média vetorial (CORRETA):

a) 90° e 270° (Leste e Oeste opostos)
   - Aritmética: 180° (Sul) — arbitrário e sem sentido físico
   - Vetorial: magnitude ≈ 0 → indica "sem direção preferencial" (disperso)

b) 45° e 135° (NE e SE)
   - Aritmética: 90° (Leste) ✓ (coincide neste caso)
   - Vetorial: 90° (Leste) ✓
   - Mostre que nem sempre a aritmética falha, mas NÃO é confiável

c) 315° e 45° (NO e NE)
   - Aritmética: 180° (Sul) — ERRADO
   - Vetorial: 0° (Norte) — CORRETO

### Cena 4 — Ângulos NÃO Notáveis
Use valores "quebrados" para mostrar que o método funciona universalmente:

a) 37°, 128°, 253°, 341° (quatro medições)
   - Calcule a aritmética ingênua: (37+128+253+341)/4 = 189.75° (Sul-Sudoeste)
   - Calcule a vetorial:
     * u = [sen(37)+sen(128)+sen(253)+sen(341)]/4
     * v = [cos(37)+cos(128)+cos(253)+cos(341)]/4
     * Mostre os cálculos numéricos na tela com 3 casas decimais
     * θ = atan2(ū, v̄) convertido para [0°, 360°)
   - Anime os quatro vetores no plano e o vetor resultante

b) 5°, 355°, 2°, 358° (medições consistentes próximas ao Norte)
   - Aritmética: 180° (Sul) — absurdo
   - Vetorial: ≈ 0° (Norte) — coerente

### Cena 5 — Magnitude do Vetor Médio como Medida de Consistência
- Explique: |R| = √(ū² + v̄²)
- Compare dois casos visualmente:
  * Direções concentradas (ex: 0°, 5°, 355°, 10°) → |R| ≈ 1 (vetor longo)
  * Direções dispersas (ex: 0°, 90°, 180°, 270°) → |R| ≈ 0 (vetor curto/nulo)
- Anime o vetor resultante encolhendo/crescendo conforme a dispersão

### Cena 6 — Ponderação pela Velocidade (bônus)
- Mostre a fórmula completa com peso V_i:
  * ū = Σ(V_i · sen(θ_i)) / Σ V_i
  * v̄ = Σ(V_i · cos(θ_i)) / Σ V_i
- Exemplo numérico curto com 3 medições de vento (velocidade + direção)

### Cena 7 — Resumo Final
- Checklist visual:
  ✗ Média aritmética de ângulos: FALHA na descontinuidade 360°/0°
  ✓ Média vetorial: correta, consistente, fisicamente significativa
- Mostre aplicações: anemômetros, correntes oceânicas, análise de marés, navegação

## REQUISITOS TÉCNICOS

- Use classes Scene do Manim (não ManimGL)
- Cada cena deve ser uma classe separada herdando de Scene
- Use cores distintas: VERMELHO para média aritmética errada, VERDE para vetorial correta, AZUL para vetores de entrada
- Adicione transições suaves (FadeIn, FadeOut, Transform, Create)
- Inclua legendas em PORTUGUÊS em todas as cenas
- Use MathTex para fórmulas e Text para textos normais
- Renderize em qualidade média (-qm) para teste e me dê o comando para qualidade alta (-qh)
- Crie um script render_all.sh (ou .bat) que renderize todas as cenas em sequência e concatene em um único vídeo final chamado media_vetorial_final.mp4

## ENTREGAS

1. Arquivo media_vetorial.py com todas as cenas
2. README.md explicando como rodar (incluindo ativação do .venv)
3. requirements.txt com versões exatas
4. Script de renderização automatizada
5. Ao final, execute uma cena de teste (a Cena 2) e me mostre o resultado

Antes de começar a codar, me mostre o plano de arquitetura das cenas e aguarde minha confirmação.