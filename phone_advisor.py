import customtkinter as ctk
import json
import os
import math
from datetime import datetime
import threading


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PROFILES_FILE = "phone_profiles.json"


PHONES_DB = [
    {
        "name": "iPhone 15 Pro Max",
        "brand": "Apple",
        "price": 9999,
        "specs": {
            "processor": "Apple A17 Pro",
            "processor_score": 98,
            "camera_mp": 48,
            "camera_score": 97,
            "battery_mah": 4422,
            "battery_score": 82,
            "storage_gb": 256,
            "ram_gb": 8,
            "display": "6.7\" Super Retina XDR OLED 120Hz",
            "weight_g": 221,
            "os": "iOS 17",
            "5g": True,
        },
        "use_scores": {"jogos": 96, "estudos": 90, "profissional": 95, "conteudo": 98},
        "highlights": [
            "Melhor câmera de smartphone do mercado",
            "Chip A17 Pro ultrapotente para jogos AAA",
            "Titanium design premium e durável",
            "ProRes video 4K para criadores profissionais",
            "Ecossistema Apple integrado",
        ],
        "pros": ["Câmera excepcional", "Performance líder mundial", "Build premium", "Suporte iOS longo prazo"],
        "cons": ["Preço elevado", "Bateria mediana para o tamanho", "Sem carregador na caixa"],
        "image_color": "#1C1C1E",
    },
    {
        "name": "Samsung Galaxy S24 Ultra",
        "brand": "Samsung",
        "price": 9499,
        "specs": {
            "processor": "Snapdragon 8 Gen 3",
            "processor_score": 97,
            "camera_mp": 200,
            "camera_score": 96,
            "battery_mah": 5000,
            "battery_score": 88,
            "storage_gb": 256,
            "ram_gb": 12,
            "display": "6.8\" Dynamic AMOLED 2X 120Hz",
            "weight_g": 232,
            "os": "Android 14 / One UI 6.1",
            "5g": True,
        },
        "use_scores": {"jogos": 95, "estudos": 92, "profissional": 97, "conteudo": 97},
        "highlights": [
            "Câmera de 200MP com zoom óptico 10x",
            "S Pen integrada para anotações e criatividade",
            "IA Galaxy avançada para produtividade",
            "Display titanium com cantos chatos",
            "7 anos de suporte garantido",
        ],
        "pros": ["S Pen integrada", "Câmera versátil zoom", "IA generativa nativa", "Bateria duradoura"],
        "cons": ["Muito pesado", "Preço premium", "One UI pode ser complexo"],
        "image_color": "#1B2A4A",
    },
    {
        "name": "Google Pixel 9 Pro",
        "brand": "Google",
        "price": 7499,
        "specs": {
            "processor": "Google Tensor G4",
            "processor_score": 88,
            "camera_mp": 50,
            "camera_score": 95,
            "battery_mah": 4700,
            "battery_score": 86,
            "storage_gb": 128,
            "ram_gb": 16,
            "display": "6.3\" LTPO OLED 120Hz",
            "weight_g": 199,
            "os": "Android 14",
            "5g": True,
        },
        "use_scores": {"jogos": 82, "estudos": 93, "profissional": 91, "conteudo": 96},
        "highlights": [
            "Computação fotográfica mais avançada do mundo",
            "Android puro com atualizações primeiro",
            "Magic Eraser e ferramentas IA exclusivas",
            "Temperatura corporal e sensor de saúde avançado",
            "7 anos de atualizações garantidas",
        ],
        "pros": ["Melhor software de câmera", "Android limpo", "IA Google nativa", "Compacto e leve"],
        "cons": ["Tensor G4 menos potente em games", "Armazenamento base 128GB", "Pouco popular no Brasil"],
        "image_color": "#2D4A3E",
    },
    {
        "name": "Xiaomi 14 Ultra",
        "brand": "Xiaomi",
        "price": 7999,
        "specs": {
            "processor": "Snapdragon 8 Gen 3",
            "processor_score": 97,
            "camera_mp": 50,
            "camera_score": 94,
            "battery_mah": 5000,
            "battery_score": 95,
            "storage_gb": 512,
            "ram_gb": 16,
            "display": "6.73\" LTPO AMOLED 120Hz",
            "weight_g": 219,
            "os": "Android 14 / HyperOS",
            "5g": True,
        },
        "use_scores": {"jogos": 97, "estudos": 85, "profissional": 88, "conteudo": 95},
        "highlights": [
            "Sistema óptico Leica profissional",
            "Carregamento 90W + wireless 80W ultrarrápido",
            "Snapdragon 8 Gen 3 para máxima performance",
            "Bateria de 5000mAh que dura 2 dias",
            "512GB de armazenamento na versão base",
        ],
        "pros": ["Melhor custo-benefício premium", "Câmera Leica profissional", "Carregamento ultra rápido", "Armazenamento enorme"],
        "cons": ["HyperOS tem muitos apps instalados", "Câmera grande demais", "Suporte de software menor que Apple/Samsung"],
        "image_color": "#2C1810",
    },
    {
        "name": "Samsung Galaxy S24+",
        "brand": "Samsung",
        "price": 6499,
        "specs": {
            "processor": "Snapdragon 8 Gen 3",
            "processor_score": 97,
            "camera_mp": 50,
            "camera_score": 89,
            "battery_mah": 4900,
            "battery_score": 87,
            "storage_gb": 256,
            "ram_gb": 12,
            "display": "6.7\" Dynamic AMOLED 2X 120Hz",
            "weight_g": 196,
            "os": "Android 14 / One UI 6.1",
            "5g": True,
        },
        "use_scores": {"jogos": 93, "estudos": 88, "profissional": 90, "conteudo": 88},
        "highlights": [
            "Performance flagship sem preço ultra premium",
            "Display enorme com bordas planas",
            "Galaxy AI para produtividade",
            "Bateria que dura o dia todo",
            "7 anos de atualizações",
        ],
        "pros": ["Ótima performance", "Display excelente", "Bateria boa", "Custo-benefício entre flagships"],
        "cons": ["Câmera inferior ao Ultra", "Sem S Pen", "Preço ainda elevado"],
        "image_color": "#1A3A5C",
    },
    {
        "name": "iPhone 15",
        "brand": "Apple",
        "price": 5999,
        "specs": {
            "processor": "Apple A16 Bionic",
            "processor_score": 94,
            "camera_mp": 48,
            "camera_score": 90,
            "battery_mah": 3877,
            "battery_score": 75,
            "storage_gb": 128,
            "ram_gb": 6,
            "display": "6.1\" Super Retina XDR OLED 60Hz",
            "weight_g": 171,
            "os": "iOS 17",
            "5g": True,
        },
        "use_scores": {"jogos": 88, "estudos": 89, "profissional": 87, "conteudo": 88},
        "highlights": [
            "Dynamic Island e câmera 48MP com USB-C",
            "Chip A16 extremamente eficiente",
            "Leve e compacto para uso diário",
            "Ecossistema Apple completo",
            "Suporte iOS por muitos anos",
        ],
        "pros": ["Leve e premium", "Ecossistema Apple", "Performance excelente", "USB-C finalmente"],
        "cons": ["60Hz no display", "Bateria pequena", "128GB base", "Preço alto pelo tier"],
        "image_color": "#2E4057",
    },
    {
        "name": "Motorola Edge 50 Pro",
        "brand": "Motorola",
        "price": 3299,
        "specs": {
            "processor": "Snapdragon 7 Gen 3",
            "processor_score": 82,
            "camera_mp": 50,
            "camera_score": 80,
            "battery_mah": 4500,
            "battery_score": 90,
            "storage_gb": 256,
            "ram_gb": 12,
            "display": "6.7\" pOLED 144Hz",
            "weight_g": 186,
            "os": "Android 14",
            "5g": True,
        },
        "use_scores": {"jogos": 80, "estudos": 82, "profissional": 78, "conteudo": 79},
        "highlights": [
            "Display pOLED 144Hz ultrafluido",
            "Carregamento TurboPower 125W",
            "Android praticamente limpo",
            "Ótimo custo-benefício intermediário",
            "Design elegante com couro vegano",
        ],
        "pros": ["Custo-benefício excelente", "Carregamento 125W ultra rápido", "Display 144Hz", "Android limpo"],
        "cons": ["Sem estabilização óptica traseira", "Processador intermediário", "Câmera não compete com flagships"],
        "image_color": "#1A1A2E",
    },
    {
        "name": "Xiaomi Redmi Note 13 Pro+",
        "brand": "Xiaomi",
        "price": 2199,
        "specs": {
            "processor": "MediaTek Dimensity 7200 Ultra",
            "processor_score": 75,
            "camera_mp": 200,
            "camera_score": 78,
            "battery_mah": 5000,
            "battery_score": 91,
            "storage_gb": 256,
            "ram_gb": 8,
            "display": "6.67\" AMOLED 120Hz",
            "weight_g": 204,
            "os": "Android 13 / MIUI 14",
            "5g": True,
        },
        "use_scores": {"jogos": 72, "estudos": 80, "profissional": 70, "conteudo": 75},
        "highlights": [
            "Câmera de 200MP no custo intermediário",
            "Bateria 5000mAh com carregamento 120W",
            "Display AMOLED 120Hz brilhante",
            "Melhor custo-benefício do mercado",
            "5G por menos de R$2500",
        ],
        "pros": ["Preço acessível", "Câmera 200MP", "Bateria com carga rápida 120W", "Display AMOLED"],
        "cons": ["MIUI com muitos apps", "Processador médio", "Câmera 200MP com qualidade real limitada"],
        "image_color": "#162032",
    },
    {
        "name": "Samsung Galaxy A55 5G",
        "brand": "Samsung",
        "price": 2799,
        "specs": {
            "processor": "Exynos 1480",
            "processor_score": 72,
            "camera_mp": 50,
            "camera_score": 76,
            "battery_mah": 5000,
            "battery_score": 88,
            "storage_gb": 128,
            "ram_gb": 8,
            "display": "6.6\" Super AMOLED 120Hz",
            "weight_g": 213,
            "os": "Android 14 / One UI 6.1",
            "5g": True,
        },
        "use_scores": {"jogos": 71, "estudos": 81, "profissional": 75, "conteudo": 73},
        "highlights": [
            "4 anos de atualizações garantidas pela Samsung",
            "IP67 — resistente a água",
            "Display Super AMOLED vibrante",
            "Design robusto e premium para o preço",
            "Câmera versátil com OIS",
        ],
        "pros": ["IP67 resistente à água", "4 anos de updates Samsung", "Display AMOLED ótimo", "Marca confiável"],
        "cons": ["Processador Exynos inferior", "Sem carregamento rápido potente", "128GB base"],
        "image_color": "#0D2137",
    },
    {
        "name": "OnePlus 12",
        "brand": "OnePlus",
        "price": 5499,
        "specs": {
            "processor": "Snapdragon 8 Gen 3",
            "processor_score": 97,
            "camera_mp": 50,
            "camera_score": 87,
            "battery_mah": 5400,
            "battery_score": 93,
            "storage_gb": 256,
            "ram_gb": 12,
            "display": "6.82\" LTPO AMOLED 120Hz",
            "weight_g": 220,
            "os": "Android 14 / OxygenOS 14",
            "5g": True,
        },
        "use_scores": {"jogos": 96, "estudos": 85, "profissional": 85, "conteudo": 85},
        "highlights": [
            "Snapdragon 8 Gen 3 com resfriamento superior",
            "Bateria 5400mAh + carga 100W ultrarrápida",
            "Câmera Hasselblad calibrada profissionalmente",
            "Melhor performance por real do mercado",
            "OxygenOS limpo e fluido",
        ],
        "pros": ["Melhor custo-benefício flagship", "Performance topo de linha", "Bateria enorme + carga 100W", "Câmera Hasselblad"],
        "cons": ["Câmera não é top 3", "Marca menos conhecida no Brasil", "Sem IP68 na versão padrão"],
        "image_color": "#0A2818",
    },
    {
        "name": "ASUS ROG Phone 8 Pro",
        "brand": "ASUS",
        "price": 8999,
        "specs": {
            "processor": "Snapdragon 8 Gen 3",
            "processor_score": 99,
            "camera_mp": 50,
            "camera_score": 82,
            "battery_mah": 5500,
            "battery_score": 90,
            "storage_gb": 512,
            "ram_gb": 16,
            "display": "6.78\" AMOLED 165Hz",
            "weight_g": 225,
            "os": "Android 14 / ROG UI",
            "5g": True,
        },
        "use_scores": {"jogos": 100, "estudos": 72, "profissional": 75, "conteudo": 80},
        "highlights": [
            "Display 165Hz — o mais fluido para games",
            "Resfriamento ativo com cooler de vapor",
            "Gatilhos AirTrigger para controle preciso",
            "512GB e 16GB RAM para máximo desempenho",
            "Bateria 5500mAh para sessões longas",
        ],
        "pros": ["Melhor smartphone para games", "Display 165Hz", "Cooler ativo", "Gatilhos físicos exclusivos"],
        "cons": ["Câmera não é prioridade", "Design gamer polarizador", "Caro para o que oferece fora de games"],
        "image_color": "#1A0A2E",
    },
    {
        "name": "Sony Xperia 1 VI",
        "brand": "Sony",
        "price": 10999,
        "specs": {
            "processor": "Snapdragon 8 Gen 3",
            "processor_score": 97,
            "camera_mp": 52,
            "camera_score": 93,
            "battery_mah": 5000,
            "battery_score": 86,
            "storage_gb": 256,
            "ram_gb": 12,
            "display": "6.5\" OLED 120Hz 4K",
            "weight_g": 192,
            "os": "Android 14",
            "5g": True,
        },
        "use_scores": {"jogos": 88, "estudos": 85, "profissional": 92, "conteudo": 97},
        "highlights": [
            "Câmera com sensor Alpha — qualidade fotográfica profissional",
            "Display 4K OLED — o mais nítido disponível",
            "Gravação de vídeo com controles manuais Cinema Pro",
            "Áudio de alta resolução com P2 dedicado",
            "Zoom óptico contínuo 1x–7.1x",
        ],
        "pros": ["Câmera profissional Sony Alpha", "Display 4K único no mercado", "Áudio premium", "Vídeo cinematográfico"],
        "cons": ["Preço altíssimo", "Design conservador", "Pouca presença no Brasil"],
        "image_color": "#1C1C1C",
    },
    {
        "name": "Motorola Moto G84",
        "brand": "Motorola",
        "price": 1399,
        "specs": {
            "processor": "Snapdragon 695",
            "processor_score": 62,
            "camera_mp": 50,
            "camera_score": 65,
            "battery_mah": 5000,
            "battery_score": 85,
            "storage_gb": 256,
            "ram_gb": 12,
            "display": "6.55\" pOLED 120Hz",
            "weight_g": 169,
            "os": "Android 14",
            "5g": True,
        },
        "use_scores": {"jogos": 58, "estudos": 75, "profissional": 65, "conteudo": 62},
        "highlights": [
            "pOLED 120Hz num preço muito acessível",
            "256GB de armazenamento — enorme para o preço",
            "Android quase limpo da Motorola",
            "Leve e fino para o dia a dia",
            "5G acessível",
        ],
        "pros": ["Excelente custo-benefício", "Display pOLED 120Hz", "256GB de base", "Leve e fino"],
        "cons": ["Processador limitado para games pesados", "Câmera básica", "Sem carregamento rápido potente"],
        "image_color": "#1E2D3D",
    },
    {
        "name": "Samsung Galaxy Z Fold 6",
        "brand": "Samsung",
        "price": 19999,
        "specs": {
            "processor": "Snapdragon 8 Gen 3",
            "processor_score": 97,
            "camera_mp": 50,
            "camera_score": 88,
            "battery_mah": 4400,
            "battery_score": 78,
            "storage_gb": 256,
            "ram_gb": 12,
            "display": "7.6\" AMOLED 120Hz dobrável",
            "weight_g": 239,
            "os": "Android 14 / One UI 6.1.1",
            "5g": True,
        },
        "use_scores": {"jogos": 88, "estudos": 97, "profissional": 99, "conteudo": 90},
        "highlights": [
            "Tela dobrável de 7.6\" — tablet e celular em um",
            "Multitarefa avançada com 3 apps simultâneos",
            "S Pen compatível para anotações",
            "Design premium em alumínio Armor",
            "Ideal para produtividade máxima",
        ],
        "pros": ["Produtividade sem igual", "Tela enorme dobrável", "Multitarefa real", "Status e inovação"],
        "cons": ["Preço extremo", "Bateria fraca para o tamanho", "Pesado e grosso", "Câmera inferior ao Ultra"],
        "image_color": "#0D1B2A",
    },
    {
        "name": "Realme GT 6",
        "brand": "Realme",
        "price": 3799,
        "specs": {
            "processor": "Snapdragon 8s Gen 3",
            "processor_score": 91,
            "camera_mp": 50,
            "camera_score": 79,
            "battery_mah": 5000,
            "battery_score": 88,
            "storage_gb": 256,
            "ram_gb": 12,
            "display": "6.78\" AMOLED 120Hz",
            "weight_g": 199,
            "os": "Android 14 / Realme UI 5",
            "5g": True,
        },
        "use_scores": {"jogos": 89, "estudos": 80, "profissional": 78, "conteudo": 78},
        "highlights": [
            "Snapdragon 8s Gen 3 por preço de intermediário",
            "Display AMOLED brilhante e nítido",
            "Bateria 5000mAh com carregamento 120W",
            "Ótima performance para games e uso pesado",
            "Design moderno e atrativo",
        ],
        "pros": ["Melhor processador por real", "Carga 120W ultrarrápida", "Boa performance em games", "Preço atrativo"],
        "cons": ["Câmera não é destaque", "Realme UI com muitos apps", "Suporte menor que as grandes marcas"],
        "image_color": "#1A2E1A",
    },

    {
        "name": "Samsung Galaxy S25 Ultra",
        "brand": "Samsung",
        "price": 10999,
        "specs": {
            "processor": "Snapdragon 8 Elite",
            "processor_score": 100,
            "camera_mp": 200,
            "camera_score": 98,
            "battery_mah": 5000,
            "battery_score": 89,
            "storage_gb": 256,
            "ram_gb": 12,
            "display": "6.9\" Dynamic AMOLED 2X 120Hz",
            "weight_g": 218,
            "os": "Android 15 / One UI 7",
            "5g": True,
        },
        "use_scores": {"jogos": 98, "estudos": 95, "profissional": 99, "conteudo": 99},
        "highlights": [
            "Snapdragon 8 Elite — processador mais potente do mundo",
            "Câmera 200MP com IA generativa avançada",
            "S Pen integrada com latência ultrabaixa",
            "7 anos de atualizações garantidas",
            "Galaxy AI de última geração",
        ],
        "pros": ["Processador imbatível", "Câmera com IA top", "S Pen integrada", "Suporte 7 anos"],
        "cons": ["Preço muito elevado", "Pesado", "Carregamento 45W apenas"],
        "image_color": "#101A2E",
    },
    {
        "name": "iPhone 16 Pro Max",
        "brand": "Apple",
        "price": 12999,
        "specs": {
            "processor": "Apple A18 Pro",
            "processor_score": 100,
            "camera_mp": 48,
            "camera_score": 99,
            "battery_mah": 4685,
            "battery_score": 88,
            "storage_gb": 256,
            "ram_gb": 8,
            "display": "6.9\" Super Retina XDR OLED 120Hz",
            "weight_g": 227,
            "os": "iOS 18",
            "5g": True,
        },
        "use_scores": {"jogos": 98, "estudos": 92, "profissional": 97, "conteudo": 99},
        "highlights": [
            "Chip A18 Pro — melhor do mercado para Apple Intelligence",
            "Câmera 48MP com zoom tetra-prisma 5x",
            "Gravação ProRes 4K a 120fps",
            "Botão Camera Control dedicado",
            "Apple Intelligence com IA generativa",
        ],
        "pros": ["Melhor câmera de vídeo", "Apple Intelligence nativo", "Tela maior da linha Pro", "Ecossistema Apple"],
        "cons": ["Preço altíssimo", "Bateria não revolucionária", "Sem carregador na caixa"],
        "image_color": "#1C1A10",
    },
    {
        "name": "Motorola Edge 50 Ultra",
        "brand": "Motorola",
        "price": 4299,
        "specs": {
            "processor": "Snapdragon 8s Gen 3",
            "processor_score": 91,
            "camera_mp": 50,
            "camera_score": 84,
            "battery_mah": 4500,
            "battery_score": 89,
            "storage_gb": 512,
            "ram_gb": 12,
            "display": "6.67\" pOLED 165Hz",
            "weight_g": 182,
            "os": "Android 14",
            "5g": True,
        },
        "use_scores": {"jogos": 85, "estudos": 84, "profissional": 83, "conteudo": 84},
        "highlights": [
            "Display pOLED 165Hz — dos mais fluidos do mercado",
            "512GB de armazenamento nativo",
            "Carregamento 125W + wireless 50W",
            "Leve e fino com design premium",
            "Android limpo sem bloatwares",
        ],
        "pros": ["Display 165Hz incrível", "512GB nativo", "Carregamento 125W", "Leve para o tamanho"],
        "cons": ["Câmera não é top", "Processador intermediário-alto", "Bateria 4500mAh apenas"],
        "image_color": "#1A0E2E",
    },
    {
        "name": "Xiaomi Redmi Note 14 Pro+",
        "brand": "Xiaomi",
        "price": 2599,
        "specs": {
            "processor": "Snapdragon 7s Gen 3",
            "processor_score": 79,
            "camera_mp": 200,
            "camera_score": 81,
            "battery_mah": 6200,
            "battery_score": 97,
            "storage_gb": 256,
            "ram_gb": 12,
            "display": "6.67\" AMOLED 120Hz",
            "weight_g": 210,
            "os": "Android 14 / HyperOS",
            "5g": True,
        },
        "use_scores": {"jogos": 74, "estudos": 83, "profissional": 73, "conteudo": 78},
        "highlights": [
            "Bateria de 6200mAh — maior autonomia da categoria",
            "Câmera de 200MP por preço acessível",
            "Carregamento 90W ultrarrápido",
            "IP68 — resistência total à água",
            "Display AMOLED 120Hz brilhante",
        ],
        "pros": ["Bateria gigantesca", "IP68 resistente", "200MP acessível", "Carga 90W rápida"],
        "cons": ["Processador intermediário", "HyperOS pode ter bloatwares", "Câmera real limitada"],
        "image_color": "#0A1A2A",
    },
    {
        "name": "Samsung Galaxy A35 5G",
        "brand": "Samsung",
        "price": 1899,
        "specs": {
            "processor": "Exynos 1380",
            "processor_score": 68,
            "camera_mp": 50,
            "camera_score": 72,
            "battery_mah": 5000,
            "battery_score": 87,
            "storage_gb": 128,
            "ram_gb": 6,
            "display": "6.6\" Super AMOLED 120Hz",
            "weight_g": 210,
            "os": "Android 14 / One UI 6.1",
            "5g": True,
        },
        "use_scores": {"jogos": 65, "estudos": 79, "profissional": 70, "conteudo": 69},
        "highlights": [
            "4 anos de atualizações Samsung garantidas",
            "IP67 — resistência à água por preço baixo",
            "Display Super AMOLED vibrante",
            "Confiabilidade Samsung com preço acessível",
            "5G integrado na faixa de R$1900",
        ],
        "pros": ["IP67 no preço", "4 anos de updates", "Display AMOLED", "Marca confiável"],
        "cons": ["Processador fraco para jogos", "128GB base", "Carregamento lento 25W"],
        "image_color": "#0D1A30",
    },
    {
        "name": "Poco X6 Pro",
        "brand": "Xiaomi/Poco",
        "price": 2299,
        "specs": {
            "processor": "MediaTek Dimensity 8300 Ultra",
            "processor_score": 87,
            "camera_mp": 64,
            "camera_score": 74,
            "battery_mah": 5000,
            "battery_score": 88,
            "storage_gb": 256,
            "ram_gb": 12,
            "display": "6.67\" AMOLED 120Hz",
            "weight_g": 186,
            "os": "Android 14 / MIUI 14",
            "5g": True,
        },
        "use_scores": {"jogos": 88, "estudos": 77, "profissional": 72, "conteudo": 71},
        "highlights": [
            "Dimensity 8300 Ultra — processador top por preço intermediário",
            "Melhor smartphone para games abaixo de R$2500",
            "Display AMOLED 120Hz",
            "256GB de armazenamento",
            "Bateria 5000mAh com carga 67W",
        ],
        "pros": ["Melhor processador da categoria", "Ótimo para games", "256GB nativo", "Preço atrativo"],
        "cons": ["Câmera básica", "MIUI com bloatwares", "Design simples"],
        "image_color": "#2A0E1A",
    },
    {
        "name": "Motorola Moto G85",
        "brand": "Motorola",
        "price": 1699,
        "specs": {
            "processor": "Snapdragon 6 Gen 1",
            "processor_score": 65,
            "camera_mp": 50,
            "camera_score": 68,
            "battery_mah": 5000,
            "battery_score": 85,
            "storage_gb": 256,
            "ram_gb": 8,
            "display": "6.67\" pOLED 120Hz",
            "weight_g": 171,
            "os": "Android 14",
            "5g": True,
        },
        "use_scores": {"jogos": 62, "estudos": 77, "profissional": 68, "conteudo": 67},
        "highlights": [
            "Display pOLED 120Hz raridade no preço",
            "Leve com apenas 171g",
            "256GB de armazenamento incluso",
            "Android praticamente limpo",
            "Excelente custo-benefício básico",
        ],
        "pros": ["pOLED no preço", "Leve e fino", "256GB nativo", "Android limpo"],
        "cons": ["Processador limitado", "Câmera básica", "Sem carregamento rápido potente"],
        "image_color": "#1A2A3A",
    },
    {
        "name": "OnePlus 13",
        "brand": "OnePlus",
        "price": 6299,
        "specs": {
            "processor": "Snapdragon 8 Elite",
            "processor_score": 100,
            "camera_mp": 50,
            "camera_score": 88,
            "battery_mah": 6000,
            "battery_score": 97,
            "storage_gb": 256,
            "ram_gb": 12,
            "display": "6.82\" LTPO AMOLED 120Hz",
            "weight_g": 210,
            "os": "Android 15 / OxygenOS 15",
            "5g": True,
        },
        "use_scores": {"jogos": 98, "estudos": 87, "profissional": 87, "conteudo": 87},
        "highlights": [
            "Snapdragon 8 Elite com resfriamento superior",
            "Bateria 6000mAh com carga 100W ultrarrápida",
            "Melhor custo-benefício flagship de 2025",
            "IP65 resistência à poeira e água",
            "Câmera Hasselblad calibrada profissionalmente",
        ],
        "pros": ["Processador topo de linha", "Bateria enorme 6000mAh", "Carga 100W", "Melhor custo-benefício"],
        "cons": ["Câmera não é top 3", "Marca menos conhecida no Brasil", "UI pode ser pesada"],
        "image_color": "#0A2010",
    },
    {
        "name": "iPhone 16",
        "brand": "Apple",
        "price": 6499,
        "specs": {
            "processor": "Apple A18",
            "processor_score": 96,
            "camera_mp": 48,
            "camera_score": 92,
            "battery_mah": 3561,
            "battery_score": 78,
            "storage_gb": 128,
            "ram_gb": 8,
            "display": "6.1\" Super Retina XDR OLED 60Hz",
            "weight_g": 170,
            "os": "iOS 18",
            "5g": True,
        },
        "use_scores": {"jogos": 90, "estudos": 90, "profissional": 88, "conteudo": 90},
        "highlights": [
            "Apple Intelligence integrado nativo",
            "Chip A18 com suporte total a IA",
            "Botão Camera Control exclusivo",
            "O iPhone mais leve e compacto",
            "Ecossistema Apple completo",
        ],
        "pros": ["Apple Intelligence", "Compacto e leve", "Camera Control", "Performance sólida"],
        "cons": ["60Hz no display", "Bateria pequena", "128GB base", "Preço alto para o tier"],
        "image_color": "#203040",
    },
    {
        "name": "Samsung Galaxy Z Flip 6",
        "brand": "Samsung",
        "price": 7999,
        "specs": {
            "processor": "Snapdragon 8 Gen 3",
            "processor_score": 97,
            "camera_mp": 50,
            "camera_score": 82,
            "battery_mah": 4000,
            "battery_score": 74,
            "storage_gb": 256,
            "ram_gb": 12,
            "display": "6.7\" Dynamic AMOLED 120Hz dobrável",
            "weight_g": 187,
            "os": "Android 14 / One UI 6.1.1",
            "5g": True,
        },
        "use_scores": {"jogos": 82, "estudos": 80, "profissional": 84, "conteudo": 88},
        "highlights": [
            "Design flip que cabe em qualquer bolso",
            "Tela externa 3.4\" FlexWindow útil",
            "Snapdragon 8 Gen 3 topo de linha",
            "Fotos únicas com ângulos criativos",
            "Ideal para quem busca estilo diferenciado",
        ],
        "pros": ["Design único e compacto", "Performance flagship", "Estilo diferenciado", "Tela externa funcional"],
        "cons": ["Bateria fraca 4000mAh", "Câmera básica para o preço", "Durabilidade da dobradiça"],
        "image_color": "#2A0A2A",
    },
    {
        "name": "Xiaomi 14T Pro",
        "brand": "Xiaomi",
        "price": 5999,
        "specs": {
            "processor": "MediaTek Dimensity 9300+",
            "processor_score": 96,
            "camera_mp": 50,
            "camera_score": 92,
            "battery_mah": 5000,
            "battery_score": 93,
            "storage_gb": 512,
            "ram_gb": 12,
            "display": "6.67\" AMOLED 144Hz",
            "weight_g": 209,
            "os": "Android 14 / HyperOS",
            "5g": True,
        },
        "use_scores": {"jogos": 94, "estudos": 86, "profissional": 87, "conteudo": 93},
        "highlights": [
            "Câmera Leica com 3 lentes otimizadas",
            "Carregamento 120W + wireless 50W",
            "Display 144Hz para máxima fluidez",
            "512GB de armazenamento nativo",
            "Dimensity 9300+ de altíssima performance",
        ],
        "pros": ["Câmera Leica excelente", "512GB nativo", "Carga 120W", "Display 144Hz"],
        "cons": ["HyperOS com bloatwares", "Câmera grande", "Suporte menor que Apple/Samsung"],
        "image_color": "#1A2A10",
    },
    {
        "name": "Google Pixel 9",
        "brand": "Google",
        "price": 5499,
        "specs": {
            "processor": "Google Tensor G4",
            "processor_score": 85,
            "camera_mp": 50,
            "camera_score": 94,
            "battery_mah": 4700,
            "battery_score": 85,
            "storage_gb": 128,
            "ram_gb": 12,
            "display": "6.3\" OLED 120Hz",
            "weight_g": 198,
            "os": "Android 15",
            "5g": True,
        },
        "use_scores": {"jogos": 78, "estudos": 91, "profissional": 89, "conteudo": 95},
        "highlights": [
            "Computação fotográfica de ponta — melhor câmera por software",
            "Android 15 puro com updates garantidos",
            "Gemini AI integrado nativamente",
            "Magic Editor e ferramentas IA exclusivas",
            "7 anos de atualizações garantidas",
        ],
        "pros": ["Melhor câmera por software", "Gemini AI nativo", "Android limpo", "7 anos de updates"],
        "cons": ["Tensor G4 menos potente em games", "128GB base apenas", "Pouco popular no Brasil"],
        "image_color": "#1A3A2E",
    },
    {
        "name": "Motorola Moto G55 5G",
        "brand": "Motorola",
        "price": 1299,
        "specs": {
            "processor": "MediaTek Dimensity 7025",
            "processor_score": 58,
            "camera_mp": 50,
            "camera_score": 62,
            "battery_mah": 5000,
            "battery_score": 83,
            "storage_gb": 128,
            "ram_gb": 8,
            "display": "6.49\" IPS LCD 120Hz",
            "weight_g": 179,
            "os": "Android 14",
            "5g": True,
        },
        "use_scores": {"jogos": 55, "estudos": 72, "profissional": 62, "conteudo": 58},
        "highlights": [
            "5G mais barato do mercado",
            "Bateria 5000mAh de longa duração",
            "Android limpo sem bloatwares",
            "Leve e confortável no dia a dia",
            "Ideal para uso básico e comunicação",
        ],
        "pros": ["5G mais acessível", "Bateria boa", "Android limpo", "Leve e confortável"],
        "cons": ["Processador muito básico", "Câmera simples", "Sem AMOLED"],
        "image_color": "#152030",
    },
    {
        "name": "Samsung Galaxy A16 5G",
        "brand": "Samsung",
        "price": 1199,
        "specs": {
            "processor": "Exynos 1330",
            "processor_score": 60,
            "camera_mp": 50,
            "camera_score": 63,
            "battery_mah": 5000,
            "battery_score": 84,
            "storage_gb": 128,
            "ram_gb": 4,
            "display": "6.7\" Super AMOLED 90Hz",
            "weight_g": 200,
            "os": "Android 14 / One UI 6",
            "5g": True,
        },
        "use_scores": {"jogos": 56, "estudos": 74, "profissional": 63, "conteudo": 60},
        "highlights": [
            "Super AMOLED no preço mais baixo do mercado",
            "6 anos de atualizações Samsung garantidas",
            "5G acessível com marca confiável",
            "Bateria 5000mAh duradoura",
            "Design moderno e resistente",
        ],
        "pros": ["AMOLED baratíssimo", "6 anos de updates Samsung", "5G acessível", "Marca confiável"],
        "cons": ["4GB RAM limitado", "Processador básico", "Carregamento 25W"],
        "image_color": "#0A1520",
    },
]

USE_CASES = {
    "jogos": {"label": "🎮 Jogos", "icon": "🎮", "color": "#B06060", "weights": {"processor_score": 0.40, "battery_score": 0.25, "camera_score": 0.10, "storage_score": 0.25}},
    "estudos": {"label": "📚 Estudos", "icon": "📚", "color": "#6B96D4", "weights": {"processor_score": 0.20, "battery_score": 0.35, "camera_score": 0.15, "storage_score": 0.30}},
    "profissional": {"label": "💼 Profissional/Trabalho", "icon": "💼", "color": "#6AAF80", "weights": {"processor_score": 0.30, "battery_score": 0.30, "camera_score": 0.20, "storage_score": 0.20}},
    "conteudo": {"label": "📸 Criação de Conteúdo", "icon": "📸", "color": "#C8A84A", "weights": {"processor_score": 0.20, "battery_score": 0.20, "camera_score": 0.45, "storage_score": 0.15}},
}


def score_phone(phone, use_case, max_price, custom_weights=None):
    specs = phone["specs"]
    storage_score = min(100, (specs["storage_gb"] / 512) * 100)
    if custom_weights is not None:
        weights = custom_weights
    else:
        weights = USE_CASES[use_case]["weights"]
    total = (
        specs["processor_score"] * weights["processor_score"]
        + specs["battery_score"] * weights["battery_score"]
        + specs["camera_score"] * weights["camera_score"]
        + storage_score * weights["storage_score"]
    )
  
    price_ratio = phone["price"] / max_price
    value_bonus = (1 - price_ratio) * 5
    return round(total + value_bonus, 1)


def get_recommendations(max_price, use_case, top_n=5, custom_weights=None):
    eligible = [p for p in PHONES_DB if p["price"] <= max_price]
    if not eligible:
        return []
    scored = [(p, score_phone(p, use_case, max_price, custom_weights)) for p in eligible]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_n]


def load_profiles():
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_profiles(profiles):
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)



COLORS = {
    "bg_dark": "#141820",
    "bg_card": "#1C2434",
    "bg_card2": "#232D42",
    "accent": "#6B96D4",
    "accent2": "#7B9BD0",
    "accent3": "#3A5CA8",
    "text": "#E2E8F8",
    "text_muted": "#7A8DA8",
    "gold": "#C8A84A",
    "silver": "#9AAAB8",
    "bronze": "#A87848",
    "green": "#6AAF80",
    "red": "#B06060",
    "border": "#252E40",
}

MEDAL_COLORS = [COLORS["gold"], COLORS["silver"], COLORS["bronze"], "#6B9BD2", "#8B6B9B"]



    def __init__(self):
        super().__init__()
        self.title("📱 PhoneAdvisor — Qual Celular Comprar?")
        self.geometry("1300x800")
        self.minsize(1100, 700)
        self.configure(fg_color=COLORS["bg_dark"])

        self.profiles = load_profiles()
        self.current_profile = None
        self.results = []
        self.selected_use = ctk.StringVar(value="jogos")
        self.price_var = ctk.IntVar(value=6000)
        self.comparing = []

      
        self.w_processor = ctk.IntVar(value=40)
        self.w_battery = ctk.IntVar(value=25)
        self.w_camera = ctk.IntVar(value=10)
        self.w_storage = ctk.IntVar(value=25)
        self._use_custom_weights = ctk.BooleanVar(value=False)

        self._build_ui()
       
        self._load_preset_weights("jogos")

  
    def _build_ui(self):
       
        header = ctk.CTkFrame(self, fg_color=COLORS["bg_card"], corner_radius=0, height=48)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="📱 PhoneAdvisor",
            font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold"),
            text_color=COLORS["accent"],
        ).pack(side="left", padx=16, pady=8)

        ctk.CTkLabel(
            header,
            text="Guia inteligente de smartphones",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_muted"],
        ).pack(side="left", padx=4)

       
        self.profile_label = ctk.CTkLabel(header, text="Sem perfil", text_color=COLORS["text_muted"], font=ctk.CTkFont(size=11))
        self.profile_label.pack(side="right", padx=8)
        ctk.CTkButton(header, text="💾 Salvar", width=90, height=30, fg_color=COLORS["accent2"], hover_color=COLORS["accent3"],
                      command=self._save_profile_dialog, corner_radius=6).pack(side="right", padx=4)
        ctk.CTkButton(header, text="📂 Perfis", width=80, height=30, fg_color=COLORS["bg_card2"], hover_color=COLORS["border"],
                      command=self._open_profiles_dialog, corner_radius=6).pack(side="right", padx=4)

        
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=8, pady=8)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)

      
        self._build_left_panel(main)
        
        self._build_right_panel(main)

    def _build_left_panel(self, parent):
        outer = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], corner_radius=12, width=290)
        outer.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        outer.grid_propagate(False)
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(0, weight=1)

        panel = ctk.CTkScrollableFrame(outer, fg_color="transparent", corner_radius=0,
                                       scrollbar_button_color=COLORS["border"],
                                       scrollbar_button_hover_color=COLORS["accent"])
        panel.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        panel.columnconfigure(0, weight=1)

        ctk.CTkLabel(panel, text="⚙️  Configurar Busca", font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=COLORS["text"]).grid(row=0, column=0, padx=12, pady=(10, 4), sticky="w")

       
        budget_frame = ctk.CTkFrame(panel, fg_color=COLORS["bg_card2"], corner_radius=10)
        budget_frame.grid(row=1, column=0, padx=8, pady=4, sticky="ew")
        ctk.CTkLabel(budget_frame, text="💰 Orçamento máximo", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=COLORS["accent"]).pack(anchor="w", padx=10, pady=(8, 0))

        self.price_display = ctk.CTkLabel(budget_frame, text="R$ 6.000",
                                          font=ctk.CTkFont(size=20, weight="bold"), text_color=COLORS["gold"])
        self.price_display.pack(pady=(0, 2))

        slider = ctk.CTkSlider(budget_frame, from_=800, to=20000, variable=self.price_var,
                               command=self._on_price_change, progress_color=COLORS["accent"],
                               button_color=COLORS["accent"], button_hover_color=COLORS["accent2"], height=16)
        slider.pack(fill="x", padx=10, pady=(2, 2))

        price_row = ctk.CTkFrame(budget_frame, fg_color="transparent")
        price_row.pack(fill="x", padx=10, pady=(0, 6))
        ctk.CTkLabel(price_row, text="R$ 800", font=ctk.CTkFont(size=9), text_color=COLORS["text_muted"]).pack(side="left")
        ctk.CTkLabel(price_row, text="R$ 20.000", font=ctk.CTkFont(size=9), text_color=COLORS["text_muted"]).pack(side="right")

       
        use_frame = ctk.CTkFrame(panel, fg_color=COLORS["bg_card2"], corner_radius=10)
        use_frame.grid(row=2, column=0, padx=8, pady=4, sticky="ew")
        ctk.CTkLabel(use_frame, text="🎯 Para qual uso?", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=COLORS["accent"]).pack(anchor="w", padx=10, pady=(8, 4))

        self.use_btns = {}
        for key, info in USE_CASES.items():
            btn = ctk.CTkButton(
                use_frame, text=info["label"], corner_radius=8,
                fg_color=COLORS["bg_dark"] if self.selected_use.get() != key else info["color"],
                hover_color=info["color"], text_color=COLORS["text"], font=ctk.CTkFont(size=11),
                command=lambda k=key: self._select_use(k), height=30
            )
            btn.pack(fill="x", padx=8, pady=2)
            self.use_btns[key] = btn
        ctk.CTkFrame(use_frame, fg_color="transparent", height=4).pack()

        
        weights_frame = ctk.CTkFrame(panel, fg_color=COLORS["bg_card2"], corner_radius=10)
        weights_frame.grid(row=3, column=0, padx=8, pady=4, sticky="ew")

        title_row = ctk.CTkFrame(weights_frame, fg_color="transparent")
        title_row.pack(fill="x", padx=10, pady=(8, 2))
        ctk.CTkLabel(title_row, text="🎚️ Pesos",
                     font=ctk.CTkFont(size=11, weight="bold"), text_color=COLORS["accent"]).pack(side="left")

        self.custom_chk = ctk.CTkCheckBox(
            title_row, text="Personalizar", variable=self._use_custom_weights,
            font=ctk.CTkFont(size=10), text_color=COLORS["text_muted"],
            checkbox_width=14, checkbox_height=14,
            fg_color=COLORS["accent"], hover_color=COLORS["accent2"],
            command=self._on_custom_toggle
        )
        self.custom_chk.pack(side="right")

        self.preset_hint = ctk.CTkLabel(weights_frame, text="Baseado no uso selecionado",
                                        font=ctk.CTkFont(size=9), text_color=COLORS["text_muted"])
        self.preset_hint.pack(anchor="w", padx=10, pady=(0, 2))

        
        slider_defs = [
            ("🔥 Desempenho", self.w_processor, COLORS["red"]),
            ("📸 Câmera",     self.w_camera,    COLORS["accent"]),
            ("🔋 Bateria",    self.w_battery,   COLORS["green"]),
            ("💾 Armazen.",   self.w_storage,   COLORS["accent2"]),
        ]
        self.weight_value_labels = {}
        self.weight_sliders = {}
        for label, var, color in slider_defs:
            row = ctk.CTkFrame(weights_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=(1, 0))
            ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=10),
                         text_color=COLORS["text_muted"], width=90, anchor="w").pack(side="left")
            val_lbl = ctk.CTkLabel(row, text=f"{var.get()}%",
                                   font=ctk.CTkFont(size=10, weight="bold"), text_color=color, width=32)
            val_lbl.pack(side="right")
            self.weight_value_labels[label] = val_lbl

            sl = ctk.CTkSlider(
                weights_frame, from_=0, to=100, variable=var,
                progress_color=color, button_color=color,
                button_hover_color=COLORS["accent2"], height=12,
                command=lambda v, lbl=val_lbl, var_ref=var: self._on_weight_slide(v, lbl, var_ref),
                state="disabled"
            )
            sl.pack(fill="x", padx=10, pady=(0, 2))
            self.weight_sliders[label] = sl

        
        self.total_label = ctk.CTkLabel(weights_frame, text="Total: 100%  ✅",
                                        font=ctk.CTkFont(size=9, weight="bold"),
                                        text_color=COLORS["green"])
        self.total_label.pack(anchor="e", padx=10, pady=(0, 6))

        self._refresh_weight_sliders()

       
        ctk.CTkButton(
            panel, text="🔍  Encontrar Meu Celular", height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=COLORS["accent"], hover_color=COLORS["accent2"],
            text_color="#000000", corner_radius=10,
            command=self._run_search
        ).grid(row=4, column=0, padx=8, pady=8, sticky="ew")

      
        compare_frame = ctk.CTkFrame(panel, fg_color=COLORS["bg_card2"], corner_radius=10)
        compare_frame.grid(row=5, column=0, padx=8, pady=(0, 8), sticky="ew")
        ctk.CTkLabel(compare_frame, text="⚖️ Comparar selecionados", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=COLORS["accent"]).pack(anchor="w", padx=10, pady=(8, 2))
        self.compare_label = ctk.CTkLabel(compare_frame, text="Nenhum selecionado", font=ctk.CTkFont(size=10),
                                          text_color=COLORS["text_muted"])
        self.compare_label.pack(anchor="w", padx=10, pady=(0, 4))
        ctk.CTkButton(compare_frame, text="⚖️  Comparar", height=30, corner_radius=8,
                      fg_color=COLORS["accent3"], hover_color=COLORS["accent"],
                      font=ctk.CTkFont(size=11, weight="bold"), command=self._open_compare_window
                      ).pack(fill="x", padx=10, pady=(0, 8))

    def _build_right_panel(self, parent):
        panel = ctk.CTkFrame(parent, fg_color="transparent")
        panel.grid(row=0, column=1, sticky="nsew")
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(1, weight=1)

      
        self.tab_view = ctk.CTkTabview(panel, fg_color=COLORS["bg_card"], corner_radius=12,
                                       segmented_button_fg_color=COLORS["bg_card2"],
                                       segmented_button_selected_color=COLORS["accent"],
                                       segmented_button_selected_hover_color=COLORS["accent2"])
        self.tab_view.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.tab_results = self.tab_view.add("🏆  Resultados")
        self.tab_details = self.tab_view.add("🔍  Detalhes")
        self.tab_all = self.tab_view.add("📋  Todos")

      
        self.results_scroll = ctk.CTkScrollableFrame(self.tab_results, fg_color="transparent", corner_radius=0)
        self.results_scroll.pack(fill="both", expand=True)

       
        self.detail_scroll = ctk.CTkScrollableFrame(self.tab_details, fg_color="transparent", corner_radius=0)
        self.detail_scroll.pack(fill="both", expand=True)
        ctk.CTkLabel(self.detail_scroll, text="Clique em um celular nos Resultados para ver os detalhes.",
                     text_color=COLORS["text_muted"], font=ctk.CTkFont(size=13)).pack(pady=30)

      
        self.all_scroll = ctk.CTkScrollableFrame(self.tab_all, fg_color="transparent", corner_radius=0)
        self.all_scroll.pack(fill="both", expand=True)
        self._populate_all_phones()

        
        self._show_welcome()

    
    def _show_welcome(self):
        for w in self.results_scroll.winfo_children():
            w.destroy()

        frame = ctk.CTkFrame(self.results_scroll, fg_color="transparent")
        frame.pack(fill="both", expand=True, pady=20)

        ctk.CTkLabel(frame, text="📱", font=ctk.CTkFont(size=48)).pack()
        ctk.CTkLabel(frame, text="Bem-vindo ao PhoneAdvisor!",
                     font=ctk.CTkFont(size=18, weight="bold"), text_color=COLORS["accent"]).pack(pady=4)
        ctk.CTkLabel(frame, text="Configure seu orçamento e finalidade ao lado,\ndepois clique em 'Encontrar Meu Celular'.",
                     font=ctk.CTkFont(size=12), text_color=COLORS["text_muted"], justify="center").pack()

        tips_frame = ctk.CTkFrame(frame, fg_color=COLORS["bg_card2"], corner_radius=10)
        tips_frame.pack(pady=12, padx=30, fill="x")
        ctk.CTkLabel(tips_frame, text="💡  Dicas rápidas", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=COLORS["gold"]).pack(anchor="w", padx=12, pady=(8, 2))
        dicas = [
            "🎮  Para jogos: priorizamos processador e armazenamento",
            "📸  Para criação de conteúdo: câmera e processador em foco",
            "💼  Uso profissional: equilíbrio entre tudo + bateria",
            "📚  Estudos: bateria longa e armazenamento generoso",
            "⚖️  Selecione 2+ celulares nos resultados para comparar",
        ]
        for d in dicas:
            ctk.CTkLabel(tips_frame, text=d, font=ctk.CTkFont(size=11), text_color=COLORS["text_muted"],
                         anchor="w").pack(anchor="w", padx=12, pady=1)
        ctk.CTkFrame(tips_frame, fg_color="transparent", height=8).pack()

   
    def _on_price_change(self, val):
        v = int(float(val))
        self.price_display.configure(text=f"R$ {v:,.0f}".replace(",", "."))

    def _select_use(self, key):
        self.selected_use.set(key)
        for k, btn in self.use_btns.items():
            if k == key:
                btn.configure(fg_color=USE_CASES[k]["color"])
            else:
                btn.configure(fg_color=COLORS["bg_dark"])
        
        if not self._use_custom_weights.get():
            self._load_preset_weights(key)
        self._refresh_weight_sliders()

    def _load_preset_weights(self, use_key):
        w = USE_CASES[use_key]["weights"]
        self.w_processor.set(int(w["processor_score"] * 100))
        self.w_battery.set(int(w["battery_score"] * 100))
        self.w_camera.set(int(w["camera_score"] * 100))
        self.w_storage.set(int(w["storage_score"] * 100))

    def _on_custom_toggle(self):
        if not self._use_custom_weights.get():
            
            self._load_preset_weights(self.selected_use.get())
        self._refresh_weight_sliders()

    def _on_weight_slide(self, val, lbl, var_ref):
        v = int(float(val))
        var_ref.set(v)
        lbl.configure(text=f"{v}%")
        self._update_total_label()

    def _update_total_label(self):
        total = self.w_processor.get() + self.w_battery.get() + self.w_camera.get() + self.w_storage.get()
        ok = abs(total - 100) <= 5
        color = COLORS["green"] if ok else COLORS["red"]
        icon = "✅" if ok else "⚠️"
        self.total_label.configure(text=f"Total: {total}%  {icon}", text_color=color)

    def _refresh_weight_sliders(self):
        is_custom = self._use_custom_weights.get()
        state = "normal" if is_custom else "disabled"
        hint = "Pesos personalizados ativos" if is_custom else "Baseado no uso selecionado"
        self.preset_hint.configure(text=hint)
        for sl in self.weight_sliders.values():
            sl.configure(state=state)
       
        labels_map = {
            "🔥 Desempenho": self.w_processor,
            "📸 Câmera":     self.w_camera,
            "🔋 Bateria":    self.w_battery,
            "💾 Armazen.":   self.w_storage,
        }
        for label, var in labels_map.items():
            self.weight_value_labels[label].configure(text=f"{var.get()}%")
        self._update_total_label()

    def _get_active_weights(self):
        """Retorna os pesos normalizados para uso no score."""
        raw = {
            "processor_score": self.w_processor.get(),
            "battery_score":   self.w_battery.get(),
            "camera_score":    self.w_camera.get(),
            "storage_score":   self.w_storage.get(),
        }
        total = sum(raw.values()) or 100
        return {k: v / total for k, v in raw.items()}

  
    def _run_search(self):
        price = self.price_var.get()
        use = self.selected_use.get()
        custom_weights = self._get_active_weights()
        self.results = get_recommendations(price, use, top_n=5, custom_weights=custom_weights)
        self.comparing = []
        self._update_compare_label()
        self._show_results()
        self.tab_view.set("🏆  Resultados")

    def _show_results(self):
        for w in self.results_scroll.winfo_children():
            w.destroy()

        if not self.results:
            ctk.CTkLabel(self.results_scroll, text="😔  Nenhum celular encontrado neste orçamento.",
                         font=ctk.CTkFont(size=16), text_color=COLORS["text_muted"]).pack(pady=60)
            return

        use = self.selected_use.get()
        use_info = USE_CASES[use]

      
        hdr = ctk.CTkFrame(self.results_scroll, fg_color=COLORS["bg_card2"], corner_radius=10)
        hdr.pack(fill="x", padx=4, pady=(4, 6))
        ctk.CTkLabel(hdr, text=f"🏆  Top {len(self.results)} para {use_info['label']}",
                     font=ctk.CTkFont(size=14, weight="bold"), text_color=COLORS["accent"]).pack(side="left", padx=12, pady=7)
        ctk.CTkLabel(hdr, text=f"R$ {self.price_var.get():,.0f}".replace(",", "."),
                     font=ctk.CTkFont(size=12), text_color=COLORS["text_muted"]).pack(side="right", padx=12)

        for i, (phone, score) in enumerate(self.results):
            self._create_result_card(i, phone, score, use)

    def _create_result_card(self, rank, phone, score, use):
        medal_color = MEDAL_COLORS[rank] if rank < len(MEDAL_COLORS) else COLORS["text_muted"]
        is_top = rank == 0

        card = ctk.CTkFrame(
            self.results_scroll,
            fg_color=COLORS["bg_card2"] if not is_top else "#0D2240",
            corner_radius=12,
            border_width=2 if is_top else 1,
            border_color=COLORS["accent"] if is_top else COLORS["border"]
        )
        card.pack(fill="x", padx=4, pady=3)

       
        top_row = ctk.CTkFrame(card, fg_color="transparent")
        top_row.pack(fill="x", padx=10, pady=(8, 2))

        rank_label = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][rank]
        ctk.CTkLabel(top_row, text=rank_label, font=ctk.CTkFont(size=22)).pack(side="left")

        name_frame = ctk.CTkFrame(top_row, fg_color="transparent")
        name_frame.pack(side="left", padx=8)

        if is_top:
            ctk.CTkLabel(name_frame, text="⭐ MELHOR ESCOLHA", font=ctk.CTkFont(size=9, weight="bold"),
                         text_color=COLORS["gold"]).pack(anchor="w")

        ctk.CTkLabel(name_frame, text=phone["name"], font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(name_frame, text=phone["brand"] + "  •  " + phone["specs"]["os"],
                     font=ctk.CTkFont(size=10), text_color=COLORS["text_muted"]).pack(anchor="w")

        
        right = ctk.CTkFrame(top_row, fg_color="transparent")
        right.pack(side="right")

        score_color = COLORS["green"] if score >= 85 else COLORS["gold"] if score >= 70 else COLORS["accent3"]
        ctk.CTkLabel(right, text=f"{score:.0f}pts", font=ctk.CTkFont(size=19, weight="bold"),
                     text_color=score_color).pack(anchor="e")
        ctk.CTkLabel(right, text=f"R$ {phone['price']:,.0f}".replace(",", "."),
                     font=ctk.CTkFont(size=12, weight="bold"), text_color=COLORS["accent"]).pack(anchor="e")

      
        bars_frame = ctk.CTkFrame(card, fg_color="transparent")
        bars_frame.pack(fill="x", padx=10, pady=2)

        specs_to_show = [
            ("🔥 Desemp.", phone["specs"]["processor_score"], COLORS["red"]),
            ("📸 Câmera", phone["specs"]["camera_score"], COLORS["accent"]),
            ("🔋 Bateria", phone["specs"]["battery_score"], COLORS["green"]),
            ("💾 Armazen.", min(100, int(phone["specs"]["storage_gb"] / 512 * 100)), COLORS["accent2"]),
        ]

        for i, (label, val, color) in enumerate(specs_to_show):
            col = ctk.CTkFrame(bars_frame, fg_color="transparent")
            col.pack(side="left", expand=True, fill="x", padx=3)
            ctk.CTkLabel(col, text=label, font=ctk.CTkFont(size=9), text_color=COLORS["text_muted"]).pack(anchor="w")
            prog = ctk.CTkProgressBar(col, height=6, progress_color=color, fg_color=COLORS["bg_dark"])
            prog.pack(fill="x", pady=1)
            prog.set(val / 100)
            ctk.CTkLabel(col, text=f"{val}", font=ctk.CTkFont(size=9, weight="bold"),
                         text_color=COLORS["text"]).pack(anchor="w")

     
        if is_top and phone.get("highlights"):
            high_frame = ctk.CTkFrame(card, fg_color=COLORS["bg_dark"], corner_radius=6)
            high_frame.pack(fill="x", padx=10, pady=(4, 2))
            ctk.CTkLabel(high_frame, text="✨ Por que foi escolhido:", font=ctk.CTkFont(size=10, weight="bold"),
                         text_color=COLORS["gold"]).pack(anchor="w", padx=8, pady=(4, 1))
            for h in phone["highlights"][:3]:
                ctk.CTkLabel(high_frame, text=f"  • {h}", font=ctk.CTkFont(size=10),
                             text_color=COLORS["text_muted"], anchor="w").pack(anchor="w", padx=8, pady=1)
            ctk.CTkFrame(high_frame, fg_color="transparent", height=4).pack()
            
       
        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=10, pady=(4, 8))

        ctk.CTkButton(btn_row, text="🔍 Ver Detalhes", width=120, height=28, corner_radius=6,
                      fg_color=COLORS["accent"], hover_color=COLORS["accent2"], text_color="#000",
                      font=ctk.CTkFont(size=10, weight="bold"),
                      command=lambda p=phone, s=score, u=use: self._show_detail(p, s, u)
                      ).pack(side="left", padx=(0, 8))

      
        var = ctk.BooleanVar(value=phone["name"] in [c["name"] for c in self.comparing])
        chk = ctk.CTkCheckBox(btn_row, text="⚖️ Comparar", variable=var, font=ctk.CTkFont(size=10),
                              text_color=COLORS["text_muted"], checkbox_width=16, checkbox_height=16,
                              fg_color=COLORS["accent3"], hover_color=COLORS["accent3"],
                              command=lambda p=phone, v=var: self._toggle_compare(p, v))
        chk.pack(side="left")

    def _toggle_compare(self, phone, var):
        if var.get():
            if len(self.comparing) < 3:
                self.comparing.append(phone)
            else:
                var.set(False)
        else:
            self.comparing = [p for p in self.comparing if p["name"] != phone["name"]]
        self._update_compare_label()

    def _update_compare_label(self):
        if not self.comparing:
            self.compare_label.configure(text="Nenhum selecionado")
        else:
            names = ", ".join(p["name"].split()[-1] for p in self.comparing)
            self.compare_label.configure(text=f"{len(self.comparing)} selecionados: {names}")

   
    def _show_detail(self, phone, score, use):
        for w in self.detail_scroll.winfo_children():
            w.destroy()

        self.tab_view.set("🔍  Detalhes")

       
        hdr = ctk.CTkFrame(self.detail_scroll, fg_color=phone["image_color"], corner_radius=12)
        hdr.pack(fill="x", padx=4, pady=(4, 6))

       
        hdr_inner = ctk.CTkFrame(hdr, fg_color="transparent")
        hdr_inner.pack(fill="x", padx=16, pady=12)
        hdr_left = ctk.CTkFrame(hdr_inner, fg_color="transparent")
        hdr_left.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(hdr_left, text="📱", font=ctk.CTkFont(size=36)).pack(anchor="w")
        ctk.CTkLabel(hdr_left, text=phone["name"], font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="white").pack(anchor="w")
        ctk.CTkLabel(hdr_left, text=phone["brand"] + "  •  " + phone["specs"]["os"],
                     font=ctk.CTkFont(size=11), text_color="#AAAACC").pack(anchor="w")
        ctk.CTkLabel(hdr_left, text=f"Pontuação: {score:.0f} pts · {USE_CASES[use]['label']}",
                     font=ctk.CTkFont(size=11), text_color=COLORS["accent"]).pack(anchor="w", pady=(4, 0))
        hdr_right = ctk.CTkFrame(hdr_inner, fg_color="transparent")
        hdr_right.pack(side="right", anchor="e")
        ctk.CTkLabel(hdr_right, text=f"R$ {phone['price']:,.0f}".replace(",", "."),
                     font=ctk.CTkFont(size=22, weight="bold"), text_color=COLORS["gold"]).pack(anchor="e")

        
        two_col = ctk.CTkFrame(self.detail_scroll, fg_color="transparent")
        two_col.pack(fill="x", padx=4, pady=2)
        two_col.columnconfigure(0, weight=1)
        two_col.columnconfigure(1, weight=1)

       
        specs_frame = ctk.CTkFrame(two_col, fg_color=COLORS["bg_card2"], corner_radius=10)
        specs_frame.grid(row=0, column=0, padx=(0, 4), sticky="nsew")
        ctk.CTkLabel(specs_frame, text="📋 Especificações",
                     font=ctk.CTkFont(size=12, weight="bold"), text_color=COLORS["accent"]).pack(anchor="w", padx=10, pady=(8, 4))

        specs = phone["specs"]
        spec_items = [
            ("🔥 Processador", specs["processor"]),
            ("💾 RAM", f"{specs['ram_gb']} GB"),
            ("🗄️ Armazenamento", f"{specs['storage_gb']} GB"),
            ("📸 Câmera", f"{specs['camera_mp']} MP"),
            ("🔋 Bateria", f"{specs['battery_mah']} mAh"),
            ("📺 Display", specs["display"]),
            ("⚖️ Peso", f"{specs['weight_g']} g"),
            ("📡 5G", "Sim ✅" if specs.get("5g") else "Não ❌"),
        ]

        for label, val in spec_items:
            row_f = ctk.CTkFrame(specs_frame, fg_color=COLORS["bg_dark"], corner_radius=6)
            row_f.pack(fill="x", padx=8, pady=2)
            ctk.CTkLabel(row_f, text=label, font=ctk.CTkFont(size=10), text_color=COLORS["text_muted"], anchor="w").pack(side="left", padx=8, pady=4)
            ctk.CTkLabel(row_f, text=val, font=ctk.CTkFont(size=10, weight="bold"), text_color=COLORS["text"], anchor="e", wraplength=180).pack(side="right", padx=8, pady=4)
        ctk.CTkFrame(specs_frame, fg_color="transparent", height=6).pack()

        
        bars_frame = ctk.CTkFrame(two_col, fg_color=COLORS["bg_card2"], corner_radius=10)
        bars_frame.grid(row=0, column=1, padx=(4, 0), sticky="nsew")
        ctk.CTkLabel(bars_frame, text="📊 Pontuações",
                     font=ctk.CTkFont(size=12, weight="bold"), text_color=COLORS["accent"]).pack(anchor="w", padx=10, pady=(8, 4))

        bars_data = [
            ("🔥 Desempenho", specs["processor_score"], COLORS["red"]),
            ("📸 Câmera", specs["camera_score"], COLORS["accent"]),
            ("🔋 Bateria", specs["battery_score"], COLORS["green"]),
            ("💾 Armazenamento", min(100, int(specs["storage_gb"] / 512 * 100)), COLORS["accent2"]),
        ]

        for label, val, color in bars_data:
            row = ctk.CTkFrame(bars_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=3)
            lbl_row = ctk.CTkFrame(row, fg_color="transparent")
            lbl_row.pack(fill="x")
            ctk.CTkLabel(lbl_row, text=label, font=ctk.CTkFont(size=11), text_color=COLORS["text"], anchor="w").pack(side="left")
            ctk.CTkLabel(lbl_row, text=f"{val}/100", font=ctk.CTkFont(size=11, weight="bold"), text_color=color).pack(side="right")
            prog = ctk.CTkProgressBar(row, height=10, progress_color=color, fg_color=COLORS["bg_dark"], corner_radius=5)
            prog.pack(fill="x", pady=(2, 0))
            prog.set(val / 100)
        ctk.CTkFrame(bars_frame, fg_color="transparent", height=6).pack()

      
        why_frame = ctk.CTkFrame(self.detail_scroll, fg_color=COLORS["bg_card2"], corner_radius=10)
        why_frame.pack(fill="x", padx=4, pady=4)
        ctk.CTkLabel(why_frame, text=f"✨  Por que o {phone['name'].split()[0]} {phone['name'].split()[1]} é bom para {USE_CASES[use]['label']}?",
                     font=ctk.CTkFont(size=12, weight="bold"), text_color=COLORS["gold"]).pack(anchor="w", padx=10, pady=(8, 2))

        for h in phone.get("highlights", []):
            ctk.CTkLabel(why_frame, text=f"  ✅  {h}", font=ctk.CTkFont(size=11), text_color=COLORS["text"],
                         anchor="w", wraplength=700, justify="left").pack(anchor="w", padx=10, pady=1)
        ctk.CTkFrame(why_frame, fg_color="transparent", height=6).pack()

        
        pc_frame = ctk.CTkFrame(self.detail_scroll, fg_color="transparent")
        pc_frame.pack(fill="x", padx=4, pady=4)
        pc_frame.columnconfigure(0, weight=1)
        pc_frame.columnconfigure(1, weight=1)

        pros_frame = ctk.CTkFrame(pc_frame, fg_color=COLORS["bg_card2"], corner_radius=10)
        pros_frame.grid(row=0, column=0, padx=(0, 4), sticky="nsew")
        ctk.CTkLabel(pros_frame, text="✅  Pontos Fortes", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=COLORS["green"]).pack(anchor="w", padx=10, pady=(8, 4))
        for p in phone.get("pros", []):
            ctk.CTkLabel(pros_frame, text=f"  + {p}", font=ctk.CTkFont(size=11), text_color=COLORS["text"],
                         anchor="w", wraplength=300, justify="left").pack(anchor="w", padx=10, pady=1)
        ctk.CTkFrame(pros_frame, fg_color="transparent", height=6).pack()

        cons_frame = ctk.CTkFrame(pc_frame, fg_color=COLORS["bg_card2"], corner_radius=10)
        cons_frame.grid(row=0, column=1, padx=(4, 0), sticky="nsew")
        ctk.CTkLabel(cons_frame, text="⚠️  Pontos Fracos", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=COLORS["accent3"]).pack(anchor="w", padx=10, pady=(8, 4))
        for c in phone.get("cons", []):
            ctk.CTkLabel(cons_frame, text=f"  - {c}", font=ctk.CTkFont(size=11), text_color=COLORS["text"],
                         anchor="w", wraplength=300, justify="left").pack(anchor="w", padx=10, pady=1)
        ctk.CTkFrame(cons_frame, fg_color="transparent", height=6).pack()

        ctk.CTkFrame(self.detail_scroll, fg_color="transparent", height=10).pack()

    
    def _populate_all_phones(self):
        ctk.CTkLabel(self.all_scroll, text="📋  Todos os celulares disponíveis",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color=COLORS["accent"]).pack(anchor="w", padx=8, pady=(6, 2))

        sorted_phones = sorted(PHONES_DB, key=lambda p: p["price"])
        for phone in sorted_phones:
            card = ctk.CTkFrame(self.all_scroll, fg_color=COLORS["bg_card2"], corner_radius=8)
            card.pack(fill="x", padx=4, pady=2)

            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=6)

            ctk.CTkLabel(row, text="📱", font=ctk.CTkFont(size=18)).pack(side="left", padx=(0, 6))

            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left")
            ctk.CTkLabel(info, text=phone["name"], font=ctk.CTkFont(size=12, weight="bold"),
                         text_color=COLORS["text"]).pack(anchor="w")
            ctk.CTkLabel(info, text=f"{phone['specs']['processor']}  •  {phone['specs']['camera_mp']}MP  •  {phone['specs']['battery_mah']}mAh  •  {phone['specs']['storage_gb']}GB",
                         font=ctk.CTkFont(size=10), text_color=COLORS["text_muted"]).pack(anchor="w")

            ctk.CTkLabel(row, text=f"R$ {phone['price']:,.0f}".replace(",", "."),
                         font=ctk.CTkFont(size=14, weight="bold"), text_color=COLORS["gold"]).pack(side="right", padx=6)

    
    def _open_compare_window(self):
        if len(self.comparing) < 2:
            self._show_toast("Selecione pelo menos 2 celulares para comparar!")
            return

        win = ctk.CTkToplevel(self)
        win.title("⚖️  Comparação de Celulares")
        win.geometry("950x700")
        win.configure(fg_color=COLORS["bg_dark"])
        win.grab_set()

        ctk.CTkLabel(win, text="⚖️  Comparação Lado a Lado",
                     font=ctk.CTkFont(size=20, weight="bold"), text_color=COLORS["accent"]).pack(pady=(16, 4))

        scroll = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=16, pady=8)

        phones = self.comparing
        cols = len(phones) + 1

        
        for i, phone in enumerate(phones):
            f = ctk.CTkFrame(scroll, fg_color=phone["image_color"], corner_radius=12)
            f.grid(row=0, column=i + 1, padx=4, pady=4, sticky="ew")
            scroll.columnconfigure(i + 1, weight=1)
            ctk.CTkLabel(f, text="📱", font=ctk.CTkFont(size=32)).pack(pady=(10, 2))
            ctk.CTkLabel(f, text=phone["name"], font=ctk.CTkFont(size=13, weight="bold"),
                         text_color="white", wraplength=200, justify="center").pack(padx=8)
            ctk.CTkLabel(f, text=f"R$ {phone['price']:,.0f}".replace(",", "."),
                         font=ctk.CTkFont(size=15, weight="bold"), text_color=COLORS["gold"]).pack(pady=(2, 10))

        
        compare_rows = [
            ("Processador", lambda p: p["specs"]["processor"], None),
            ("Score Processador", lambda p: str(p["specs"]["processor_score"]) + "/100", "processor_score"),
            ("Câmera", lambda p: f"{p['specs']['camera_mp']} MP", None),
            ("Score Câmera", lambda p: str(p["specs"]["camera_score"]) + "/100", "camera_score"),
            ("Bateria", lambda p: f"{p['specs']['battery_mah']} mAh", None),
            ("Score Bateria", lambda p: str(p["specs"]["battery_score"]) + "/100", "battery_score"),
            ("Armazenamento", lambda p: f"{p['specs']['storage_gb']} GB", None),
            ("RAM", lambda p: f"{p['specs']['ram_gb']} GB", None),
            ("Display", lambda p: p["specs"]["display"], None),
            ("Sistema", lambda p: p["specs"]["os"], None),
            ("5G", lambda p: "✅" if p["specs"].get("5g") else "❌", None),
            ("Peso", lambda p: f"{p['specs']['weight_g']} g", None),
        ]

        for row_i, (label, fn, score_key) in enumerate(compare_rows):
            r = row_i + 1
            bg = COLORS["bg_card2"] if row_i % 2 == 0 else COLORS["bg_dark"]

            label_frame = ctk.CTkFrame(scroll, fg_color=bg, corner_radius=8)
            label_frame.grid(row=r, column=0, padx=2, pady=1, sticky="ew")
            scroll.columnconfigure(0, weight=1)
            ctk.CTkLabel(label_frame, text=label, font=ctk.CTkFont(size=12, weight="bold"),
                         text_color=COLORS["text_muted"]).pack(padx=10, pady=6)

            vals = [p["specs"].get(score_key, 0) for p in phones] if score_key else []

            for col_i, phone in enumerate(phones):
                val_str = fn(phone)
                cell_bg = bg

                if score_key and vals:
                    numeric_val = phone["specs"].get(score_key, 0)
                    if numeric_val == max(vals):
                        cell_bg = "#1A2E40"

                cell = ctk.CTkFrame(scroll, fg_color=cell_bg, corner_radius=8)
                cell.grid(row=r, column=col_i + 1, padx=2, pady=1, sticky="ew")

                color = COLORS["text"]
                if score_key and vals:
                    numeric_val = phone["specs"].get(score_key, 0)
                    if numeric_val == max(vals):
                        color = COLORS["green"]

                ctk.CTkLabel(cell, text=val_str, font=ctk.CTkFont(size=12), text_color=color).pack(padx=8, pady=6)

        ctk.CTkLabel(scroll, text="✅ Verde = melhor resultado neste critério", font=ctk.CTkFont(size=11),
                     text_color=COLORS["text_muted"]).grid(row=len(compare_rows) + 2, column=0, columnspan=cols, pady=12)

   
    def _save_profile_dialog(self):
        dialog = ctk.CTkInputDialog(text="Nome do perfil:", title="Salvar Perfil")
        name = dialog.get_input()
        if name and name.strip():
            name = name.strip()
            profile_data = {
                "name": name,
                "price": self.price_var.get(),
                "use_case": self.selected_use.get(),
                "saved_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "results": [(p["name"], round(s, 1)) for p, s in self.results],
                "custom_weights": {
                    "processor_score": self.w_processor.get(),
                    "battery_score":   self.w_battery.get(),
                    "camera_score":    self.w_camera.get(),
                    "storage_score":   self.w_storage.get(),
                },
                "use_custom": self._use_custom_weights.get(),
            }
            self.profiles[name] = profile_data
            save_profiles(self.profiles)
            self.current_profile = name
            self.profile_label.configure(text=f"📂 {name}", text_color=COLORS["accent"])
            self._show_toast(f"Perfil '{name}' salvo com sucesso!")

    def _open_profiles_dialog(self):
        win = ctk.CTkToplevel(self)
        win.title("📂  Perfis Salvos")
        win.geometry("500x450")
        win.configure(fg_color=COLORS["bg_dark"])
        win.grab_set()

        ctk.CTkLabel(win, text="📂  Perfis Salvos", font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=COLORS["accent"]).pack(pady=16)

        scroll = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=16, pady=8)

        if not self.profiles:
            ctk.CTkLabel(scroll, text="Nenhum perfil salvo ainda.", text_color=COLORS["text_muted"],
                         font=ctk.CTkFont(size=14)).pack(pady=40)
        else:
            for pname, pdata in self.profiles.items():
                card = ctk.CTkFrame(scroll, fg_color=COLORS["bg_card2"], corner_radius=12)
                card.pack(fill="x", pady=4)

                ctk.CTkLabel(card, text=f"👤  {pname}", font=ctk.CTkFont(size=14, weight="bold"),
                             text_color=COLORS["text"]).pack(anchor="w", padx=12, pady=(10, 2))
                ctk.CTkLabel(card, text=f"Orçamento: R$ {pdata['price']:,.0f}  •  Uso: {USE_CASES[pdata['use_case']]['label']}  •  {pdata['saved_at']}".replace(",", "."),
                             font=ctk.CTkFont(size=11), text_color=COLORS["text_muted"]).pack(anchor="w", padx=12, pady=2)

                if pdata.get("results"):
                    results_text = "  ".join([f"#{i+1} {r[0].split()[0]} {r[0].split()[-1]}" for i, r in enumerate(pdata["results"][:3])])
                    ctk.CTkLabel(card, text=f"Resultados: {results_text}", font=ctk.CTkFont(size=11),
                                 text_color=COLORS["accent"]).pack(anchor="w", padx=12, pady=2)

                btn_row = ctk.CTkFrame(card, fg_color="transparent")
                btn_row.pack(fill="x", padx=12, pady=(4, 10))

                ctk.CTkButton(btn_row, text="▶  Carregar", width=110, height=30, corner_radius=8,
                              fg_color=COLORS["accent"], text_color="#000",
                              command=lambda pd=pdata, w=win: self._load_profile(pd, w)
                              ).pack(side="left", padx=(0, 6))

                ctk.CTkButton(btn_row, text="🗑  Excluir", width=90, height=30, corner_radius=8,
                              fg_color=COLORS["red"], hover_color="#CC2222",
                              command=lambda pn=pname, w=win: self._delete_profile(pn, w)
                              ).pack(side="left")

    def _load_profile(self, pdata, win):
        self.price_var.set(pdata["price"])
        self._on_price_change(pdata["price"])
        self._select_use(pdata["use_case"])
        # Restaura pesos salvos, se existirem
        if pdata.get("use_custom") and pdata.get("custom_weights"):
            cw = pdata["custom_weights"]
            self.w_processor.set(cw.get("processor_score", 40))
            self.w_battery.set(cw.get("battery_score", 25))
            self.w_camera.set(cw.get("camera_score", 10))
            self.w_storage.set(cw.get("storage_score", 25))
            self._use_custom_weights.set(True)
        else:
            self._use_custom_weights.set(False)
            self._load_preset_weights(pdata["use_case"])
        self._refresh_weight_sliders()
        self.current_profile = pdata["name"]
        self.profile_label.configure(text=f"📂 {pdata['name']}", text_color=COLORS["accent"])
        win.destroy()
        self._run_search()

    def _delete_profile(self, pname, win):
        if pname in self.profiles:
            del self.profiles[pname]
            save_profiles(self.profiles)
            win.destroy()
            self._open_profiles_dialog()

   
        toast = ctk.CTkToplevel(self)
        toast.overrideredirect(True)
        toast.configure(fg_color=COLORS["bg_card2"])
        ctk.CTkLabel(toast, text=msg, font=ctk.CTkFont(size=13), text_color=COLORS["text"],
                     padx=20, pady=12).pack()
        x = self.winfo_x() + self.winfo_width() // 2 - 180
        y = self.winfo_y() + self.winfo_height() - 80
        toast.geometry(f"360x44+{x}+{y}")
        toast.after(2500, toast.destroy)



    app = PhoneAdvisorApp()
    app.mainloop()
