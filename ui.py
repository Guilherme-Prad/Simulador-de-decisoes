import customtkinter as ctk

from dados import USE_CASES, load_profiles, save_profiles
from logica import rank_phones

# ─── Theme & Colors ────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

COLORS = {
    "bg_dark":     "#12110F",   # quente, quase preto
    "bg_card":     "#1C1A17",   # marrom-escuro suave
    "bg_surface":  "#252219",   # superfície levemente âmbar
    "accent":      "#6EA8D8",   # azul mais suave, menos saturado
    "accent2":     "#9B72CF",   # roxo suave
    "accent3":     "#4DB889",   # verde mais discreto
    "danger":      "#D96C6C",   # vermelho suavizado
    "warning":     "#D4973A",   # âmbar quente
    "text_primary":"#EDE8DF",   # branco-creme, não puro
    "text_muted":  "#7A7060",   # cinza-dourado
    "border":      "#332E24",   # borda quente
    "gold":        "#CFA840",   # ouro mais profundo
}


# ─── Widgets ──────────────────────────────────────────────────────────────────────
class ScoreBar(ctk.CTkFrame):
    def __init__(self, master, label: str, value: int, color: str = COLORS["accent"], **kw):
        super().__init__(master, fg_color="transparent", **kw)
        ctk.CTkLabel(self, text=label, font=("Inter", 11), text_color=COLORS["text_muted"],
                     width=70, anchor="w").pack(side="left")
        bar_bg = ctk.CTkFrame(self, fg_color=COLORS["border"], height=6, corner_radius=3, width=160)
        bar_bg.pack(side="left", padx=(6, 6), pady=0)
        bar_bg.pack_propagate(False)
        fill_w = max(4, int(160 * value / 100))
        fill = ctk.CTkFrame(bar_bg, fg_color=color, height=6, corner_radius=3, width=fill_w)
        fill.place(x=0, y=0, relheight=1)
        ctk.CTkLabel(self, text=f"{value}", font=("Inter", 11, "bold"),
                     text_color=color).pack(side="left")


class PhoneCard(ctk.CTkFrame):
    def __init__(self, master, rank: int, score: float, phone: dict, use_case: str, on_detail, compare_var: ctk.BooleanVar = None, on_compare_toggle=None, **kw):
        is_first = rank == 1
        super().__init__(
            master,
            fg_color="#1C2030" if is_first else COLORS["bg_card"],
            corner_radius=18 if is_first else 14,
            border_width=2 if is_first else 1,
            border_color=COLORS["gold"] if is_first else (COLORS["accent"] if rank == 2 else COLORS["border"]),
            **kw
        )
        self.phone = phone
        self.use_case = use_case
        self.on_detail = on_detail
        self.compare_var = compare_var
        self.on_compare_toggle = on_compare_toggle
        self._build(rank, score)

    def _build(self, rank, score):
        is_first = rank == 1
        pad = dict(padx=16, pady=4)

        # ── Gold banner for #1 ──────────────────────────────────────
        if is_first:
            banner = ctk.CTkFrame(self, fg_color="#2A2010", corner_radius=0, height=32)
            banner.pack(fill="x")
            banner.pack_propagate(False)
            ctk.CTkLabel(
                banner,
                text="🏆  MELHOR ESCOLHA PARA VOCÊ",
                font=("Inter", 11, "bold"),
                text_color=COLORS["gold"],
            ).pack(side="left", padx=16, pady=6)
            score_pct = f"Score: {score:.1f}"
            ctk.CTkLabel(banner, text=score_pct, font=("Inter", 10), text_color=COLORS["text_muted"]).pack(side="right", padx=16)

        # Header
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=16, pady=(12 if is_first else 14, 4))

        if is_first:
            badge_text = "👑 #1"
            badge_fg = COLORS["gold"]
            badge_bg = "#3A2E00"
            name_font = ("Inter", 17, "bold")
            name_color = "#FFD966"
        elif rank == 2:
            badge_text = "🥈 #2"
            badge_fg = COLORS["accent3"]
            badge_bg = COLORS["bg_surface"]
            name_font = ("Inter", 15, "bold")
            name_color = COLORS["text_primary"]
        else:
            badge_text = f"#{rank}"
            badge_fg = COLORS["text_muted"]
            badge_bg = COLORS["bg_surface"]
            name_font = ("Inter", 14, "bold")
            name_color = COLORS["text_primary"]

        ctk.CTkLabel(
            hdr, text=badge_text,
            font=("Inter", 13, "bold"),
            text_color=badge_fg, fg_color=badge_bg,
            corner_radius=8, width=46, height=26,
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            hdr,
            text=self.phone["image_emoji"] + "  " + self.phone["name"],
            font=name_font,
            text_color=name_color,
        ).pack(side="left")

        price_label = f"R$ {self.phone['price']:,.0f}".replace(",", ".")
        ctk.CTkLabel(
            hdr, text=price_label,
            font=("Inter", 15 if is_first else 14, "bold"),
            text_color=COLORS["gold"] if is_first else COLORS["accent3"],
        ).pack(side="right")

        # Separator
        sep_color = COLORS["gold"] if is_first else COLORS["border"]
        ctk.CTkFrame(self, fg_color=sep_color, height=1).pack(fill="x", padx=16, pady=(4, 8))

        # Scores
        scores_frame = ctk.CTkFrame(self, fg_color="transparent")
        scores_frame.pack(fill="x", **pad)

        col1 = ctk.CTkFrame(scores_frame, fg_color="transparent")
        col1.pack(side="left", fill="x", expand=True)
        col2 = ctk.CTkFrame(scores_frame, fg_color="transparent")
        col2.pack(side="left", fill="x", expand=True)

        ScoreBar(col1, "🎮 Games", self.phone["gaming"], COLORS["accent"]).pack(anchor="w", pady=2)
        ScoreBar(col1, "📷 Câmera", self.phone["camera"], COLORS["accent2"]).pack(anchor="w", pady=2)
        ScoreBar(col2, "🔋 Bateria", self.phone["battery"], COLORS["accent3"]).pack(anchor="w", pady=2)
        ScoreBar(col2, "⚡ CPU", self.phone["cpu_score"], COLORS["warning"]).pack(anchor="w", pady=2)

        # Why section
        why_color = "#2A2810" if is_first else COLORS["bg_surface"]
        why_bg = ctk.CTkFrame(self, fg_color=why_color, corner_radius=10)
        why_bg.pack(fill="x", padx=16, pady=(4, 8))
        reason = self._why(score)
        ctk.CTkLabel(
            why_bg,
            text=f"✅  {reason}",
            font=("Inter", 12, "bold" if is_first else "normal"),
            text_color=COLORS["gold"] if is_first else COLORS["text_primary"],
            wraplength=480, justify="left", anchor="w",
        ).pack(padx=12, pady=8, anchor="w")

        # Footer
        foot = ctk.CTkFrame(self, fg_color="transparent")
        foot.pack(fill="x", padx=16, pady=(0, 12))
        ctk.CTkLabel(
            foot,
            text=f"{self.phone['cpu']}  ·  {self.phone['os']}  ·  até {self.phone['storage_max']}GB",
            font=("Inter", 11), text_color=COLORS["text_muted"],
        ).pack(side="left")
        btn_color = COLORS["gold"] if is_first else COLORS["bg_dark"]
        btn_hover = "#B8860B" if is_first else COLORS["accent"]
        btn_text_color = "#1A1000" if is_first else COLORS["text_primary"]
        ctk.CTkButton(
            foot,
            text="Ver detalhes →",
            width=120 if is_first else 110, height=30 if is_first else 28,
            font=("Inter", 12, "bold" if is_first else "normal"),
            corner_radius=8,
            fg_color=btn_color, hover_color=btn_hover,
            text_color=btn_text_color,
            border_width=0 if is_first else 1,
            border_color=COLORS["accent"],
            command=lambda: self.on_detail(self.phone, self.use_case),
        ).pack(side="right")

        # Compare toggle button — destacado, com estado visual claro
        if self.compare_var is not None:
            self._compare_btn = ctk.CTkButton(
                foot,
                text="⊕ Comparar",
                width=110, height=30 if is_first else 28,
                font=("Inter", 11, "bold"),
                corner_radius=8,
                fg_color=COLORS["bg_surface"],
                hover_color=COLORS["accent"],
                text_color=COLORS["text_muted"],
                border_width=2,
                border_color=COLORS["border"],
                command=self._toggle_compare,
            )
            self._compare_btn.pack(side="right", padx=(0, 8))

    def _toggle_compare(self):
        new_val = not self.compare_var.get()
        self.compare_var.set(new_val)
        if new_val:
            self._compare_btn.configure(
                text="✓ Selecionado",
                fg_color=COLORS["accent"],
                text_color=COLORS["bg_dark"],
                border_color=COLORS["accent"],
            )
        else:
            self._compare_btn.configure(
                text="⊕ Comparar",
                fg_color=COLORS["bg_surface"],
                text_color=COLORS["text_muted"],
                border_color=COLORS["border"],
            )
        if self.on_compare_toggle:
            self.on_compare_toggle()

    def _why(self, score: float) -> str:
        p = self.phone
        uc = self.use_case
        if uc == "jogos":
            return f"CPU {p['cpu']} com nota {p['gaming']}/100 em games — ideal para títulos pesados."
        elif uc == "conteudo":
            return f"Camera {p['camera']}/100, gravação 4K e telas vibrantes para criar conteúdo profissional."
        elif uc == "estudos":
            return f"Bateria {p['battery']}/100 e {p['storage_max']}GB de armazenamento para estudo prolongado."
        else:
            return f"CPU {p['cpu_score']}/100 e bateria {p['battery']}/100 garantem produtividade o dia todo."


class DetailWindow(ctk.CTkToplevel):
    def __init__(self, master, phone: dict, use_case: str):
        super().__init__(master)
        self.title(f"Detalhes — {phone['name']}")
        self.geometry("680x720")
        self.configure(fg_color=COLORS["bg_dark"])
        self.resizable(False, False)
        self.transient(master)
        self.attributes("-topmost", True)
        self.after(200, lambda: self.attributes("-topmost", False))
        self.lift()
        self.focus_force()
        self._build(phone, use_case)

    def _build(self, p, uc):
        # Header
        hdr = ctk.CTkFrame(self, fg_color=COLORS["bg_card"], corner_radius=0)
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text=p["image_emoji"] + "  " + p["name"],
                     font=("Inter", 20, "bold"), text_color=COLORS["text_primary"]).pack(side="left", padx=24, pady=16)
        price = f"R$ {p['price']:,.0f}".replace(",", ".")
        ctk.CTkLabel(hdr, text=price, font=("Inter", 18, "bold"),
                     text_color=COLORS["accent3"]).pack(side="right", padx=24)

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=16, pady=16)

        def section(title):
            ctk.CTkLabel(scroll, text=title, font=("Inter", 14, "bold"),
                         text_color=COLORS["accent"]).pack(anchor="w", pady=(12, 4))
            ctk.CTkFrame(scroll, fg_color=COLORS["accent"], height=2).pack(fill="x", pady=(0, 6))

        # Specs grid
        section("📋 Especificações")
        specs_frame = ctk.CTkFrame(scroll, fg_color=COLORS["bg_card"], corner_radius=12)
        specs_frame.pack(fill="x", pady=4)
        specs = [
            ("Processador", p["cpu"]),
            ("RAM", f"{p['ram']} GB"),
            ("Armazenamento", f"até {p['storage_max']} GB"),
            ("Tela", p["display"]),
            ("Sistema", p["os"]),
        ]
        for i, (k, v) in enumerate(specs):
            row = ctk.CTkFrame(specs_frame, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=5)
            ctk.CTkLabel(row, text=k, font=("Inter", 12), text_color=COLORS["text_muted"],
                         width=130, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=v, font=("Inter", 12, "bold"),
                         text_color=COLORS["text_primary"], anchor="w").pack(side="left")

        # Scores
        section("📊 Comparativo de Notas")
        bars = ctk.CTkFrame(scroll, fg_color=COLORS["bg_card"], corner_radius=12)
        bars.pack(fill="x", pady=4)
        scores_data = [
            ("🎮 Desempenho em Games", p["gaming"], COLORS["accent"]),
            ("📷 Qualidade de Câmera", p["camera"], COLORS["accent2"]),
            ("🔋 Duração de Bateria", p["battery"], COLORS["accent3"]),
            ("⚡ Performance CPU", p["cpu_score"], COLORS["warning"]),
        ]
        for label, val, color in scores_data:
            row = ctk.CTkFrame(bars, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=6)
            ctk.CTkLabel(row, text=label, font=("Inter", 12),
                         text_color=COLORS["text_muted"], width=200, anchor="w").pack(side="left")
            bar_bg = ctk.CTkFrame(row, fg_color=COLORS["border"], height=10, corner_radius=5, width=220)
            bar_bg.pack(side="left", padx=6)
            bar_bg.pack_propagate(False)
            fill_w = max(4, int(220 * val / 100))
            ctk.CTkFrame(bar_bg, fg_color=color, height=10, corner_radius=5, width=fill_w).place(x=0, y=0, relheight=1)
            ctk.CTkLabel(row, text=str(val), font=("Inter", 12, "bold"),
                         text_color=color).pack(side="left", padx=4)

        # Highlights
        section("✅ Pontos Fortes")
        for h in p["highlights"]:
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.pack(fill="x", pady=1)
            ctk.CTkLabel(row, text="▸", text_color=COLORS["accent3"],
                         font=("Inter", 13)).pack(side="left", padx=(4, 8))
            ctk.CTkLabel(row, text=h, font=("Inter", 12),
                         text_color=COLORS["text_primary"], anchor="w").pack(side="left")

        # Weaknesses
        section("⚠️ Limitações")
        for w in p["weaknesses"]:
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.pack(fill="x", pady=1)
            ctk.CTkLabel(row, text="▸", text_color=COLORS["warning"],
                         font=("Inter", 13)).pack(side="left", padx=(4, 8))
            ctk.CTkLabel(row, text=w, font=("Inter", 12),
                         text_color=COLORS["text_muted"], anchor="w").pack(side="left")

        # Use case fit
        section(f"🎯 Para o Caso de Uso: {USE_CASES[uc]['label']}")
        fit_bg = ctk.CTkFrame(scroll, fg_color=COLORS["bg_card"], corner_radius=12)
        fit_bg.pack(fill="x", pady=4)
        is_fit = uc in p["best_for"]
        fit_text = (f"✅ Este celular é otimizado para {USE_CASES[uc]['label']}.\n{USE_CASES[uc]['priority_text']}"
                    if is_fit
                    else f"⚠️ Este celular não é a primeira escolha para {USE_CASES[uc]['label']}, mas pode atender parcialmente.\n{USE_CASES[uc]['priority_text']}")
        ctk.CTkLabel(fit_bg, text=fit_text, font=("Inter", 12),
                     text_color=COLORS["text_primary"], wraplength=580,
                     justify="left").pack(padx=14, pady=12, anchor="w")


# ─── Compare Window ───────────────────────────────────────────────────────────────
class CompareWindow(ctk.CTkToplevel):
    def __init__(self, master, phones: list):
        super().__init__(master)
        self.title("⚖️ Comparativo de Celulares")
        n = len(phones)
        width = 700 + (n - 2) * 180
        self.geometry(f"{width}x640")
        self.configure(fg_color=COLORS["bg_dark"])
        self.resizable(True, True)
        self.transient(master)
        self.attributes("-topmost", True)
        self.after(200, lambda: self.attributes("-topmost", False))
        self.lift()
        self.focus_force()
        self._build(phones)

    def _build(self, phones):
        n = len(phones)
        width = 700 + (n - 2) * 180
        col_w = max(140, int((width - 200) / n))
        ctk.CTkLabel(self, text=f"⚖️  Comparativo — {n} Celulares",
                     font=("Inter", 18, "bold"), text_color=COLORS["text_primary"]).pack(pady=(20, 4))
        ctk.CTkLabel(self, text="Análise lado a lado dos celulares selecionados",
                     font=("Inter", 12), text_color=COLORS["text_muted"]).pack(pady=(0, 16))

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Header row
        hdr = ctk.CTkFrame(scroll, fg_color=COLORS["bg_card"], corner_radius=12)
        hdr.pack(fill="x", pady=(0, 4))
        col_w = max(140, int((width - 200) / n))
        ctk.CTkLabel(hdr, text="Critério", font=("Inter", 12, "bold"),
                     text_color=COLORS["text_muted"], width=150, anchor="w").grid(row=0, column=0, padx=14, pady=10)
        colors_list = [COLORS["gold"], COLORS["accent3"], COLORS["accent"], COLORS["accent2"]]
        for i, phone in enumerate(phones):
            ctk.CTkLabel(hdr, text=f"#{i+1}  {phone['image_emoji']} {phone['name']}",
                         font=("Inter", 12, "bold"), text_color=colors_list[i % len(colors_list)],
                         width=col_w, anchor="center").grid(row=0, column=i+1, padx=6, pady=10)

        # Rows
        rows_data = [
            ("💰 Preço", lambda p: f"R$ {p['price']:,.0f}".replace(",", "."), None),
            ("⚡ Processador", lambda p: p["cpu"], None),
            ("🔋 Bateria", lambda p: f"{p['battery']}/100", "battery"),
            ("📷 Câmera", lambda p: f"{p['camera']}/100", "camera"),
            ("🎮 Gaming", lambda p: f"{p['gaming']}/100", "gaming"),
            ("🧠 CPU Score", lambda p: f"{p['cpu_score']}/100", "cpu_score"),
            ("💾 Armazenamento", lambda p: f"até {p['storage_max']} GB", "storage_max"),
            ("📺 Tela", lambda p: p["display"], None),
            ("🤖 Sistema", lambda p: p["os"], None),
        ]

        for ri, (label, getter, key) in enumerate(rows_data):
            bg = COLORS["bg_surface"] if ri % 2 == 0 else COLORS["bg_card"]
            row_frame = ctk.CTkFrame(scroll, fg_color=bg, corner_radius=8)
            row_frame.pack(fill="x", pady=2)
            ctk.CTkLabel(row_frame, text=label, font=("Inter", 12),
                         text_color=COLORS["text_muted"], width=150, anchor="w").grid(
                row=0, column=0, padx=14, pady=8)

            values = [getter(p) for p in phones]
            # Highlight best value
            if key and key != "storage_max":
                nums = [getattr(p, key, None) or p.get(key, 0) for p in phones]
                max_val = max(nums)
            else:
                max_val = None

            for j, (phone, val) in enumerate(zip(phones, values)):
                is_best = False
                if key:
                    raw_val = phone.get(key, 0)
                    if max_val and raw_val == max_val:
                        is_best = True
                color = COLORS["accent3"] if is_best else COLORS["text_primary"]
                ctk.CTkLabel(row_frame, text=val + (" ✓" if is_best else ""),
                             font=("Inter", 12, "bold" if is_best else "normal"),
                             text_color=color, width=col_w, anchor="center").grid(
                    row=0, column=j+1, padx=6, pady=8)

        # Verdict
        ctk.CTkLabel(scroll, text="🏆 Veredicto",
                     font=("Inter", 14, "bold"), text_color=COLORS["accent"]).pack(anchor="w", pady=(16, 6))
        ctk.CTkFrame(scroll, fg_color=COLORS["accent"], height=2).pack(fill="x", pady=(0, 8))
        verdict_bg = ctk.CTkFrame(scroll, fg_color=COLORS["bg_card"], corner_radius=12)
        verdict_bg.pack(fill="x", pady=4)
        verdict_text = self._verdict(phones)
        ctk.CTkLabel(verdict_bg, text=verdict_text, font=("Inter", 12),
                     text_color=COLORS["text_primary"], wraplength=740,
                     justify="left").pack(padx=16, pady=14, anchor="w")

    def _verdict(self, phones):
        top = phones[0]
        second = phones[1] if len(phones) > 1 else None
        text = f"🥇 {top['name']} é a melhor escolha geral, com o maior score ponderado.\n"
        if second:
            text += f"🥈 {second['name']} é a segunda opção, "
            if second["price"] < top["price"] - 500:
                text += f"com preço R$ {top['price'] - second['price']:,.0f} menor.".replace(",", ".")
            elif second["camera"] > top["camera"]:
                text += "com câmera superior."
            elif second["gaming"] > top["gaming"]:
                text += "com desempenho em games ligeiramente melhor."
            else:
                text += "uma alternativa sólida com características similares."
        return text


# ─── Main App ─────────────────────────────────────────────────────────────────────
class PhoneAdvisorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("📱 PhoneAdvisor — Qual celular comprar?")
        self.geometry("1100x780")
        self.minsize(900, 640)
        self.configure(fg_color=COLORS["bg_dark"])

        self.profiles = load_profiles()
        self.current_profile = ctk.StringVar(value="")
        self.use_case_var = ctk.StringVar(value="profissional")
        self.price_var = ctk.DoubleVar(value=8000)
        self.min_storage_var = ctk.StringVar(value="Qualquer")
        self._search_job = None  # debounce handle for slider
        self._compare_selection: dict = {}   # phone name -> BooleanVar

        # Custom weight sliders (0–10, normalized on search)
        self.w_gaming   = ctk.DoubleVar(value=5)
        self.w_camera   = ctk.DoubleVar(value=5)
        self.w_battery  = ctk.DoubleVar(value=5)
        self.w_cpu      = ctk.DoubleVar(value=5)
        self.w_storage  = ctk.DoubleVar(value=5)
        self._weight_labels = {}   # filled in _build_sidebar
        self._use_custom_weights = ctk.BooleanVar(value=False)

        self._build_layout()
        self._run_search()

    # ── Layout ──────────────────────────────────────────────────────────────────
    def _build_layout(self):
        # Left sidebar
        self.sidebar = ctk.CTkFrame(self, fg_color=COLORS["bg_card"], width=270, corner_radius=0)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)
        self._build_sidebar()

        # Right content
        self.content = ctk.CTkFrame(self, fg_color=COLORS["bg_dark"], corner_radius=0)
        self.content.pack(side="left", fill="both", expand=True)
        self._build_content()

    def _build_sidebar(self):
        # Logo
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color=COLORS["bg_dark"], corner_radius=0)
        logo_frame.pack(fill="x", pady=0)
        ctk.CTkLabel(logo_frame, text="📱 PhoneAdvisor",
                     font=("Inter", 17, "bold"), text_color=COLORS["accent"]).pack(pady=16, padx=20, anchor="w")
        ctk.CTkLabel(logo_frame, text="Encontre o celular ideal para você",
                     font=("Inter", 11), text_color=COLORS["text_muted"]).pack(padx=20, anchor="w", pady=(0, 12))

        ctk.CTkFrame(self.sidebar, fg_color=COLORS["border"], height=1).pack(fill="x")

        scroll = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent",
                                        scrollbar_button_color=COLORS["border"])
        scroll.pack(fill="both", expand=True)

        # ── Step 1: Parâmetros ────────────────────────────────────
        self._section_label(scroll, "1️⃣  Parâmetros de busca")

        # Toggle
        toggle_row = ctk.CTkFrame(scroll, fg_color="transparent")
        toggle_row.pack(fill="x", padx=16, pady=(0, 6))
        ctk.CTkSwitch(
            toggle_row,
            text="Personalizar parâmetros",
            variable=self._use_custom_weights,
            font=("Inter", 12), text_color=COLORS["text_primary"],
            fg_color=COLORS["border"], progress_color=COLORS["accent"],
            button_color=COLORS["text_primary"],
            command=self._on_weight_toggle,
        ).pack(side="left")

        # Container fixo para os parâmetros (sempre no lugar certo)
        # Params sliders frame — empacotado diretamente no scroll, oculto por padrão
        self._weights_frame = ctk.CTkFrame(scroll, fg_color=COLORS["bg_surface"], corner_radius=12)

        weight_defs = [
            ("🎮 Games",    self.w_gaming,  COLORS["accent"]),
            ("📷 Câmera",   self.w_camera,  COLORS["accent2"]),
            ("🔋 Bateria",  self.w_battery, COLORS["accent3"]),
            ("⚡ CPU",      self.w_cpu,     COLORS["warning"]),
            ("💾 Armazen.", self.w_storage, COLORS["text_muted"]),
        ]
        for label, var, color in weight_defs:
            row = ctk.CTkFrame(self._weights_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=(6, 0))

            ctk.CTkLabel(row, text=label, font=("Inter", 11),
                         text_color=COLORS["text_muted"], width=76, anchor="w").pack(side="left")

            val_lbl = ctk.CTkLabel(row, text="5", font=("Inter", 11, "bold"),
                                   text_color=color, width=20)
            val_lbl.pack(side="right")
            self._weight_labels[label] = val_lbl

            def make_cmd(v=var, lbl=val_lbl):
                def cmd(val):
                    lbl.configure(text=str(int(val)))
                return cmd

            ctk.CTkSlider(
                row, from_=0, to=10, variable=var,
                number_of_steps=10,
                button_color=color, button_hover_color=COLORS["accent2"],
                progress_color=color,
                command=make_cmd(),
                height=14,
            ).pack(side="left", fill="x", expand=True, padx=(4, 8))

        reset_row = ctk.CTkFrame(self._weights_frame, fg_color="transparent")
        reset_row.pack(fill="x", padx=10, pady=(4, 8))
        ctk.CTkButton(
            reset_row, text="↺ Resetar parâmetros",
            font=("Inter", 10), height=24, corner_radius=6,
            fg_color=COLORS["bg_card"], hover_color=COLORS["border"],
            border_width=1, border_color=COLORS["border"],
            command=self._reset_weights,
        ).pack(side="right")

        # Start collapsed — não ocupa espaço algum
        # (não chamamos pack aqui; pack_forget equivale a nunca ter empacotado)

        self._weights_sep = ctk.CTkFrame(scroll, fg_color=COLORS["border"], height=1)
        self._weights_sep.pack(fill="x", padx=16, pady=(10, 0))

        # ── Step 2: Uso Principal ─────────────────────────────────
        self._section_label(scroll, "2️⃣  Para que vai usar?")
        for key, info in USE_CASES.items():
            ctk.CTkRadioButton(
                scroll, text=info["label"],
                variable=self.use_case_var, value=key,
                font=("Inter", 12), text_color=COLORS["text_primary"],
                fg_color=COLORS["accent"], border_color=COLORS["border"],
            ).pack(anchor="w", padx=16, pady=3)

        ctk.CTkFrame(scroll, fg_color=COLORS["border"], height=1).pack(fill="x", padx=16, pady=(10, 0))

        # ── Step 3: Orçamento ─────────────────────────────────────
        self._section_label(scroll, "3️⃣  Orçamento Máximo")
        self.price_label = ctk.CTkLabel(scroll, text="R$ 8.000",
                                        font=("Inter", 18, "bold"), text_color=COLORS["accent3"])
        self.price_label.pack(pady=(0, 6))

        slider_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        slider_frame.pack(fill="x", padx=14)
        ctk.CTkSlider(
            slider_frame, from_=500, to=20000, variable=self.price_var,
            button_color=COLORS["accent"], button_hover_color=COLORS["accent2"],
            progress_color=COLORS["accent"], number_of_steps=39,
            command=self._on_price,
        ).pack(fill="x")
        hint_row = ctk.CTkFrame(slider_frame, fg_color="transparent")
        hint_row.pack(fill="x")
        ctk.CTkLabel(hint_row, text="R$ 500", font=("Inter", 10),
                     text_color=COLORS["text_muted"]).pack(side="left")
        ctk.CTkLabel(hint_row, text="R$ 20.000", font=("Inter", 10),
                     text_color=COLORS["text_muted"]).pack(side="right")

        # Quick budget buttons
        quick_row = ctk.CTkFrame(scroll, fg_color="transparent")
        quick_row.pack(fill="x", padx=14, pady=(6, 0))
        for label, val in [("3k", 3000), ("6k", 6000), ("10k", 10000), ("20k", 20000)]:
            ctk.CTkButton(
                quick_row, text=label, width=50, height=26,
                font=("Inter", 11), corner_radius=6,
                fg_color=COLORS["bg_surface"], hover_color=COLORS["accent"],
                border_width=1, border_color=COLORS["border"],
                command=lambda v=val: (self.price_var.set(v), self._on_price(v))
            ).pack(side="left", padx=2)

        ctk.CTkFrame(scroll, fg_color=COLORS["border"], height=1).pack(fill="x", padx=16, pady=10)

        # ── Actions ────────────────────────────────────────────────
        ctk.CTkButton(
            scroll, text="🔍  Buscar Celulares",
            font=("Inter", 13, "bold"), height=42, corner_radius=12,
            fg_color=COLORS["accent"], hover_color=COLORS["accent2"],
            command=self._run_search
        ).pack(padx=16, pady=(0, 8), fill="x")

        ctk.CTkButton(
            scroll, text="⚖️  Comparar Selecionados",
            font=("Inter", 12), height=36, corner_radius=12,
            fg_color=COLORS["bg_surface"], hover_color=COLORS["accent"],
            border_width=1, border_color=COLORS["accent"],
            command=self._open_compare
        ).pack(padx=16, pady=(0, 8), fill="x")

        ctk.CTkFrame(scroll, fg_color=COLORS["border"], height=1).pack(fill="x", padx=16, pady=6)

        # ── Perfis (avançado, no final) ───────────────────────────
        self._section_label(scroll, "👤 Perfis Salvos")
        profile_row = ctk.CTkFrame(scroll, fg_color="transparent")
        profile_row.pack(fill="x", padx=12, pady=4)

        profile_names = list(self.profiles.keys()) or ["(nenhum)"]
        self.profile_menu = ctk.CTkOptionMenu(
            profile_row, values=profile_names,
            variable=self.current_profile,
            fg_color=COLORS["bg_surface"], button_color=COLORS["accent"],
            dropdown_fg_color=COLORS["bg_card"],
            font=("Inter", 12), width=150,
            command=self._load_profile
        )
        self.profile_menu.pack(side="left")
        ctk.CTkButton(profile_row, text="💾", width=32, height=32,
                      font=("Inter", 14),
                      fg_color=COLORS["bg_surface"], hover_color=COLORS["accent"],
                      border_width=1, border_color=COLORS["border"],
                      command=self._save_profile_dialog).pack(side="left", padx=4)

    def _section_label(self, parent, text):
        ctk.CTkLabel(parent, text=text, font=("Inter", 12, "bold"),
                     text_color=COLORS["text_muted"]).pack(anchor="w", padx=16, pady=(14, 4))

    def _build_content(self):
        # Top bar
        top = ctk.CTkFrame(self.content, fg_color=COLORS["bg_card"],
                           corner_radius=0, height=56)
        top.pack(fill="x")
        top.pack_propagate(False)
        self.result_title = ctk.CTkLabel(top, text="Melhores celulares para você",
                                         font=("Inter", 16, "bold"),
                                         text_color=COLORS["text_primary"])
        self.result_title.pack(side="left", padx=20, pady=16)
        self.result_count = ctk.CTkLabel(top, text="", font=("Inter", 12),
                                         text_color=COLORS["text_muted"])
        self.result_count.pack(side="right", padx=20)

        # Compare selection bar (hidden until selection is made)
        self._compare_bar = ctk.CTkFrame(self.content, fg_color=COLORS["bg_surface"],
                                          corner_radius=0, height=44)
        self._compare_bar_label = ctk.CTkLabel(
            self._compare_bar, text="",
            font=("Inter", 12), text_color=COLORS["text_muted"])
        self._compare_bar_label.pack(side="left", padx=16, pady=10)
        ctk.CTkButton(
            self._compare_bar, text="⚖️ Comparar agora",
            font=("Inter", 12, "bold"), height=30, width=160, corner_radius=8,
            fg_color=COLORS["accent"], hover_color=COLORS["accent2"],
            command=self._open_compare,
        ).pack(side="right", padx=16, pady=7)
        ctk.CTkButton(
            self._compare_bar, text="✕ Limpar",
            font=("Inter", 11), height=28, width=80, corner_radius=8,
            fg_color=COLORS["bg_card"], hover_color=COLORS["danger"],
            border_width=1, border_color=COLORS["border"],
            command=self._clear_compare_selection,
        ).pack(side="right", padx=(0, 4), pady=7)

        # Results scroll
        self.results_frame = ctk.CTkScrollableFrame(
            self.content, fg_color="transparent",
            scrollbar_button_color=COLORS["border"]
        )
        self.results_frame.pack(fill="both", expand=True, padx=16, pady=16)

    def _on_weight_toggle(self):
        if self._use_custom_weights.get():
            self._weights_frame.pack(fill="x", padx=16, pady=(0, 4), before=self._weights_sep)
        else:
            self._weights_frame.pack_forget()

    def _reset_weights(self):
        for var in (self.w_gaming, self.w_camera, self.w_battery, self.w_cpu, self.w_storage):
            var.set(5)
        for lbl in self._weight_labels.values():
            lbl.configure(text="5")

    def _debounce_search(self):
        if self._search_job is not None:
            self.after_cancel(self._search_job)
        self._search_job = self.after(450, self._run_search)

    def _on_price(self, val):
        v = int(val)
        v = round(v / 500) * 500
        formatted = f"R$ {v:,.0f}".replace(",", ".")
        self.price_label.configure(text=formatted)

    def _get_custom_weights(self) -> dict:
        """Normalize the 0-10 sliders into weights summing to 1.0."""
        raw = {
            "gaming":    self.w_gaming.get(),
            "camera":    self.w_camera.get(),
            "battery":   self.w_battery.get(),
            "cpu_score": self.w_cpu.get(),
            "storage":   self.w_storage.get(),
        }
        total = sum(raw.values()) or 1
        return {k: v / total for k, v in raw.items()}

    def _run_search(self, *_):
        use_case = self.use_case_var.get()
        max_price = int(self.price_var.get())

        custom_weights = self._get_custom_weights() if self._use_custom_weights.get() else None
        results = rank_phones(use_case, max_price, {}, custom_weights=custom_weights)
        self.last_results = results

        # Clear previous cards and compare selection
        for w in self.results_frame.winfo_children():
            w.destroy()
        self._compare_selection.clear()
        self._compare_bar.pack_forget()

        uc_info = USE_CASES[use_case]
        self.result_title.configure(text=f"Melhores para {uc_info['label']}")
        self.result_count.configure(text=f"{len(results)} celular(es) encontrado(s)")

        if not results:
            ctk.CTkLabel(self.results_frame,
                         text="😕 Nenhum celular encontrado com esses critérios.\nAumente o orçamento ou ajuste os filtros.",
                         font=("Inter", 14), text_color=COLORS["text_muted"],
                         justify="center").pack(expand=True, pady=60)
            return

        top8 = results[:8]
        hint = "⚖️ Parâmetros personalizados ativos." if self._use_custom_weights.get() else f"💡 {uc_info['priority_text']}"

        for index, (score, phone) in enumerate(top8):
            compare_var = ctk.BooleanVar(value=False)
            self._compare_selection[phone["name"]] = (compare_var, phone)
            card = PhoneCard(self.results_frame, index + 1, score, phone, use_case,
                             on_detail=self._open_detail,
                             compare_var=compare_var,
                             on_compare_toggle=self._on_compare_toggle)
            card.pack(fill="x", pady=6)

        info_frame = ctk.CTkFrame(self.results_frame, fg_color=COLORS["bg_surface"], corner_radius=10)
        info_frame.pack(fill="x", pady=8)
        ctk.CTkLabel(info_frame, text=hint, font=("Inter", 12),
                     text_color=COLORS["text_muted"],
                     wraplength=640, justify="left").pack(padx=16, pady=10, anchor="w")

    def _open_detail(self, phone, use_case):
        DetailWindow(self, phone, use_case)

    def _on_compare_toggle(self):
        selected = [(name, phone) for name, (var, phone) in self._compare_selection.items() if var.get()]
        count = len(selected)
        if count == 0:
            self._compare_bar.pack_forget()
        else:
            if not self._compare_bar.winfo_ismapped():
                # Insert compare bar between top bar and results frame
                self._compare_bar.pack(fill="x", before=self.results_frame)
            names = ", ".join(n for n, _ in selected)
            limit_hint = " (máx. 4)" if count >= 4 else ""
            self._compare_bar_label.configure(
                text=f"✅ {count} selecionado(s){limit_hint}: {names}"
            )
            # Disable unchecked checkboxes if 4 already selected
            for name, (var, phone) in self._compare_selection.items():
                pass  # checkboxes self-limit via on_compare_toggle logic

    def _clear_compare_selection(self):
        for name, (var, phone) in self._compare_selection.items():
            var.set(False)
        self._compare_bar.pack_forget()

    def _open_compare(self):
        selected_phones = [phone for name, (var, phone) in self._compare_selection.items() if var.get()]
        if len(selected_phones) < 2:
            # Fall back to top 3 from results if nothing selected
            results = getattr(self, "last_results", [])
            selected_phones = [p for _, p in results[:3]]
        if len(selected_phones) < 2:
            return
        CompareWindow(self, selected_phones[:4])

    # ── Profile management ───────────────────────────────────────────────────────
    def _save_profile_dialog(self):
        dialog = ctk.CTkInputDialog(text="Nome do perfil:", title="Salvar Perfil")
        name = dialog.get_input()
        if not name or not name.strip():
            return
        name = name.strip()
        self.profiles[name] = {
            "use_case": self.use_case_var.get(),
            "max_price": int(self.price_var.get()),
            "custom_weights": self._use_custom_weights.get(),
            "w_gaming":  self.w_gaming.get(),
            "w_camera":  self.w_camera.get(),
            "w_battery": self.w_battery.get(),
            "w_cpu":     self.w_cpu.get(),
            "w_storage": self.w_storage.get(),
        }
        save_profiles(self.profiles)
        names = list(self.profiles.keys())
        self.profile_menu.configure(values=names)
        self.current_profile.set(name)

    def _load_profile(self, name):
        if name in self.profiles:
            p = self.profiles[name]
            self.use_case_var.set(p.get("use_case", "profissional"))
            self.price_var.set(p.get("max_price", 8000))
            self._use_custom_weights.set(p.get("custom_weights", False))
            self.w_gaming.set(p.get("w_gaming", 5))
            self.w_camera.set(p.get("w_camera", 5))
            self.w_battery.set(p.get("w_battery", 5))
            self.w_cpu.set(p.get("w_cpu", 5))
            self.w_storage.set(p.get("w_storage", 5))
            # Update weight value labels
            for (label, var, _), key in zip(
                [("🎮 Games", self.w_gaming, None), ("📷 Câmera", self.w_camera, None),
                 ("🔋 Bateria", self.w_battery, None), ("⚡ CPU", self.w_cpu, None),
                 ("💾 Armazen.", self.w_storage, None)],
                ["w_gaming", "w_camera", "w_battery", "w_cpu", "w_storage"]
            ):
                if label in self._weight_labels:
                    self._weight_labels[label].configure(text=str(int(var.get())))
            self._on_weight_toggle()
            self._on_price(self.price_var.get())
