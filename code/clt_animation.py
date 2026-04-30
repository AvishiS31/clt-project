"""
Central Limit Theorem Animation
Seeing Theory Reference: https://seeing-theory.brown.edu/probability-distributions/
Storyline: Non-normal populations → Sampling → Histogram forms → CLT formula → Probability

Run:
    manim -pql clt_animation.py CLTFullAnimation   # fast preview
    manim -pqh clt_animation.py CLTFullAnimation   # high quality
"""

from manim import *
import numpy as np
from scipy.stats import norm as scipy_norm

# ── colour palette ────────────────────────────────────────────────────────────
UNIFORM_COLOR = BLUE
EXP_COLOR     = GREEN
BIMODAL_COLOR = ORANGE
SAMPLE_COLOR  = YELLOW
HIST_COLOR    = TEAL
NORMAL_COLOR  = RED
SHADE_COLOR   = BLUE


class CLTFullAnimation(Scene):

    def construct(self):
        self.s1_non_normal_distributions()
        self.s2_sampling_from_population()
        self.s3_histogram_forming()
        self.s4_clt_formula()
        self.s5_probability_application()

    def clear_all(self, run_time=0.7):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)

    # ═══════════════════════════════════════════════════════════════════════════
    # SCENE 1 — Non-normal distributions
    # ═══════════════════════════════════════════════════════════════════════════
    def s1_non_normal_distributions(self):

        title = Text("Populations Are Not Always Normal",
                     font_size=40, color=WHITE).to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1.0)
        self.wait(0.3)

        # three axes spaced so they never overlap
        ax1 = Axes(
            x_range=[0, 1, 0.5], y_range=[0, 2.5, 1],
            x_length=3.0, y_length=2.2,
            axis_config={"color": GRAY, "stroke_width": 1.5,
                         "tip_length": 0.12},
        ).shift(LEFT * 4.0 + DOWN * 0.6)

        ax2 = Axes(
            x_range=[0, 1, 0.5], y_range=[0, 2.5, 1],
            x_length=3.0, y_length=2.2,
            axis_config={"color": GRAY, "stroke_width": 1.5,
                         "tip_length": 0.12},
        ).shift(ORIGIN + DOWN * 0.6)

        ax3 = Axes(
            x_range=[0, 5, 1], y_range=[0, 1.2, 0.5],
            x_length=3.0, y_length=2.2,
            axis_config={"color": GRAY, "stroke_width": 1.5,
                         "tip_length": 0.12},
        ).shift(RIGHT * 4.0 + DOWN * 0.6)

        # Uniform
        unif_curve = ax1.plot(lambda x: 1.0,
                              x_range=[0, 1], color=UNIFORM_COLOR,
                              stroke_width=3)
        unif_area  = ax1.get_area(unif_curve, x_range=[0, 1],
                                  color=UNIFORM_COLOR, opacity=0.3)
        unif_lbl   = Text("Uniform", font_size=22, color=UNIFORM_COLOR
                          ).next_to(ax1, UP, buff=0.12)

        # Bimodal
        def bimodal(x):
            return (2.0 * np.exp(-((x - 0.25) ** 2) / 0.006)
                    + 2.0 * np.exp(-((x - 0.75) ** 2) / 0.006))

        bim_curve  = ax2.plot(bimodal, x_range=[0.001, 0.999],
                              color=BIMODAL_COLOR, stroke_width=3)
        bim_area   = ax2.get_area(bim_curve, x_range=[0.001, 0.999],
                                  color=BIMODAL_COLOR, opacity=0.3)
        bim_lbl    = Text("Bimodal", font_size=22, color=BIMODAL_COLOR
                          ).next_to(ax2, UP, buff=0.12)

        # Exponential (skewed)
        exp_curve  = ax3.plot(lambda x: np.exp(-x),
                              x_range=[0.001, 5], color=EXP_COLOR,
                              stroke_width=3)
        exp_area   = ax3.get_area(exp_curve, x_range=[0.001, 5],
                                  color=EXP_COLOR, opacity=0.3)
        exp_lbl    =Text("Skewed", font="Arial", font_size=22, color=EXP_COLOR).next_to(ax3, UP, buff=0.12)

        note = Text("None of these are Normal distributions.",
                    font_size=26, color=YELLOW).to_edge(DOWN, buff=0.35)

        self.play(
            Create(ax1), Create(ax2), Create(ax3),
            Write(unif_lbl), Write(bim_lbl), Write(exp_lbl),
            run_time=0.8,
        )
        self.play(Create(unif_curve), FadeIn(unif_area), run_time=0.7)
        self.play(Create(bim_curve),  FadeIn(bim_area),  run_time=0.7)
        self.play(Create(exp_curve),  FadeIn(exp_area),  run_time=0.7)
        self.play(Write(note))
        self.wait(2.5)
        self.clear_all()

    # ═══════════════════════════════════════════════════════════════════════════
    # SCENE 2 — Sampling from a population
    # ═══════════════════════════════════════════════════════════════════════════
    def s2_sampling_from_population(self):
        np.random.seed(0)
        rng = np.random.default_rng(1)

        title = Text("Taking Random Samples", font_size=40, color=WHITE
                     ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # population circle — left side
        pop_center = LEFT * 3.2 + DOWN * 0.5
        pop_circle = Circle(radius=2.0, color=BLUE, fill_opacity=0.12,
                            stroke_width=2.5).move_to(pop_center)
        pop_lbl    = Text("Population", font_size=26, color=BLUE
                          ).next_to(pop_circle, UP, buff=0.15)

        # scatter dots inside population circle
        pop_dots = VGroup()
        while len(pop_dots) < 55:
            x, y = rng.uniform(-1.7, 1.7), rng.uniform(-1.7, 1.7)
            if x**2 + y**2 < 1.6**2:
                pop_dots.add(
                    Dot(pop_center + np.array([x, y, 0]),
                        radius=0.07, color=WHITE, fill_opacity=0.5)
                )

        self.play(Create(pop_circle), Write(pop_lbl))
        self.play(FadeIn(pop_dots), run_time=0.7)

        # sample circle — right side
        samp_center  = RIGHT * 3.2 + DOWN * 0.5
        samp_circle  = Circle(radius=1.0, color=SAMPLE_COLOR,
                              fill_opacity=0.12, stroke_width=2.5
                              ).move_to(samp_center)
        samp_lbl     = Text("Sample  (n = 10)", font_size=22,
                            color=SAMPLE_COLOR).next_to(samp_circle, UP, buff=0.15)

        self.play(Create(samp_circle), Write(samp_lbl))

        # arrow between circles
        arrow = Arrow(pop_circle.get_right(), samp_circle.get_left(),
                      buff=0.1, color=WHITE, stroke_width=2.5,
                      max_tip_length_to_length_ratio=0.15)
        arr_lbl = Text("random\nsample", font_size=18, color=GRAY,
                       line_spacing=1.2).next_to(arrow, UP, buff=0.1)
        self.play(Create(arrow), Write(arr_lbl))

        # formula — placed below sample circle so nothing overlaps
        formula = MathTex(
            r"\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i",
            font_size=40,
        ).next_to(samp_circle, DOWN, buff=0.55)
        f_box = SurroundingRectangle(formula, color=SAMPLE_COLOR,
                                     buff=0.18, corner_radius=0.1)
        self.play(Write(formula), Create(f_box))

        # animate 4 sampling rounds
        xbar_mobj = Text("", font_size=1)
        self.add(xbar_mobj)

        for _ in range(4):
            chosen_idx = rng.choice(len(pop_dots), size=10, replace=False)
            chosen     = VGroup(*[pop_dots[i] for i in chosen_idx])

            self.play(chosen.animate.set_color(SAMPLE_COLOR).scale(1.5),
                      run_time=0.25)

            s_dots = VGroup(*[
                Dot(samp_center + np.append(rng.uniform(-0.65, 0.65, 2), 0),
                    radius=0.09, color=SAMPLE_COLOR)
                for _ in range(10)
            ])
            fake_xbar = round(rng.uniform(0.7, 1.3), 3)
            new_xbar  = Text(f"x̄ = {fake_xbar}", font_size=22, color=YELLOW
                             ).next_to(samp_circle, RIGHT, buff=0.4)

            self.play(
                FadeIn(s_dots),
                chosen.animate.set_color(WHITE).scale(1 / 1.5),
                Transform(xbar_mobj, new_xbar),
                run_time=0.35,
            )
            self.wait(0.3)
            self.play(FadeOut(s_dots), run_time=0.2)

        self.wait(1.5)
        self.clear_all()

    # ═══════════════════════════════════════════════════════════════════════════
    # SCENE 3 — Histogram forming over time
    # ═══════════════════════════════════════════════════════════════════════════
    def s3_histogram_forming(self):
        np.random.seed(42)
        N_TOTAL = 200
        N_PER   = 30
        BINS    = 22

        title = Text("Sample Means Form a Normal Distribution",
                     font_size=36, color=WHITE).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax = Axes(
            x_range=[0.3, 1.7, 0.2], y_range=[0, 55, 10],
            x_length=9.0, y_length=4.4,
            axis_config={"color": WHITE, "stroke_width": 1.5},
            x_axis_config={"numbers_to_include": np.round(np.arange(0.4, 1.7, 0.2), 1)},
            y_axis_config={"numbers_to_include": np.arange(0, 56, 10)},
        ).shift(DOWN * 0.5)

        x_lbl = Text("Sample Mean  x̄", font_size=20, color=GRAY
                     ).next_to(ax, DOWN, buff=0.15)
        y_lbl = Text("Count", font_size=20, color=GRAY
                     ).next_to(ax.get_left(), LEFT, buff=0.1)

        self.play(Create(ax), Write(x_lbl), Write(y_lbl))

        counter   = Text("Samples drawn: 0", font_size=24, color=YELLOW
                         ).to_corner(UR).shift(LEFT * 0.4 + DOWN * 1.3)
        note_mobj = VMobject()   # invisible placeholder
        self.add(counter, note_mobj)

        all_means = np.random.uniform(0, 2, size=(N_TOTAL, N_PER)).mean(axis=1)
        bin_edges = np.linspace(0.3, 1.7, BINS + 1)
        bw        = bin_edges[1] - bin_edges[0]

        milestones = {
            10:  ("Still very jagged...",        ORANGE),
            50:  ("Smoother now...",              ORANGE),
            100: ("Starting to look Normal!",     GREEN),
            200: ("Bell curve!  CLT in action!",  GREEN),
        }

        bars = VMobject()
        self.add(bars)

        schedule = (
            [(1,  0.20)] * 10
            + [(2,  0.14)] * 10
            + [(5,  0.10)] * 8
            + [(10, 0.09)] * 8
            + [(20, 0.12)] * 4
            + [(10, 0.18)] * 2
        )

        idx = 0
        for (batch, rt) in schedule:
            if idx >= N_TOTAL:
                break
            idx = min(idx + batch, N_TOTAL)

            counts, _ = np.histogram(all_means[:idx], bins=bin_edges)

            new_bars = VGroup()
            for i, c in enumerate(counts):
                if c == 0:
                    continue
                bx    = bin_edges[i]
                bar_h = ax.y_axis.n2p(c)[1] - ax.y_axis.n2p(0)[1]
                bar_w = ax.x_axis.n2p(bx + bw)[0] - ax.x_axis.n2p(bx)[0]
                new_bars.add(
                    Rectangle(
                        width=bar_w, height=max(bar_h, 0.01),
                        fill_color=HIST_COLOR, fill_opacity=0.75,
                        stroke_color=WHITE, stroke_width=0.5,
                    ).move_to(ax.c2p(bx + bw / 2, c / 2))
                )

            new_counter = Text(f"Samples drawn: {idx}", font_size=24,
                               color=YELLOW
                               ).to_corner(UR).shift(LEFT * 0.4 + DOWN * 1.3)

            anims = [Transform(bars, new_bars),
                     Transform(counter, new_counter)]

            if idx in milestones:
                text, col = milestones[idx]
                new_note  = Text(text, font_size=26, color=col
                                 ).to_edge(DOWN, buff=0.35).shift(UP * 5.5)
                anims.append(Transform(note_mobj, new_note))

            self.play(*anims, run_time=rt)

        # overlay fitted normal curve
        mu_e = all_means.mean()
        se_e = all_means.std()
        norm_curve = ax.plot(
            lambda x: N_TOTAL * bw
            * (1 / (se_e * np.sqrt(2 * np.pi)))
            * np.exp(-0.5 * ((x - mu_e) / se_e) ** 2),
            x_range=[0.35, 1.65],
            color=NORMAL_COLOR, stroke_width=3.5,
        )
        self.play(Create(norm_curve), run_time=1.5)
        self.wait(2.5)
        self.clear_all()

    # ═══════════════════════════════════════════════════════════════════════════
    # SCENE 4 — CLT formula + explanation
    # ═══════════════════════════════════════════════════════════════════════════
    def s4_clt_formula(self):

        title = Text("The Central Limit Theorem",
                     font_size=42, color=WHITE).to_edge(UP, buff=0.35)
        self.play(Write(title))

        # main formula — centered, not too large
        formula = MathTex(
            r"\bar{X} \;\sim\; \mathcal{N}\!\left(\mu,\;"
            r"\frac{\sigma^2}{n}\right)"
            r"\quad \text{as } n \to \infty",
            font_size=46,
        ).shift(UP * 1.2)
        box = SurroundingRectangle(formula, color=NORMAL_COLOR,
                                   buff=0.28, corner_radius=0.12)
        self.play(Write(formula), run_time=1.4)
        self.play(Create(box))
        self.wait(0.4)

        # legend rows — placed below formula with plenty of spacing
        entries = [
            (r"\bar{X}",  "= sample mean",              SAMPLE_COLOR),
            (r"\mu",       "= population mean",           BLUE),
            (r"\sigma^2",  "= population variance",       GREEN),
            (r"n",         "= sample size  (larger is better)", ORANGE),
        ]

        legend = VGroup()
        for tex, desc, col in entries:
            row = VGroup(
                MathTex(tex, font_size=32, color=col),
                Text(desc, font_size=24, color=col),
            ).arrange(RIGHT, buff=0.25)
            legend.add(row)

        legend.arrange(DOWN, buff=0.28, aligned_edge=LEFT
                       ).next_to(formula, DOWN, buff=0.55)

        for row in legend:
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.4)
            self.wait(0.08)

        summary = Text(
            "No matter the population shape,\n"
            "sample means become Normally distributed as n grows.",
            font_size=25, color=YELLOW, line_spacing=1.35,
        ).to_edge(DOWN, buff=0.3)
        self.play(Write(summary), run_time=1.2)
        self.wait(3.0)
        self.clear_all()

    # ═══════════════════════════════════════════════════════════════════════════
    # SCENE 5 — Bell curve, shaded area, probability expression
    # ═══════════════════════════════════════════════════════════════════════════
    def s5_probability_application(self):

        title = Text("Using the CLT: Finding Probabilities",
                     font_size=38, color=WHITE).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # axes for standard normal — leave room at right for formula
        ax = Axes(
            x_range=[-3.5, 3.5, 1], y_range=[0, 0.46, 0.1],
            x_length=7.5, y_length=4.0,
            axis_config={"color": WHITE, "stroke_width": 1.5},
            x_axis_config={"numbers_to_include": np.arange(-3, 4, 1)},
        ).shift(LEFT * 1.5 + DOWN * 0.5)

        self.play(Create(ax))

        def phi(x):
            return np.exp(-x**2 / 2) / np.sqrt(2 * np.pi)

        curve = ax.plot(phi, x_range=[-3.5, 3.5],
                        color=WHITE, stroke_width=2.5)
        self.play(Create(curve), run_time=0.9)

        # a and b
        a, b = -1.0, 1.5

        line_a = ax.get_vertical_line(ax.c2p(a, phi(a)),
                                      color=SAMPLE_COLOR,
                                      line_func=DashedLine,
                                      stroke_width=2.5)
        line_b = ax.get_vertical_line(ax.c2p(b, phi(b)),
                                      color=SAMPLE_COLOR,
                                      line_func=DashedLine,
                                      stroke_width=2.5)
        lbl_a  = MathTex("a", font_size=30, color=SAMPLE_COLOR
                         ).next_to(ax.c2p(a, 0), DOWN, buff=0.2)
        lbl_b  = MathTex("b", font_size=30, color=SAMPLE_COLOR
                         ).next_to(ax.c2p(b, 0), DOWN, buff=0.2)

        self.play(Create(line_a), Create(line_b),
                  Write(lbl_a), Write(lbl_b), run_time=0.8)

        shade = ax.get_area(curve, x_range=[a, b],
                            color=SHADE_COLOR, opacity=0.45)
        self.play(FadeIn(shade), run_time=0.9)

        # formula — right column, will not overlap axes
        prob_expr = MathTex(
            r"P(a \leq \bar{X} \leq b)",
            r"= \int_{a}^{b} \phi\!\left(\frac{x-\mu}{\sigma/\sqrt{n}}\right)"
            r"\frac{dx}{\sigma/\sqrt{n}}",
            font_size=28,
        ).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)
        prob_box = SurroundingRectangle(prob_expr, color=SHADE_COLOR,
                                        buff=0.2, corner_radius=0.1)

        self.play(Write(prob_expr), Create(prob_box), run_time=1.5)

        # numeric example
        prob_val   = scipy_norm.cdf(b) - scipy_norm.cdf(a)
        num_example = VGroup(
            MathTex(r"a = -1,\quad b = 1.5", font_size=26, color=SAMPLE_COLOR),
            MathTex(rf"P \approx {prob_val:.4f}", font_size=30, color=YELLOW),
        ).arrange(DOWN, buff=0.2).next_to(prob_expr, DOWN, buff=0.35)

        self.play(FadeIn(num_example), run_time=0.8)


        self.wait(3.5)
        self.clear_all()

        # closing card
        end = Text("Central Limit Theorem", font_size=50, color=WHITE)
        sub = Text("Regardless of the original distribution, \n" \
        "predictions, confidence intervals, and \n" \
        "hypothesis tests can be made. ",
                   font_size=28, color=GRAY).next_to(end, DOWN, buff=0.4)
        self.play(Write(end), FadeIn(sub))
        self.wait(3)
        self.play(FadeOut(end), FadeOut(sub))
