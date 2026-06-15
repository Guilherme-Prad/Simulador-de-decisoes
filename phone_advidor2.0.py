import customtkinter as ctk
import json
import os
from dataclasses import dataclass, asdict
from typing import Optional
import threading
import math


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

COLORS = {
    "bg_dark":     "#0D0F14",
    "bg_card":     "#161B27",
    "bg_surface":  "#1E2535",
    "accent":      "#4F9CF9",
    "accent2":     "#7C3AED",
    "accent3":     "#10B981",
    "danger":      "#EF4444",
    "warning":     "#F59E0B",
    "text_primary":"#F1F5F9",
    "text_muted":  "#64748B",
    "border":      "#2D3748",
    "gold":        "#F59E0B",
}

PROFILES_FILE = os.path.join(os.path.dirname(__file__), "profiles.json")


PHONES = [
    {
        "name": "iPhone 16 Pro Max",
        "brand": "Apple",
        "price": 12999,
        "cpu": "A18 Pro",
        "cpu_score": 99,
        "camera": 98,
        "battery": 88,
        "storage_max": 1024,
        "ram": 8,
        "display": '6.9" OLED 120Hz ProMotion',
        "gaming": 98,
        "os": "iOS 18",
        "best_for": ["profissional", "conteudo", "fotos"],
        "highlights": [
            "Chip A18 Pro mais poderoso do mercado",
            "Camera principal 48MP com tetraprism 5x",
            "Gravação de vídeo 4K 120fps ProRes",
            "Display ProMotion LTPO 1–120Hz",
            "Apple Intelligence com IA generativa",
        ],
        "weaknesses": ["Sem expansão de armazenamento", "Preço elevado", "Sem carregamento rápido acima de 30W"],
        "image_emoji": "📱",
    },
    {
        "name": "Samsung Galaxy S25 Ultra",
        "brand": "Samsung",
        "price": 11999,
        "cpu": "Snapdragon 8 Elite",
        "cpu_score": 97,
        "camera": 97,
        "battery": 89,
        "storage_max": 1024,
        "ram": 12,
        "display": '6.9" Dynamic AMOLED 2X 120Hz',
        "gaming": 97,
        "os": "Android 15 / One UI 7",
        "best_for": ["profissional", "conteudo", "fotos", "jogos"],
        "highlights": [
            "Snapdragon 8 Elite top de linha",
            "Camera 200MP + zoom periscópio 5x",
            "S Pen integrada para produtividade",
            "Bateria 5000mAh com carregamento 45W",
            "Galaxy AI para edição e resumos",
        ],
        "weaknesses": ["Preço alto", "Software pesado", "S Pen pode ser desnecessária"],
        "image_emoji": "📲",
    },
    {
        "name": "Google Pixel 9 Pro XL",
        "brand": "Google",
        "price": 9999,
        "cpu": "Google Tensor G4",
        "cpu_score": 85,
        "camera": 99,
        "battery": 87,
        "storage_max": 1024,
        "ram": 16,
        "display": '6.8" LTPO OLED 120Hz',
        "gaming": 78,
        "os": "Android 15 puro",
        "best_for": ["fotos", "profissional", "conteudo"],
        "highlights": [
            "Melhor camera computacional do mundo",
            "IA Google com Gemini integrado",
            "7 anos de atualizações garantidas",
            "Modo astrofotografia único",
            "Funcionalidades Magic Eraser, Best Take",
        ],
        "weaknesses": ["Tensor G4 inferior em gaming", "Ecossistema menor que Apple/Samsung", "Preço premium"],
        "image_emoji": "📸",
    },
    {
        "name": "OnePlus 13",
        "brand": "OnePlus",
        "price": 5999,
        "cpu": "Snapdragon 8 Elite",
        "cpu_score": 97,
        "camera": 82,
        "battery": 97,
        "storage_max": 512,
        "ram": 16,
        "display": '6.82" LTPO AMOLED 120Hz',
        "gaming": 96,
        "os": "OxygenOS 15 / Android 15",
        "best_for": ["jogos", "profissional"],
        "highlights": [
            "Snapdragon 8 Elite com refrigeração vapor",
            "Bateria 6000mAh + carregamento 100W",
            "Carregamento sem fio 50W",
            "UX limpa e rápida OxygenOS",
            "Melhor custo-benefício topo de linha",
        ],
        "weaknesses": ["Camera mediana para o preço", "Marca menos conhecida no Brasil", "Pós-venda limitado"],
        "image_emoji": "⚡",
    },
    {
        "name": "Xiaomi 15 Ultra",
        "brand": "Xiaomi",
        "price": 9499,
        "cpu": "Snapdragon 8 Elite",
        "cpu_score": 97,
        "camera": 96,
        "battery": 92,
        "storage_max": 1024,
        "ram": 16,
        "display": '6.73" LTPO AMOLED 120Hz',
        "gaming": 96,
        "os": "HyperOS 2 / Android 15",
        "best_for": ["fotos", "jogos", "conteudo"],
        "highlights": [
            "Parceria Leica para cameras profissionais",
            "Bateria 5500mAh com carregamento 90W",
            "Camera principal 1 polegada Sony LYT-900",
            "Zoom óptico 5x periscópio Leica",
            "Carregamento sem fio 80W + inverso 10W",
        ],
        "weaknesses": ["MIUI/HyperOS carregado de apps", "Suporte pós-venda no BR limitado", "Updates mais lentos"],
        "image_emoji": "🔭",
    },
    {
        "name": "Samsung Galaxy S25+",
        "brand": "Samsung",
        "price": 7999,
        "cpu": "Snapdragon 8 Elite",
        "cpu_score": 97,
        "camera": 90,
        "battery": 85,
        "storage_max": 512,
        "ram": 12,
        "display": '6.7" Dynamic AMOLED 2X 120Hz',
        "gaming": 95,
        "os": "Android 15 / One UI 7",
        "best_for": ["profissional", "jogos", "estudos"],
        "highlights": [
            "Snapdragon 8 Elite ao melhor preço Samsung",
            "Design mais fino e leve que o Ultra",
            "Ecosystem Samsung perfeito (Watch, Buds, TV)",
            "Galaxy AI embarcado",
            "7 anos de atualizações de segurança",
        ],
        "weaknesses": ["Bateria menor que concorrentes", "Sem S Pen", "Camera inferior ao Ultra"],
        "image_emoji": "💼",
    },
    {
        "name": "iPhone 16",
        "brand": "Apple",
        "price": 7499,
        "cpu": "A18",
        "cpu_score": 95,
        "camera": 90,
        "battery": 85,
        "storage_max": 512,
        "ram": 8,
        "display": '6.1" OLED 60Hz',
        "gaming": 94,
        "os": "iOS 18",
        "best_for": ["estudos", "profissional", "fotos"],
        "highlights": [
            "Chip A18 com Neural Engine avançado",
            "Camera com botão Camera Control",
            "Melhor tela OLED compacta",
            "Apple Intelligence e Siri avançada",
            "Ecossistema Apple completo",
        ],
        "weaknesses": ["Tela 60Hz (não ProMotion)", "Bateria modesta", "Preço alto para 60Hz"],
        "image_emoji": "🍎",
    },
    {
        "name": "Motorola Edge 50 Pro",
        "brand": "Motorola",
        "price": 3499,
        "cpu": "Snapdragon 7s Gen 3",
        "cpu_score": 72,
        "camera": 75,
        "battery": 90,
        "storage_max": 512,
        "ram": 12,
        "display": '6.7" pOLED 144Hz',
        "gaming": 70,
        "os": "Android 14 / Hello UI",
        "best_for": ["estudos", "jogos"],
        "highlights": [
            "Tela pOLED 144Hz curva premium",
            "Carregamento TurboPower 125W ultra rápido",
            "Design fino e elegante",
            "Boa experiência Android puro",
            "Preço acessível para tela OLED",
        ],
        "weaknesses": ["CPU mediocre para gaming pesado", "Camera inconsistente", "Poucas atualizações garantidas"],
        "image_emoji": "🏎️",
    },
    {
        "name": "Realme GT 7 Pro",
        "brand": "Realme",
        "price": 4999,
        "cpu": "Snapdragon 8 Elite",
        "cpu_score": 97,
        "camera": 78,
        "battery": 88,
        "storage_max": 512,
        "ram": 16,
        "display": '6.78" AMOLED 120Hz',
        "gaming": 97,
        "os": "Realme UI 6 / Android 15",
        "best_for": ["jogos"],
        "highlights": [
            "Snapdragon 8 Elite ao menor preço do mercado",
            "Sistema de resfriamento VC avançado",
            "Bateria 6500mAh enorme",
            "Ideal para gaming extremo",
            "RAM 16GB + armazenamento UFS 4.0",
        ],
        "weaknesses": ["Camera abaixo do esperado", "Software com muitos apps desnecessários", "Pouco suporte no BR"],
        "image_emoji": "🎮",
    },
    {
        "name": "Samsung Galaxy A55 5G",
        "brand": "Samsung",
        "price": 2399,
        "cpu": "Exynos 1480",
        "cpu_score": 60,
        "camera": 72,
        "battery": 82,
        "storage_max": 256,
        "ram": 8,
        "display": '6.6" Super AMOLED 120Hz',
        "gaming": 58,
        "os": "Android 14 / One UI 6.1",
        "best_for": ["estudos"],
        "highlights": [
            "Tela Super AMOLED brilhante",
            "4 anos de atualizações Android",
            "Design premium com Gorilla Glass Victus",
            "Bateria 5000mAh confiável",
            "Marca com boa assistência técnica no BR",
        ],
        "weaknesses": ["CPU mediana", "Camera sem recursos avançados", "Sem 5G em todas frequências"],
        "image_emoji": "📚",
    },
    {
        "name": "Poco X7 Pro",
        "brand": "Xiaomi/Poco",
        "price": 2999,
        "cpu": "MediaTek Dimensity 8400 Ultra",
        "cpu_score": 85,
        "camera": 70,
        "battery": 88,
        "storage_max": 512,
        "ram": 12,
        "display": '6.67" AMOLED 120Hz',
        "gaming": 86,
        "os": "HyperOS / Android 15",
        "best_for": ["jogos", "estudos"],
        "highlights": [
            "Dimensity 8400 Ultra excelente para jogos",
            "Bateria 6000mAh com carregamento 90W",
            "Tela AMOLED de alta qualidade",
            "Custo-benefício excepcional para gaming",
            "Armazenamento UFS 4.0 veloz",
        ],
        "weaknesses": ["Camera básica", "Software com anúncios", "Sem NFC em alguns modelos"],
        "image_emoji": "🕹️",
    },
    {
        "name": "Samsung Galaxy Z Fold 6",
        "brand": "Samsung",
        "price": 19999,
        "cpu": "Snapdragon 8 Gen 3",
        "cpu_score": 94,
        "camera": 88,
        "battery": 78,
        "storage_max": 1024,
        "ram": 12,
        "display": '7.6" Dynamic AMOLED 2X (interno) / 6.3" (externo)',
        "gaming": 92,
        "os": "Android 15 / One UI 7",
        "best_for": ["profissional", "estudos", "conteudo"],
        "highlights": [
            "Tela dobrável 7.6\" única no mercado",
            "Multitarefa real com janelas lado a lado",
            "S Pen compatível para notas e desenho",
            "Design premium e durável IPX8",
            "Galaxy AI avançado para produtividade",
        ],
        "weaknesses": ["Bateria ruim para o tamanho", "Preço altíssimo", "Espessura quando dobrado"],
        "image_emoji": "📋",
    },
]

USE_CASES = {
    "estudos": {
        "label": "🎓 Estudos",
        "desc": "Leitura, aulas online, anotações e organização",
        "weights": {"camera": 0.1, "battery": 0.35, "gaming": 0.05, "cpu_score": 0.25, "storage": 0.25},
        "priority_text": "Bateria duradoura e armazenamento para apps e materiais são essenciais.",
    },
    "profissional": {
        "label": "💼 Uso Profissional",
        "desc": "E-mails, videoconferências, multitarefa e produtividade",
        "weights": {"camera": 0.2, "battery": 0.25, "gaming": 0.05, "cpu_score": 0.3, "storage": 0.2},
        "priority_text": "CPU potente para multitarefa e bateria confiável são prioridades.",
    },
    "conteudo": {
        "label": "🎬 Produção de Conteúdo",
        "desc": "Fotos, vídeos, reels e streaming",
        "weights": {"camera": 0.45, "battery": 0.2, "gaming": 0.05, "cpu_score": 0.2, "storage": 0.1},
        "priority_text": "Camera de alta qualidade é o fator mais importante.",
    },
    "jogos": {
        "label": "🎮 Games",
        "desc": "Jogos pesados, streaming de jogos e esports",
        "weights": {"camera": 0.05, "battery": 0.2, "gaming": 0.55, "cpu_score": 0.15, "storage": 0.05},
        "priority_text": "Desempenho em jogos e bateria para longas sessões são cruciais.",
    },
}


def score_phone(phone: dict, use_case: str, max_price: int) -> float:
    if phone["price"] > max_price:
        return -1
    w = USE_CASES[use_case]["weights"]
    storage_score = min(100, phone["storage_max"] / 10.24)
    raw = (
        w["camera"]    * phone["camera"]
        + w["battery"] * phone["battery"]
        + w["gaming"]  * phone["gaming"]
        + w["cpu_score"] * phone["cpu_score"]
        + w["storage"] * storage_score
    )
   
    if use_case in phone["best_for"]:
        raw *= 1.12
  
    price_ratio = 1 - (phone["price"] / 20000) * 0.15
    return raw * price_ratio


def rank_phones(use_case: str, max_price: int, filters: dict) -> list:
    scored = []
    for p in PHONES:
        s = score_phone(p, use_case, max_price)
        if s < 0:
            continue
        if filters.get("min_storage") and p["storage_max"] < filters["min_storage"]:
            continue
        scored.append((s, p))
    scored.sort(reverse=True, key=lambda x: x[0])
    return scored



def load_profiles():
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_profiles(profiles):
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)



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
    def __init__(self, master, rank: int, score: float, phone: dict, use_case: str, on_detail, **kw):
        super().__init__(master, fg_color=COLORS["bg_card"], corner_radius=16,
                         border_width=1,
                         border_color=COLORS["accent"] if rank == 1 else COLORS["border"], **kw)
        self.phone = phone
        self.use_case = use_case
        self.on_detail = on_detail
        self._build(rank, score)

    def _build(self, rank, score):
        pad = dict(padx=16, pady=4)

        # Header
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=16, pady=(14, 4))

        badge_color = (COLORS["gold"] if rank == 1 else
                       COLORS["text_muted"] if rank > 2 else COLORS["accent3"])
        badge_text = f"#{rank}"
        ctk.CTkLabel(hdr, text=badge_text, font=("Inter", 13, "bold"),
                     text_color=badge_color, fg_color=COLORS["bg_surface"],
                     corner_radius=8, width=34, height=24).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(hdr, text=self.phone["image_emoji"] + "  " + self.phone["name"],
                     font=("Inter", 15, "bold"),
                     text_color=COLORS["text_primary"]).pack(side="left")

        price_label = f"R$ {self.phone['price']:,.0f}".replace(",", ".")
        ctk.CTkLabel(hdr, text=price_label, font=("Inter", 14, "bold"),
                     text_color=COLORS["accent3"]).pack(side="right")

   
        ctk.CTkFrame(self, fg_color=COLORS["border"], height=1).pack(fill="x", padx=16, pady=(4, 8))

  
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
        why_bg = ctk.CTkFrame(self, fg_color=COLORS["bg_surface"], corner_radius=10)
        why_bg.pack(fill="x", padx=16, pady=(4, 8))
        uc = USE_CASES[self.use_case]
        reason = self._why(score)
        ctk.CTkLabel(why_bg, text=f"✅  {reason}", font=("Inter", 12),
                     text_color=COLORS["text_primary"], wraplength=480,
                     justify="left", anchor="w").pack(padx=12, pady=8, anchor="w")

 
        foot = ctk.CTkFrame(self, fg_color="transparent")
        foot.pack(fill="x", padx=16, pady=(0, 12))
        ctk.CTkLabel(foot, text=f"{self.phone['cpu']}  ·  {self.phone['os']}  ·  até {self.phone['storage_max']}GB",
                     font=("Inter", 11), text_color=COLORS["text_muted"]).pack(side="left")
        ctk.CTkButton(foot, text="Ver detalhes →", width=110, height=28,
                      font=("Inter", 12), corner_radius=8,
                      fg_color=COLORS["bg_dark"], hover_color=COLORS["accent"],
                      border_width=1, border_color=COLORS["accent"],
                      command=lambda: self.on_detail(self.phone, self.use_case)).pack(side="right")

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
        self._build(phone, use_case)

    def _build(self, p, uc):
    
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

 
        section("✅ Pontos Fortes")
        for h in p["highlights"]:
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.pack(fill="x", pady=1)
            ctk.CTkLabel(row, text="▸", text_color=COLORS["accent3"],
                         font=("Inter", 13)).pack(side="left", padx=(4, 8))
            ctk.CTkLabel(row, text=h, font=("Inter", 12),
                         text_color=COLORS["text_primary"], anchor="w").pack(side="left")


        section("⚠️ Limitações")
        for w in p["weaknesses"]:
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.pack(fill="x", pady=1)
            ctk.CTkLabel(row, text="▸", text_color=COLORS["warning"],
                         font=("Inter", 13)).pack(side="left", padx=(4, 8))
            ctk.CTkLabel(row, text=w, font=("Inter", 12),
                         text_color=COLORS["text_muted"], anchor="w").pack(side="left")

        
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

        self._build_layout()
        self._run_search()

   
    def _build_layout(self):
        
        self.sidebar = ctk.CTkFrame(self, fg_color=COLORS["bg_card"], width=270, corner_radius=0)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)
        self._build_sidebar()

  
        self.content = ctk.CTkFrame(self, fg_color=COLORS["bg_dark"], corner_radius=0)
        self.content.pack(side="left", fill="both", expand=True)
        self._build_content()

    def _build_sidebar(self):
      
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color=COLORS["bg_dark"], corner_radius=0)
        logo_frame.pack(fill="x", pady=0)
        ctk.CTkLabel(logo_frame, text="📱 PhoneAdvisor",
                     font=("Inter", 17, "bold"), text_color=COLORS["accent"]).pack(pady=16, padx=20, anchor="w")
        ctk.CTkLabel(logo_frame, text="Encontre o celular ideal para você",
                     font=("Inter", 11), text_color=COLORS["text_muted"]).pack(padx=20, anchor="w", pady=(0, 12))

        ctk.CTkFrame(self.sidebar, fg_color=COLORS["border"], height=1).pack(fill="x")

        scroll = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent", scrollbar_button_color=COLORS["border"])
        scroll.pack(fill="both", expand=True)

   
        self._section_label(scroll, "👤 Perfil")
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
                      command=self._save_profile_dialog).pack(side="left", padx=4)

  
        self._section_label(scroll, "🎯 Uso Principal")
        for key, info in USE_CASES.items():
            btn = ctk.CTkRadioButton(
                scroll, text=info["label"],
                variable=self.use_case_var, value=key,
                font=("Inter", 12), text_color=COLORS["text_primary"],
                fg_color=COLORS["accent"], border_color=COLORS["border"],
                command=self._run_search
            )
            btn.pack(anchor="w", padx=16, pady=3)

        ctk.CTkLabel(scroll, textvariable=ctk.StringVar(), text="",
                     height=4).pack()  


        self._section_label(scroll, "💰 Orçamento Máximo")
        self.price_label = ctk.CTkLabel(scroll, text="R$ 8.000",
                                        font=("Inter", 16, "bold"), text_color=COLORS["accent3"])
        self.price_label.pack(pady=(0, 4))
        ctk.CTkSlider(scroll, from_=500, to=20000, variable=self.price_var,
                      button_color=COLORS["accent"], button_hover_color=COLORS["accent2"],
                      progress_color=COLORS["accent"], command=self._on_price).pack(
            padx=16, fill="x")
        hint_row = ctk.CTkFrame(scroll, fg_color="transparent")
        hint_row.pack(fill="x", padx=16)
        ctk.CTkLabel(hint_row, text="R$ 500", font=("Inter", 10),
                     text_color=COLORS["text_muted"]).pack(side="left")
        ctk.CTkLabel(hint_row, text="R$ 20.000", font=("Inter", 10),
                     text_color=COLORS["text_muted"]).pack(side="right")

       
        self._section_label(scroll, "💾 Armazenamento Mínimo")
        storage_opts = ["Qualquer", "128 GB", "256 GB", "512 GB", "1 TB"]
        ctk.CTkOptionMenu(
            scroll, values=storage_opts,
            variable=self.min_storage_var,
            fg_color=COLORS["bg_surface"], button_color=COLORS["accent"],
            dropdown_fg_color=COLORS["bg_card"],
            font=("Inter", 12),
            command=lambda _: self._run_search()
        ).pack(padx=16, fill="x", pady=4)

      
        ctk.CTkButton(
            scroll, text="🔍  Buscar Celulares",
            font=("Inter", 13, "bold"), height=42, corner_radius=12,
            fg_color=COLORS["accent"], hover_color=COLORS["accent2"],
            command=self._run_search
        ).pack(padx=16, pady=16, fill="x")

     
        ctk.CTkButton(
            scroll, text="⚖️  Comparar Top 3",
            font=("Inter", 12), height=36, corner_radius=12,
            fg_color=COLORS["bg_surface"], hover_color=COLORS["accent"],
            border_width=1, border_color=COLORS["accent"],
            command=self._open_compare
        ).pack(padx=16, pady=(0, 16), fill="x")

    def _section_label(self, parent, text):
        ctk.CTkLabel(parent, text=text, font=("Inter", 12, "bold"),
                     text_color=COLORS["text_muted"]).pack(anchor="w", padx=16, pady=(14, 4))

    def _build_content(self):
     
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

     
        self.results_frame = ctk.CTkScrollableFrame(
            self.content, fg_color="transparent",
            scrollbar_button_color=COLORS["border"]
        )
        self.results_frame.pack(fill="both", expand=True, padx=16, pady=16)


    def _on_price(self, val):
        v = int(val)
        formatted = f"R$ {v:,.0f}".replace(",", ".")
        self.price_label.configure(text=formatted)
        self._run_search()

    def _run_search(self, *_):
        use_case = self.use_case_var.get()
        max_price = int(self.price_var.get())
        storage_str = self.min_storage_var.get()
        min_storage = 0
        if "128" in storage_str:
            min_storage = 128
        elif "256" in storage_str:
            min_storage = 256
        elif "512" in storage_str:
            min_storage = 512
        elif "1 TB" in storage_str:
            min_storage = 1024

        results = rank_phones(use_case, max_price, {"min_storage": min_storage})
        self.last_results = results

       
        for w in self.results_frame.winfo_children():
            w.destroy()

        uc_info = USE_CASES[use_case]
        self.result_title.configure(text=f"Melhores para {uc_info['label']}")
        self.result_count.configure(text=f"{len(results)} celular(es) encontrado(s)")

        if not results:
            ctk.CTkLabel(self.results_frame, text="😕 Nenhum celular encontrado com esses critérios.\nAumente o orçamento ou ajuste os filtros.",
                         font=("Inter", 14), text_color=COLORS["text_muted"],
                         justify="center").pack(expand=True, pady=60)
            return

        for i, (score, phone) in enumerate(results[:8], 1):
            card = PhoneCard(self.results_frame, i, score, phone, use_case,
                             on_detail=self._open_detail)
            card.pack(fill="x", pady=6)

        
        info_frame = ctk.CTkFrame(self.results_frame, fg_color=COLORS["bg_surface"],
                                  corner_radius=10)
        info_frame.pack(fill="x", pady=8)
        ctk.CTkLabel(info_frame,
                     text=f"💡 {uc_info['priority_text']}",
                     font=("Inter", 12), text_color=COLORS["text_muted"],
                     wraplength=640, justify="left").pack(padx=16, pady=10, anchor="w")

    def _open_detail(self, phone, use_case):
        DetailWindow(self, phone, use_case)

    def _open_compare(self):
        results = getattr(self, "last_results", [])
        if not results:
            return
        top3 = [p for _, p in results[:3]]
        if len(top3) < 2:
            return
        CompareWindow(self, top3)


    def _save_profile_dialog(self):
        dialog = ctk.CTkInputDialog(text="Nome do perfil:", title="Salvar Perfil")
        name = dialog.get_input()
        if not name or not name.strip():
            return
        name = name.strip()
        self.profiles[name] = {
            "use_case": self.use_case_var.get(),
            "max_price": int(self.price_var.get()),
            "min_storage": self.min_storage_var.get(),
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
            self.min_storage_var.set(p.get("min_storage", "Qualquer"))
            self._on_price(self.price_var.get())



class CompareWindow(ctk.CTkToplevel):
    def __init__(self, master, phones: list):
        super().__init__(master)
        self.title("⚖️ Comparativo de Celulares")
        self.geometry("860x620")
        self.configure(fg_color=COLORS["bg_dark"])
        self.resizable(True, True)
        self._build(phones)

    def _build(self, phones):
        ctk.CTkLabel(self, text="⚖️  Comparativo — Top 3",
                     font=("Inter", 18, "bold"), text_color=COLORS["text_primary"]).pack(pady=(20, 4))
        ctk.CTkLabel(self, text="Análise lado a lado dos melhores celulares para seu perfil",
                     font=("Inter", 12), text_color=COLORS["text_muted"]).pack(pady=(0, 16))

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

     
        hdr = ctk.CTkFrame(scroll, fg_color=COLORS["bg_card"], corner_radius=12)
        hdr.pack(fill="x", pady=(0, 4))
        ctk.CTkLabel(hdr, text="Critério", font=("Inter", 12, "bold"),
                     text_color=COLORS["text_muted"], width=150, anchor="w").grid(row=0, column=0, padx=14, pady=10)
        colors_list = [COLORS["gold"], COLORS["accent3"], COLORS["accent"]]
        for i, phone in enumerate(phones):
            ctk.CTkLabel(hdr, text=f"#{i+1}  {phone['image_emoji']} {phone['name']}",
                         font=("Inter", 12, "bold"), text_color=colors_list[i],
                         width=195, anchor="center").grid(row=0, column=i+1, padx=6, pady=10)

       
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
                             text_color=color, width=195, anchor="center").grid(
                    row=0, column=j+1, padx=6, pady=8)


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



if __name__ == "__main__":
    app = PhoneAdvisorApp()
    app.mainloop()
