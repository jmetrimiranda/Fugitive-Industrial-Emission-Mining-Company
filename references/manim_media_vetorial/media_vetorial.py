from manim import *
import numpy as np

# ==================== PALETA ====================
COR_ARITMETICA = RED
COR_VETORIAL = GREEN
COR_ENTRADA = BLUE
COR_EIXOS = WHITE


# ==================== UTILIDADES ====================
def meteo_to_xy(theta_deg, magnitude=1.0):
    theta_rad = np.deg2rad(theta_deg)
    u = magnitude * np.sin(theta_rad)
    v = magnitude * np.cos(theta_rad)
    return np.array([u, v, 0.0])


def media_aritmetica(angulos):
    return float(np.mean(np.asarray(angulos, dtype=float)))


def media_vetorial(angulos, pesos=None):
    angulos = np.asarray(angulos, dtype=float)
    if pesos is None:
        pesos = np.ones_like(angulos)
    else:
        pesos = np.asarray(pesos, dtype=float)
    theta_rad = np.deg2rad(angulos)
    soma_pesos = np.sum(pesos)
    u_bar = np.sum(pesos * np.sin(theta_rad)) / soma_pesos
    v_bar = np.sum(pesos * np.cos(theta_rad)) / soma_pesos
    theta_res = np.rad2deg(np.arctan2(u_bar, v_bar)) % 360.0
    magnitude = float(np.sqrt(u_bar ** 2 + v_bar ** 2))
    return float(theta_res), magnitude


def criar_vetor_direcao(theta_deg, cor, magnitude=2.0, stroke_width=6):
    return Arrow(
        start=ORIGIN,
        end=meteo_to_xy(theta_deg, magnitude),
        color=cor,
        buff=0,
        stroke_width=stroke_width,
        max_tip_length_to_length_ratio=0.18,
    )


def _ponto_axes(axes, theta_deg, magnitude):
    xy = meteo_to_xy(theta_deg, magnitude)
    return axes.c2p(xy[0], xy[1])


# ==================== CENA 0 — ABERTURA ====================
class Cena0_Abertura(Scene):
    def construct(self):
        header = Text(
            "Gerência e Otimização: Samarco",
            font_size=38,
            weight=BOLD,
        ).to_edge(UP, buff=1.2)

        # Ícone de IA: rede neural de 3 camadas
        camadas_x = [-1.6, 0.0, 1.6]
        camadas_n = [3, 4, 2]
        nodes_por_camada = []
        for lx, n in zip(camadas_x, camadas_n):
            ys = np.linspace(-(n - 1) / 2, (n - 1) / 2, n) * 0.75
            camada = VGroup(*[
                Dot(point=np.array([lx, y, 0.0]), radius=0.13, color=BLUE_B)
                for y in ys
            ])
            nodes_por_camada.append(camada)

        linhas = VGroup()
        for i in range(len(nodes_por_camada) - 1):
            for a in nodes_por_camada[i]:
                for b in nodes_por_camada[i + 1]:
                    linhas.add(Line(
                        a.get_center(), b.get_center(),
                        stroke_width=1.8, color=BLUE_D, stroke_opacity=0.75,
                    ))
        nodes_all = VGroup(*nodes_por_camada)
        halo = Circle(radius=2.4, color=BLUE_E, stroke_width=2,
                      stroke_opacity=0.35).move_to(ORIGIN)
        ai_group = VGroup(halo, linhas, nodes_all)
        ai_group.move_to(ORIGIN).shift(DOWN * 0.2)

        legenda_ia = Text("I A", font_size=24, color=BLUE_B,
                          weight=BOLD, slant=ITALIC)
        legenda_ia.next_to(ai_group, DOWN, buff=0.35)

        nome = Text(
            "Eng. Automação  |  Jorge Metri Miranda",
            font_size=30,
        ).to_edge(DOWN, buff=1.1)

        self.play(Write(header), run_time=1.4)
        self.wait(0.2)
        self.play(Create(halo), run_time=0.8)
        self.play(
            *[Create(n) for layer in nodes_por_camada for n in layer],
            run_time=0.9,
        )
        self.play(Create(linhas, lag_ratio=0.02), run_time=1.4)
        self.play(FadeIn(legenda_ia, shift=UP * 0.1))
        self.wait(0.3)
        self.play(Write(nome), run_time=1.2)
        self.wait(2.5)

        self.play(
            FadeOut(header), FadeOut(ai_group),
            FadeOut(legenda_ia), FadeOut(nome),
            run_time=1.0,
        )


# ==================== CENA 1 ====================
class Cena1_RosaDosVentos(Scene):
    def construct(self):
        titulo = Text(
            "Por que a média aritmética FALHA em direções?",
            font_size=30,
        ).to_edge(UP, buff=0.35)
        self.play(Write(titulo))
        self.wait(0.6)

        eixos = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=5,
            y_length=5,
            axis_config={"stroke_color": COR_EIXOS, "stroke_width": 2},
            tips=False,
        ).shift(DOWN * 0.4)
        self.play(Create(eixos), run_time=1.2)

        marcador_n = Text("+y = Norte", font_size=16, color=COR_EIXOS)
        marcador_n.next_to(eixos.c2p(0, 2.5), UP, buff=0.08)
        marcador_e = Text("+x = Leste", font_size=16, color=COR_EIXOS)
        marcador_e.next_to(eixos.c2p(2.5, 0), RIGHT, buff=0.08)
        self.play(FadeIn(marcador_n), FadeIn(marcador_e))

        circulo = Circle(radius=2.1, color=COR_EIXOS, stroke_width=2).move_to(eixos.c2p(0, 0))
        self.play(Create(circulo))

        pontos_cardeais = [
            (0,   "N",  "0°/360°"),
            (45,  "NE", "45°"),
            (90,  "L",  "90°"),
            (135, "SE", "135°"),
            (180, "S",  "180°"),
            (225, "SO", "225°"),
            (270, "O",  "270°"),
            (315, "NO", "315°"),
        ]

        rotulos = VGroup()
        marcas = VGroup()
        graus = VGroup()
        for theta, sigla, grau_txt in pontos_cardeais:
            p_sigla = _ponto_axes(eixos, theta, 2.4)
            p_grau = _ponto_axes(eixos, theta, 2.85)
            p_marca_ini = _ponto_axes(eixos, theta, 2.0)
            p_marca_fim = _ponto_axes(eixos, theta, 2.15)

            rotulos.add(Text(sigla, font_size=22, color=COR_EIXOS).move_to(p_sigla))
            graus.add(Text(grau_txt, font_size=14, color=COR_EIXOS).move_to(p_grau))
            marcas.add(Line(p_marca_ini, p_marca_fim, color=COR_EIXOS, stroke_width=2))

        self.play(FadeIn(marcas, lag_ratio=0.05), run_time=1)
        self.play(FadeIn(rotulos, lag_ratio=0.08), run_time=1.2)
        self.play(FadeIn(graus, lag_ratio=0.08), run_time=1.2)

        seta = Arrow(
            eixos.c2p(0, 0),
            _ponto_axes(eixos, 0, 1.7),
            color=COR_ENTRADA,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.2,
        )
        self.play(GrowArrow(seta))

        # Rotação horária: ângulo negativo em Manim
        self.play(
            Rotate(seta, angle=-TAU, about_point=eixos.c2p(0, 0)),
            run_time=5,
            rate_func=linear,
        )
        self.wait(0.5)

        fim = Text(
            "Os ângulos são circulares — 360° e 0° são o mesmo ponto.",
            font_size=24,
            color=COR_EIXOS,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(fim))
        self.wait(2)

        self.play(
            FadeOut(seta), FadeOut(rotulos), FadeOut(graus), FadeOut(marcas),
            FadeOut(circulo), FadeOut(eixos), FadeOut(titulo),
            FadeOut(marcador_n), FadeOut(marcador_e), FadeOut(fim),
        )


# ==================== CENA 2 ====================
class Cena2_Paradoxo350_10(Scene):
    def construct(self):
        titulo = Text("Paradoxo: 350° e 10°", font_size=38).to_edge(UP)
        self.play(Write(titulo))

        eixos = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=5,
            y_length=5,
            axis_config={"stroke_color": COR_EIXOS, "stroke_width": 2},
            tips=False,
        ).shift(RIGHT * 2.2)
        self.play(Create(eixos), run_time=1)

        origem = eixos.c2p(0, 0)
        ang1, ang2 = 350.0, 10.0

        v1 = Arrow(
            origem, _ponto_axes(eixos, ang1, 2.2),
            color=COR_ENTRADA, buff=0, stroke_width=6,
            max_tip_length_to_length_ratio=0.18,
        )
        v2 = Arrow(
            origem, _ponto_axes(eixos, ang2, 2.2),
            color=COR_ENTRADA, buff=0, stroke_width=6,
            max_tip_length_to_length_ratio=0.18,
        )
        rot1 = Text("350°", font_size=22, color=COR_ENTRADA).next_to(v1.get_end(), UL, buff=0.15)
        rot2 = Text("10°", font_size=22, color=COR_ENTRADA).next_to(v2.get_end(), UR, buff=0.15)

        self.play(GrowArrow(v1), GrowArrow(v2), FadeIn(rot1), FadeIn(rot2))

        obs = Text(
            "Ambos apontam\npara o Norte.",
            font_size=22, color=COR_ENTRADA, line_spacing=0.9,
        ).to_edge(LEFT, buff=0.5).shift(UP * 1.8)
        self.play(FadeIn(obs))
        self.wait(0.8)

        # ---------- Média aritmética ----------
        aritm = media_aritmetica([ang1, ang2])
        formula_arit = MathTex(
            r"\bar{\theta}_{\text{arit}} = \frac{350° + 10°}{2} = 180°",
            color=COR_ARITMETICA,
            font_size=30,
        ).to_edge(LEFT, buff=0.3).shift(UP * 0.3)
        self.play(Write(formula_arit))
        self.wait(0.3)

        seta_arit = Arrow(
            origem, _ponto_axes(eixos, aritm, 2.0),
            color=COR_ARITMETICA, buff=0, stroke_width=7,
            max_tip_length_to_length_ratio=0.18,
        )
        rot_arit = Text("180° → SUL", font_size=22, color=COR_ARITMETICA)
        rot_arit.next_to(seta_arit.get_end(), DOWN, buff=0.15)
        self.play(GrowArrow(seta_arit), FadeIn(rot_arit))

        alerta = Text(
            "⚠ Absurdo!  Os vetores vão ao Norte,\na média aritmética diz Sul.",
            font_size=22, color=COR_ARITMETICA, line_spacing=0.9,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(alerta))
        self.wait(2)
        self.play(FadeOut(seta_arit), FadeOut(rot_arit), FadeOut(alerta), FadeOut(formula_arit))

        # ---------- Média vetorial ----------
        theta_v, _mag = media_vetorial([ang1, ang2])
        u_bar = (np.sin(np.deg2rad(ang1)) + np.sin(np.deg2rad(ang2))) / 2
        v_bar = (np.cos(np.deg2rad(ang1)) + np.cos(np.deg2rad(ang2))) / 2

        linha_u = MathTex(
            r"\bar{u} = \tfrac{\sin(350°) + \sin(10°)}{2}"
            r" \approx " + f"{u_bar:.3f}",
            color=COR_VETORIAL, font_size=26,
        )
        linha_v = MathTex(
            r"\bar{v} = \tfrac{\cos(350°) + \cos(10°)}{2}"
            r" \approx " + f"{v_bar:.3f}",
            color=COR_VETORIAL, font_size=26,
        )
        linha_theta = MathTex(
            r"\bar{\theta}_{\text{vet}} = \mathrm{atan2}(\bar{u},\bar{v})"
            r" = " + f"{theta_v:.1f}°",
            color=COR_VETORIAL, font_size=26,
        )
        passos = VGroup(linha_u, linha_v, linha_theta).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3
        ).to_edge(LEFT, buff=0.3).shift(UP * 0.1)

        for p in passos:
            self.play(Write(p), run_time=0.9)
        self.wait(0.3)

        seta_vet = Arrow(
            origem, _ponto_axes(eixos, theta_v, 2.0),
            color=COR_VETORIAL, buff=0, stroke_width=7,
            max_tip_length_to_length_ratio=0.18,
        )
        rot_vet = Text(f"{theta_v:.1f}° → NORTE ✓", font_size=22, color=COR_VETORIAL)
        rot_vet.next_to(seta_vet.get_end(), UP, buff=0.15)
        self.play(GrowArrow(seta_vet), FadeIn(rot_vet))
        self.wait(1.2)

        conclusao = Text(
            "Método vetorial respeita a geometria circular.",
            font_size=24, color=COR_VETORIAL,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(conclusao))
        self.wait(2.5)

        self.play(
            FadeOut(v1), FadeOut(v2), FadeOut(rot1), FadeOut(rot2),
            FadeOut(seta_vet), FadeOut(rot_vet), FadeOut(passos),
            FadeOut(obs), FadeOut(conclusao), FadeOut(eixos), FadeOut(titulo),
        )


# ==================== HELPER PARA MINI-EIXOS ====================
def _mini_axes(scale=1.0, shift_vec=ORIGIN):
    eixos = Axes(
        x_range=[-1.5, 1.5, 1],
        y_range=[-1.5, 1.5, 1],
        x_length=3 * scale,
        y_length=3 * scale,
        axis_config={"stroke_color": COR_EIXOS, "stroke_width": 1.5},
        tips=False,
    )
    eixos.shift(shift_vec)
    return eixos


# ==================== CENA 3 ====================
class Cena3_AngulosNotaveis(Scene):
    def _sub_caso(self, angulos, rotulo_caso, descricao_arit, descricao_vet):
        titulo = Text(rotulo_caso, font_size=34).to_edge(UP)
        self.play(Write(titulo))

        eixos = Axes(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1],
            x_length=5, y_length=5,
            axis_config={"stroke_color": COR_EIXOS, "stroke_width": 2},
            tips=False,
        ).shift(RIGHT * 2.5)
        self.play(Create(eixos), run_time=0.8)

        origem = eixos.c2p(0, 0)
        setas_in = VGroup()
        rotulos_in = VGroup()
        for a in angulos:
            s = Arrow(
                origem, _ponto_axes(eixos, a, 1.6),
                color=COR_ENTRADA, buff=0, stroke_width=5,
                max_tip_length_to_length_ratio=0.2,
            )
            setas_in.add(s)
            rotulos_in.add(
                Text(f"{a:g}°", font_size=20, color=COR_ENTRADA)
                .next_to(s.get_end(), direction=meteo_to_xy(a, 1), buff=0.15)
            )
        self.play(*[GrowArrow(s) for s in setas_in], FadeIn(rotulos_in))
        self.wait(0.3)

        aritm = media_aritmetica(angulos)
        theta_v, mag = media_vetorial(angulos)

        txt_arit = Text(descricao_arit, font_size=22, color=COR_ARITMETICA, line_spacing=0.9)
        txt_arit.to_edge(LEFT, buff=0.3).shift(UP * 1.0)
        txt_vet = Text(descricao_vet, font_size=22, color=COR_VETORIAL, line_spacing=0.9)
        txt_vet.to_edge(LEFT, buff=0.3).shift(DOWN * 1.0)

        seta_arit = Arrow(
            origem, _ponto_axes(eixos, aritm, 1.4),
            color=COR_ARITMETICA, buff=0, stroke_width=6,
            max_tip_length_to_length_ratio=0.2,
        )
        self.play(Write(txt_arit), GrowArrow(seta_arit))
        self.wait(0.8)

        if mag < 0.05:
            seta_vet = Dot(origem, color=COR_VETORIAL, radius=0.12)
            self.play(Write(txt_vet), FadeIn(seta_vet, scale=2))
        else:
            seta_vet = Arrow(
                origem, _ponto_axes(eixos, theta_v, 1.4 * max(mag, 0.25)),
                color=COR_VETORIAL, buff=0, stroke_width=6,
                max_tip_length_to_length_ratio=0.2,
            )
            self.play(Write(txt_vet), GrowArrow(seta_vet))
        self.wait(2)

        self.play(
            FadeOut(titulo), FadeOut(eixos), FadeOut(setas_in), FadeOut(rotulos_in),
            FadeOut(seta_arit), FadeOut(seta_vet), FadeOut(txt_arit), FadeOut(txt_vet),
        )

    def construct(self):
        intro = Text("Casos notáveis", font_size=40).to_edge(UP)
        sub = Text(
            "Comparando aritmética (vermelho) e vetorial (verde)",
            font_size=24,
        ).next_to(intro, DOWN, buff=0.3)
        self.play(Write(intro), FadeIn(sub))
        self.wait(1.2)
        self.play(FadeOut(intro), FadeOut(sub))

        self._sub_caso(
            [90, 270],
            "(a)  90°  e  270°",
            "Aritmética = 180°\n(escolha arbitrária)",
            "Vetorial: |R| ≈ 0\nsem direção preferencial",
        )
        self._sub_caso(
            [45, 135],
            "(b)  45°  e  135°",
            "Aritmética = 90°\n(coincide nesse caso)",
            "Vetorial = 90°\ncoincide — mas a aritmética\nnão é confiável em geral",
        )
        self._sub_caso(
            [315, 45],
            "(c)  315°  e  45°",
            "Aritmética = 180°\nERRADO (aponta Sul)",
            "Vetorial = 0° (Norte)\nCORRETO",
        )


# ==================== CENA 4 ====================
class Cena4_AngulosQuebrados(Scene):
    def _sub_caso(self, angulos, titulo_txt):
        titulo = Text(titulo_txt, font_size=34).to_edge(UP)
        self.play(Write(titulo))

        eixos = Axes(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1],
            x_length=5, y_length=5,
            axis_config={"stroke_color": COR_EIXOS, "stroke_width": 2},
            tips=False,
        ).shift(RIGHT * 2.5)
        self.play(Create(eixos), run_time=0.8)

        origem = eixos.c2p(0, 0)
        setas_in = VGroup()
        rotulos_in = VGroup()
        for a in angulos:
            s = Arrow(
                origem, _ponto_axes(eixos, a, 1.5),
                color=COR_ENTRADA, buff=0, stroke_width=4,
                max_tip_length_to_length_ratio=0.2,
            )
            setas_in.add(s)
            rotulos_in.add(
                Text(f"{a:g}°", font_size=18, color=COR_ENTRADA)
                .next_to(s.get_end(), direction=meteo_to_xy(a, 1), buff=0.1)
            )
        self.play(*[GrowArrow(s) for s in setas_in], FadeIn(rotulos_in))

        aritm = media_aritmetica(angulos)
        theta_v, mag = media_vetorial(angulos)

        formula_arit = MathTex(
            r"\bar{\theta}_{\text{arit}} = " + f"{aritm:.2f}°",
            color=COR_ARITMETICA, font_size=32,
        ).to_edge(LEFT, buff=0.3).shift(UP * 1.6)
        seta_arit = Arrow(
            origem, _ponto_axes(eixos, aritm, 1.3),
            color=COR_ARITMETICA, buff=0, stroke_width=6,
            max_tip_length_to_length_ratio=0.2,
        )
        self.play(Write(formula_arit), GrowArrow(seta_arit))
        self.wait(0.8)

        # passos vetoriais
        u_bar = np.mean(np.sin(np.deg2rad(angulos)))
        v_bar = np.mean(np.cos(np.deg2rad(angulos)))
        formula_vet = VGroup(
            MathTex(r"\bar{u} = " + f"{u_bar:.3f}", color=COR_VETORIAL, font_size=26),
            MathTex(r"\bar{v} = " + f"{v_bar:.3f}", color=COR_VETORIAL, font_size=26),
            MathTex(r"\bar{\theta}_{\text{vet}} = " + f"{theta_v:.3f}°",
                    color=COR_VETORIAL, font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        formula_vet.to_edge(LEFT, buff=0.3).shift(DOWN * 0.8)

        for linha in formula_vet:
            self.play(Write(linha), run_time=0.6)

        if mag < 0.05:
            seta_vet = Dot(origem, color=COR_VETORIAL, radius=0.1)
            self.play(FadeIn(seta_vet, scale=2))
        else:
            seta_vet = Arrow(
                origem, _ponto_axes(eixos, theta_v, 1.3),
                color=COR_VETORIAL, buff=0, stroke_width=6,
                max_tip_length_to_length_ratio=0.2,
            )
            self.play(GrowArrow(seta_vet))
        self.wait(2.5)

        self.play(
            FadeOut(titulo), FadeOut(eixos), FadeOut(setas_in), FadeOut(rotulos_in),
            FadeOut(seta_arit), FadeOut(seta_vet),
            FadeOut(formula_arit), FadeOut(formula_vet),
        )

    def construct(self):
        intro = Text("Ângulos não notáveis", font_size=40).to_edge(UP)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))

        self._sub_caso([37, 128, 253, 341], "(a)  37°,  128°,  253°,  341°")
        self._sub_caso([5, 355, 2, 358], "(b)  5°,  355°,  2°,  358°")


# ==================== CENA 5 ====================
class Cena5_Magnitude(Scene):
    def _caso(self, angulos, rotulo):
        titulo = Text(rotulo, font_size=32).to_edge(UP, buff=0.5)
        self.play(Write(titulo))

        eixos = Axes(
            x_range=[-1.5, 1.5, 1], y_range=[-1.5, 1.5, 1],
            x_length=4, y_length=4,
            axis_config={"stroke_color": COR_EIXOS, "stroke_width": 2},
            tips=False,
        ).shift(RIGHT * 2.5)
        self.play(Create(eixos), run_time=0.7)

        origem = eixos.c2p(0, 0)
        theta_v, mag = media_vetorial(angulos)

        setas_in = VGroup()
        for a in angulos:
            setas_in.add(Arrow(
                origem, _ponto_axes(eixos, a, 1.0),
                color=COR_ENTRADA, buff=0, stroke_width=4,
                max_tip_length_to_length_ratio=0.22,
            ))
        self.play(*[GrowArrow(s) for s in setas_in])

        formula = MathTex(
            r"|R| = \sqrt{\bar{u}^{2} + \bar{v}^{2}} = " + f"{mag:.3f}",
            color=COR_VETORIAL, font_size=30,
        ).to_edge(LEFT, buff=0.3).shift(UP * 0.5)
        self.play(Write(formula))

        if mag < 0.05:
            seta_R = Dot(origem, color=COR_VETORIAL, radius=0.14)
            interp = Text("→ sem direção preferencial", font_size=22, color=COR_VETORIAL)
            interp.next_to(formula, DOWN, buff=0.4).align_to(formula, LEFT)
            self.play(FadeIn(seta_R, scale=2), FadeIn(interp))
        else:
            seta_R = Arrow(
                origem, _ponto_axes(eixos, theta_v, 1.0 * mag),
                color=COR_VETORIAL, buff=0, stroke_width=6,
                max_tip_length_to_length_ratio=0.22,
            )
            interp_txt = "→ vetor longo:\n   direções concentradas" if mag > 0.8 \
                else "→ vetor curto:\n   direções dispersas"
            interp = Text(interp_txt, font_size=22, color=COR_VETORIAL, line_spacing=0.9)
            interp.next_to(formula, DOWN, buff=0.4).align_to(formula, LEFT)
            self.play(GrowArrow(seta_R), FadeIn(interp))
        self.wait(2.5)

        self.play(
            FadeOut(titulo), FadeOut(eixos), FadeOut(setas_in),
            FadeOut(seta_R), FadeOut(formula), FadeOut(interp),
        )

    def construct(self):
        intro = Text("Magnitude |R| — medida de consistência", font_size=36).to_edge(UP)
        sub = Text(
            "|R| ≈ 1  →  direções concentradas\n"
            "|R| ≈ 0  →  direções dispersas",
            font_size=24, line_spacing=1.1,
        ).next_to(intro, DOWN, buff=0.6)
        self.play(Write(intro), FadeIn(sub))
        self.wait(1.5)
        self.play(FadeOut(intro), FadeOut(sub))

        self._caso([0, 5, 355, 10], "Caso concentrado: 0°, 5°, 355°, 10°")
        self._caso([0, 90, 180, 270], "Caso disperso: 0°, 90°, 180°, 270°")


# ==================== CENA 6 ====================
class Cena6_Ponderacao(Scene):
    def construct(self):
        titulo = Text("Média vetorial ponderada por velocidade", font_size=34).to_edge(UP)
        self.play(Write(titulo))

        formula = MathTex(
            r"\bar{u} = \frac{\sum_i V_i\sin\theta_i}{\sum_i V_i}"
            r"\qquad "
            r"\bar{v} = \frac{\sum_i V_i\cos\theta_i}{\sum_i V_i}",
            font_size=34,
        ).next_to(titulo, DOWN, buff=0.5)
        self.play(Write(formula))
        self.wait(1)

        medicoes = [(5.0, 350.0), (10.0, 10.0), (2.0, 180.0)]
        tabela_linhas = [
            "i   V_i (m/s)   θ_i",
            "1   5.0          350°",
            "2  10.0           10°",
            "3   2.0          180°",
        ]
        tabela = VGroup(
            *[Text(t, font="Monospace", font_size=24) for t in tabela_linhas]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        tabela.next_to(formula, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        self.play(FadeIn(tabela, shift=UP * 0.2))

        theta_v, mag = media_vetorial(
            [m[1] for m in medicoes], pesos=[m[0] for m in medicoes]
        )
        pesos = np.array([m[0] for m in medicoes])
        angs = np.array([m[1] for m in medicoes])
        u_num = float(np.sum(pesos * np.sin(np.deg2rad(angs))))
        v_num = float(np.sum(pesos * np.cos(np.deg2rad(angs))))
        soma_pesos = float(pesos.sum())

        eixos = Axes(
            x_range=[-1.5, 1.5, 1], y_range=[-1.5, 1.5, 1],
            x_length=3.5, y_length=3.5,
            axis_config={"stroke_color": COR_EIXOS, "stroke_width": 2},
            tips=False,
        ).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.8)
        self.play(Create(eixos), run_time=0.8)

        origem = eixos.c2p(0, 0)
        seta_R = Arrow(
            origem, _ponto_axes(eixos, theta_v, max(mag, 0.2)),
            color=COR_VETORIAL, buff=0, stroke_width=6,
            max_tip_length_to_length_ratio=0.22,
        )

        resultado = VGroup(
            MathTex(r"\sum V_i = " + f"{soma_pesos:.1f}",
                    color=COR_VETORIAL, font_size=28),
            MathTex(r"\bar{u} = \tfrac{" + f"{u_num:.3f}" + r"}{" + f"{soma_pesos:.1f}"
                    r"} = " + f"{u_num/soma_pesos:.3f}",
                    color=COR_VETORIAL, font_size=26),
            MathTex(r"\bar{v} = \tfrac{" + f"{v_num:.3f}" + r"}{" + f"{soma_pesos:.1f}"
                    r"} = " + f"{v_num/soma_pesos:.3f}",
                    color=COR_VETORIAL, font_size=26),
            MathTex(r"\bar{\theta} = " + f"{theta_v:.2f}°"
                    r",\; |R| = " + f"{mag:.3f}",
                    color=COR_VETORIAL, font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        resultado.next_to(tabela, DOWN, buff=0.4).align_to(tabela, LEFT)

        for linha in resultado:
            self.play(Write(linha), run_time=0.7)
        self.play(GrowArrow(seta_R))
        self.wait(3)

        self.play(
            FadeOut(titulo), FadeOut(formula), FadeOut(tabela),
            FadeOut(resultado), FadeOut(eixos), FadeOut(seta_R),
        )


# ==================== CENA 7 ====================
class Cena7_Resumo(Scene):
    def construct(self):
        titulo = Text("Resumo", font_size=44).to_edge(UP)
        self.play(Write(titulo))

        item_x = Text(
            "✗  Média aritmética: FALHA na descontinuidade 360° / 0°",
            font_size=28, color=COR_ARITMETICA,
        )
        item_check = Text(
            "✓  Média vetorial: correta, consistente, significativa",
            font_size=28, color=COR_VETORIAL,
        )
        checklist = VGroup(item_x, item_check).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        checklist.next_to(titulo, DOWN, buff=0.8)
        self.play(FadeIn(item_x, shift=LEFT * 0.3))
        self.wait(0.4)
        self.play(FadeIn(item_check, shift=LEFT * 0.3))
        self.wait(0.6)

        aplic_titulo = Text("Aplicações", font_size=32).next_to(checklist, DOWN, buff=0.7)
        aplic = VGroup(
            Text("• Anemômetros", font_size=26),
            Text("• Correntes oceânicas", font_size=26),
            Text("• Marés", font_size=26),
            Text("• Navegação", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        aplic.next_to(aplic_titulo, DOWN, buff=0.3)

        self.play(Write(aplic_titulo))
        self.play(FadeIn(aplic, lag_ratio=0.15), run_time=1.5)
        self.wait(3)

        self.play(
            FadeOut(titulo), FadeOut(checklist),
            FadeOut(aplic_titulo), FadeOut(aplic),
        )
