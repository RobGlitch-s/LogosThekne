import json
import os
import sys
from pathlib import Path
from io import BytesIO

import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageDraw

BASE_DIR = Path(
    sys._MEIPASS if getattr(sys, "_MEIPASS", None)
    else Path(__file__).resolve().parent
)

def resource_path(relative_path: str) -> Path:
    return BASE_DIR / "assets" / relative_path


CAMINHO_LOGO = resource_path("robo_logo.png")
CAMINHO_ROBO = resource_path("robo.png")
CAMINHO_TERCEIRAPAG = resource_path("robo.png")

LARGURA_CONTAINER = 460
ALTURA_CONTAINER = 600
LARGURA_PROGRESSO = 260
ALTURA_AREA_IMAGEM = 180
POSICAO_VERTICAL_CONTAINER = 0.54

CONFIG_FILE = Path("config.json")

# =====================================================
# 🔥 PALETA DE CORES — MODO CLARO / ESCURO
# =====================================================
# Cores "estruturais" (fundo, cartões, texto, bordas) mudam
# conforme o tema. Cores de destaque (azul da marca) e cores
# de status (verde/vermelho de acerto/erro) ficam iguais nos
# dois temas, para manter a identidade visual do app.

CORES = {
    "dark": {
        "bg":               "#0f172a",
        "bg_card":          "#111827",
        "bg_input":         "#1e293b",
        "bg_hover":         "#1e3a5f",
        "borda":            "#334155",
        "texto":            "#f8fafc",
        "texto_secundario": "#94a3b8",
        "texto_apagado":    "#64748b",
    },
    "light": {
        "bg":               "#f1f5f9",
        "bg_card":          "#ffffff",
        "bg_input":         "#e2e8f0",
        "bg_hover":         "#dbeafe",
        "borda":            "#cbd5e1",
        "texto":            "#0f172a",
        "texto_secundario": "#475569",
        "texto_apagado":    "#64748b",
    },
}

def carregar_tema():
    """Lê o arquivo de configuração e retorna o tema salvo. 
    Se o arquivo não existir, retorna 'dark' como padrão."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                dados = json.load(f)
                return dados.get("tema", "dark")
        except Exception as e:
            print(f"Erro ao ler o arquivo de configuração: {e}")
            return "dark"
    return "dark"

def salvar_tema(tema):
    """Salva o tema escolhido pelo usuário no arquivo JSON."""
    dados = {"tema": tema}
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4)
        print(f"Tema '{tema}' salvo com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar o arquivo de configuração: {e}")

def obter_cores(tema: str = "dark") -> dict:
    """Retorna a paleta de cores do tema atual (dark/light)."""
    return CORES.get(tema, CORES["dark"])


# =====================================================
# LOGO
# =====================================================

def adicionar_logo(parent, caminho_logo):

    logo_outer = ctk.CTkFrame(
        parent,
        fg_color="#111827",
        corner_radius=14,
        border_width=2,
        border_color="#2563eb"
    )

    logo_outer.place(x=12, y=10)

    logo_frame = ctk.CTkFrame(
        logo_outer,
        fg_color="transparent"
    )

    logo_frame.pack(padx=10, pady=6)

    try:
        logo_img = Image.open(caminho_logo)

        logo_ctk = ctk.CTkImage(
            light_image=logo_img,
            size=(42, 42)
        )

        ctk.CTkLabel(
            logo_frame,
            image=logo_ctk,
            text=""
        ).pack(side="left", padx=(0, 8))

        logo_outer._logo_img_ref = logo_ctk

    except Exception as e:
        print("ERRO LOGO:", e)

    ctk.CTkLabel(
        logo_frame,
        text="Logos",
        font=("Poppins", 26, "bold"),
        text_color="#ffffff"
    ).pack(side="left")

    ctk.CTkLabel(
        logo_frame,
        text="Thekne",
        font=("Poppins", 26, "bold"),
        text_color="#2563eb"
    ).pack(side="left")


# =====================================================
# BOTÃO REGISTRO
# =====================================================

def adicionar_registro(parent, command=None, texto="Registrar"):

    botao_outer = ctk.CTkFrame(
        parent,
        fg_color="#111827",
        corner_radius=14,
        border_width=2,
        border_color="#2563eb"
    )

    botao_outer.place(relx=0.96, y=45, anchor="e")

    botao_frame = ctk.CTkFrame(
        botao_outer,
        fg_color="transparent"
    )

    botao_frame.pack(padx=10, pady=6)

    botao_registro = ctk.CTkButton(
        botao_frame,
        text=texto,
        width=120,
        height=30,
        corner_radius=10,
        fg_color="transparent",
        hover_color="#1e3a5f",
        text_color="#2563eb",
        font=("Poppins", 12, "bold"),
        command=command
    )

    botao_registro.pack()

    return botao_registro

# =====================================================
# 🔥 HELPER — foto circular
# =====================================================

def fazer_foto_circular(caminho: str, tamanho: int) -> ctk.CTkImage:
    img = Image.open(caminho).convert("RGBA").resize((tamanho, tamanho), Image.LANCZOS)

    mascara = Image.new("L", (tamanho, tamanho), 0)
    draw = ImageDraw.Draw(mascara)
    draw.ellipse((0, 0, tamanho - 1, tamanho - 1), fill=255)  # Corrigido: tamanho - 1

    resultado = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))
    resultado.paste(img, mask=mascara)

    return ctk.CTkImage(light_image=resultado, size=(tamanho, tamanho))


def fazer_placeholder_circular(tamanho: int) -> ctk.CTkImage:
    img = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Desenhar o círculo de fundo com RGBA ( Converter HEX para RGBA)
    draw.ellipse((0, 0, tamanho - 1, tamanho - 1), fill=(30, 58, 95))  # #1e3a5f em RGB

    cx, cy = tamanho // 2, tamanho // 2
    r_cabeca = tamanho // 6
    
    # Cabeça
    draw.ellipse(
        (cx - r_cabeca, cy - r_cabeca - tamanho // 8,
         cx + r_cabeca, cy + r_cabeca - tamanho // 8),
        fill=(148, 163, 184)  # #94a3b8 em RGB
    )
    
    # Corpo
    draw.ellipse(
        (cx - tamanho // 3, cy + tamanho // 8,
         cx + tamanho // 3, cy + tamanho // 2),
        fill=(148, 163, 184)  # #94a3b8 em RGB
    )

    return ctk.CTkImage(light_image=img, size=(tamanho, tamanho))

def bytes_para_imagem(foto_blob, tamanho):
    
    if not foto_blob:
        return None
    try:
        img = Image.open(BytesIO(foto_blob)).convert("RGBA").resize((tamanho, tamanho), Image.LANCZOS)
        return img
    except Exception as e:
        print("ERRO AO CONVERTER FOTO:", e)
        return None

def blob_para_foto_circular(foto_blob, tamanho):

    if not foto_blob:
        return None

    img = Image.open(
        BytesIO(foto_blob)
    ).convert("RGBA")

    img = img.resize(
        (tamanho, tamanho),
        Image.LANCZOS
    )

    mascara = Image.new(
        "L",
        (tamanho, tamanho),
        0
    )

    draw = ImageDraw.Draw(mascara)

    draw.ellipse(
        (0, 0, tamanho - 1, tamanho - 1),
        fill=255
    )

    resultado = Image.new(
        "RGBA",
        (tamanho, tamanho),
        (0, 0, 0, 0)
    )

    resultado.paste(
        img,
        mask=mascara
    )

    return ctk.CTkImage(
        light_image=resultado,
        size=(tamanho, tamanho)
    )


# =====================================================
# 🔥 SPINNER DE CARREGAMENTO (indicador animado)
# =====================================================

def criar_spinner(parent, cores, tamanho=48, espessura=5, cor_ativa="#2563eb"):
    """
    Cria um indicador de carregamento animado: um arco que gira sem
    parar num Canvas, usado nas telas que esperam a IA responder
    (gerar pergunta, gerar aula, etc.) ou em qualquer transição de
    tela que precise de um retorno visual de "carregando".

    Uso:
        spinner, iniciar, parar = criar_spinner(parent, self.cores)
        spinner.pack(pady=10)
        iniciar()
        # ... quando a tela for trocada/destruída:
        parar()

    Retorna (canvas, iniciar, parar).
    """
    canvas = tk.Canvas(
        parent, width=tamanho, height=tamanho,
        bg=cores["bg"], highlightthickness=0, bd=0
    )

    canvas.create_oval(
        espessura, espessura, tamanho - espessura, tamanho - espessura,
        outline=cores["bg_input"], width=espessura
    )

    arco = canvas.create_arc(
        espessura, espessura, tamanho - espessura, tamanho - espessura,
        start=0, extent=90, style="arc", outline=cor_ativa, width=espessura
    )

    estado = {"angulo": 0, "rodando": False}

    def _animar():
        if not estado["rodando"]:
            return
        try:
            if not canvas.winfo_exists():
                return
            estado["angulo"] = (estado["angulo"] - 12) % 360
            canvas.itemconfig(arco, start=estado["angulo"])
            canvas.after(30, _animar)
        except Exception:
            pass

    def iniciar():
        estado["rodando"] = True
        _animar()

    def parar():
        estado["rodando"] = False

    return canvas, iniciar, parar