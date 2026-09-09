print("Carregando MainScreen...")

import sys
import os
import math
import random
import threading
import importlib.util
from pathlib import Path

# ── Raiz do projeto
_RAIZ = Path(__file__).resolve().parent.parent

if str(_RAIZ) not in sys.path:
    sys.path.insert(0, str(_RAIZ))

# ── Importa ia.py
_ia_path = _RAIZ / "ia.py"
_ia_spec  = importlib.util.spec_from_file_location("ia", _ia_path)
_ia_mod   = importlib.util.module_from_spec(_ia_spec)
_ia_spec.loader.exec_module(_ia_mod)
gerar_pergunta         = _ia_mod.gerar_pergunta
verificar_resposta     = _ia_mod.verificar_resposta
obter_resposta_correta = _ia_mod.obter_resposta_correta
gerar_licao            = _ia_mod.gerar_licao

import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk
from database import *
from utils import *
import sons
from idioma import t, traduzir_nivel, traduzir_materia, traduzir_missao_titulo, traduzir_missao_descricao

print("MainScreen encontrada com sucesso!")


# =====================================================
# 🔥 HELPER — IMAGENS DO ROBÔ (REAÇÕES)
# =====================================================

def _carregar_robo_reacao(nome_arquivo, tamanho=100):
    """
    Carrega uma imagem do robô mascote (pasta assets/rosa) para usar
    dentro de um tk.Canvas (animação de pular / trocar de expressão).
    Retorna um ImageTk.PhotoImage ou None se o arquivo não existir.
    """
    caminho = BASE_DIR / "assets" / "rosa" / nome_arquivo
    try:
        img = Image.open(caminho).convert("RGBA")
        img.thumbnail((tamanho, tamanho), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Erro ao carregar robô '{nome_arquivo}':", e)
        return None


# =====================================================
# 🔥 ANIMAÇÃO DE NÍVEL
# =====================================================

class AnimacaoNivel(ctk.CTkToplevel):
    """Popup de animação que aparece quando o usuário sobe de nível."""

    def __init__(self, parent, controller, novo_nivel):
        super().__init__(parent)

        self.novo_nivel = novo_nivel
        self.controller = controller

        # janela sem borda, transparente, centralizada
        self.overrideredirect(True)
        self.configure(fg_color="#0f172a")
        self.attributes("-alpha", 0.0)
        self.attributes("-topmost", True)

        largura, altura = 420, 280

        # centraliza na tela
        self.update_idletasks()
        larg_tela = self.winfo_screenwidth()
        alt_tela  = self.winfo_screenheight()
        x = (larg_tela // 2) - (largura // 2)
        y = (alt_tela  // 2) - (altura  // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")

        # card principal
        card = ctk.CTkFrame(
            self,
            fg_color="#111827",
            corner_radius=24,
            border_width=2,
            border_color="#22c55e"
        )
        card.pack(fill="both", expand=True, padx=4, pady=4)

        ctk.CTkLabel(
            card, text="⬆️",
            font=("Segoe UI Emoji", 52)
        ).pack(pady=(30, 8))

        ctk.CTkLabel(
            card,
            text=t(controller, "subida_titulo"),
            font=("Poppins", 22, "bold"),
            text_color="#22c55e"
        ).pack()

        ctk.CTkLabel(
            card,
            text=t(controller, "subida_texto", nivel=novo_nivel),
            font=("Poppins", 14),
            text_color="#94a3b8"
        ).pack(pady=(6, 0))

        ctk.CTkLabel(
            card,
            text=t(controller, "subida_rodape"),
            font=("Poppins", 13),
            text_color="#64748b"
        ).pack(pady=(4, 30))

        # inicia fade in
        self._fade_in()

    def _fade_in(self, alpha=0.0):
        alpha += 0.08
        if alpha <= 1.0:
            self.attributes("-alpha", alpha)
            self.after(20, self._fade_in, alpha)
        else:
            self.attributes("-alpha", 1.0)
            # fica 2.5s e some
            self.after(2500, self._fade_out)

    def _fade_out(self, alpha=1.0):
        alpha -= 0.08
        if alpha >= 0.0:
            self.attributes("-alpha", alpha)
            self.after(20, self._fade_out, alpha)
        else:
            self.destroy()


# =====================================================
# 🔥 SELETOR DE AVATARES
# =====================================================

class SeletorAvatar(ctk.CTkToplevel):
    def __init__(self, parent, ao_selecionar, controller=None):
        super().__init__(parent)

        self.ao_selecionar = ao_selecionar
        self.controller = controller

        self.title(t(controller, "seletor_avatar_titulo"))
        self.geometry("520x580")
        self.configure(fg_color="#0f172a")
        self.grab_set()
        self.resizable(False, False)

        ctk.CTkLabel(
            self,
            text=t(controller, "seletor_avatar_titulo"),
            font=("Poppins", 20, "bold"),
            text_color="#f8fafc"
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            self,
            text=t(controller, "seletor_avatar_subtitulo"),
            font=("Poppins", 12),
            text_color="#64748b"
        ).pack(pady=(0, 12))

        abas = ctk.CTkFrame(self, fg_color="transparent")
        abas.pack(pady=(0, 12))

        self.btn_rosa = ctk.CTkButton(
            abas, text=t(controller, "seletor_avatar_rosa"),
            width=120, height=36, corner_radius=10,
            fg_color="#2563eb", hover_color="#1d4ed8",
            text_color="#ffffff", font=("Poppins", 13, "bold"),
            command=lambda: self.trocar_aba("rosa")
        )
        self.btn_rosa.pack(side="left", padx=5)

        self.btn_azul = ctk.CTkButton(
            abas, text=t(controller, "seletor_avatar_azul"),
            width=120, height=36, corner_radius=10,
            fg_color="#1e293b", hover_color="#1e3a5f",
            text_color="#94a3b8", font=("Poppins", 13, "bold"),
            command=lambda: self.trocar_aba("azul")
        )
        self.btn_azul.pack(side="left", padx=5)

        self.frame_scroll = ctk.CTkScrollableFrame(
            self, fg_color="#111827", corner_radius=16
        )
        self.frame_scroll.pack(padx=20, pady=(0, 20), fill="both", expand=True)

        for col in range(4):
            self.frame_scroll.grid_columnconfigure(col, weight=1, uniform="col")

        self.trocar_aba("rosa")

    def trocar_aba(self, aba):
        if aba == "rosa":
            self.btn_rosa.configure(fg_color="#2563eb", text_color="#ffffff")
            self.btn_azul.configure(fg_color="#1e293b", text_color="#94a3b8")
        else:
            self.btn_azul.configure(fg_color="#2563eb", text_color="#ffffff")
            self.btn_rosa.configure(fg_color="#1e293b", text_color="#94a3b8")

        for widget in self.frame_scroll.winfo_children():
            widget.destroy()

        for col in range(4):
            self.frame_scroll.grid_columnconfigure(col, weight=1, uniform="col")

        pasta = BASE_DIR / "assets" / aba

        if not pasta.exists():
            texto_erro = f"Folder '{aba}' not found." if getattr(self.controller, "idioma", "pt") == "en" else f"Pasta '{aba}' não encontrada."
            ctk.CTkLabel(
                self.frame_scroll,
                text=texto_erro,
                font=("Poppins", 13), text_color="#ef4444"
            ).grid(row=0, column=0, columnspan=4, pady=20)
            return

        arquivos = sorted(pasta.glob("*.png"))

        if not arquivos:
            texto_vazio = "No avatars found." if getattr(self.controller, "idioma", "pt") == "en" else "Nenhum avatar encontrado."
            ctk.CTkLabel(
                self.frame_scroll,
                text=texto_vazio,
                font=("Poppins", 13), text_color="#64748b"
            ).grid(row=0, column=0, columnspan=4, pady=20)
            return

        self._refs = []
        colunas = 4

        for i, caminho in enumerate(arquivos):
            linha = i // colunas
            col   = i % colunas

            try:
                img = Image.open(caminho).convert("RGBA").resize((85, 85), Image.LANCZOS)

                mascara = Image.new("L", (85, 85), 0)
                draw = ImageDraw.Draw(mascara)
                draw.ellipse((0, 0, 84, 84), fill=255)
                resultado = Image.new("RGBA", (85, 85), (0, 0, 0, 0))
                resultado.paste(img, mask=mascara)

                ctk_img = ctk.CTkImage(light_image=resultado, size=(85, 85))
                self._refs.append(ctk_img)

                frame_item = ctk.CTkFrame(
                    self.frame_scroll, fg_color="#1e293b",
                    corner_radius=12, cursor="hand2",
                    width=100, height=100
                )
                frame_item.grid(row=linha, column=col, padx=8, pady=8, sticky="nsew")
                frame_item.pack_propagate(False)

                lbl_img = ctk.CTkLabel(frame_item, image=ctk_img, text="", cursor="hand2")
                lbl_img.place(relx=0.5, rely=0.5, anchor="center")

                def on_enter(e, f=frame_item):
                    f.configure(fg_color="#1e3a5f", border_width=2, border_color="#2563eb")

                def on_leave(e, f=frame_item):
                    f.configure(fg_color="#1e293b", border_width=0)

                frame_item.bind("<Enter>", on_enter)
                frame_item.bind("<Leave>", on_leave)
                lbl_img.bind("<Enter>",    on_enter)
                lbl_img.bind("<Leave>",    on_leave)

                frame_item.bind("<Button-1>", lambda e, p=caminho: self.selecionar(p))
                lbl_img.bind("<Button-1>",    lambda e, p=caminho: self.selecionar(p))

            except Exception as ex:
                print(f"Erro ao carregar {caminho.name}: {ex}")

    def selecionar(self, caminho):
        self.ao_selecionar(str(caminho))
        self.destroy()


# =====================================================
# 🔥 SELETOR DE DIFICULDADE (usado a partir do Perfil,
# ou quando o jogo sugere subir de nível)
# =====================================================

class SeletorDificuldade(ctk.CTkToplevel):
    def __init__(self, parent, controller, cores, nivel_atual, ao_confirmar):
        super().__init__(parent)
        self.title(t(controller, "seletor_dificuldade_titulo"))
        self.geometry("380x420")
        self.configure(fg_color=cores["bg"])
        self.resizable(False, False)
        self.grab_set()

        self.controller = controller
        self.cores = cores
        self.ao_confirmar = ao_confirmar
        self.nivel_escolhido = nivel_atual
        self.frames = {}

        ctk.CTkLabel(
            self, text=t(controller, "seletor_dificuldade_titulo"),
            font=("Poppins", 18, "bold"), text_color=cores["texto"]
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            self, text=t(controller, "seletor_dificuldade_subtitulo"),
            font=("Poppins", 12), text_color=cores["texto_secundario"]
        ).pack(pady=(0, 15))

        niveis = [
            ("Iniciante",     t(controller, "nivel_desc_Iniciante")),
            ("Intermediário", t(controller, "nivel_desc_Intermediário")),
            ("Avançado",      t(controller, "nivel_desc_Avançado")),
        ]

        for nome, descricao in niveis:
            selecionado = nome == nivel_atual

            frame = ctk.CTkFrame(
                self,
                fg_color=cores["bg_hover"] if selecionado else cores["bg_input"],
                corner_radius=16, border_width=1,
                border_color="#2563eb" if selecionado else cores["borda"],
                width=320, height=75, cursor="hand2"
            )
            frame.pack(pady=6)
            frame.pack_propagate(False)

            ctk.CTkLabel(
                frame, text=traduzir_nivel(controller, nome), font=("Poppins", 15, "bold"), text_color=cores["texto"]
            ).pack(anchor="w", padx=18, pady=(10, 0))

            ctk.CTkLabel(
                frame, text=descricao, font=("Poppins", 10),
                text_color=cores["texto_secundario"], wraplength=280, justify="left"
            ).pack(anchor="w", padx=18)

            self.frames[nome] = frame
            frame.bind("<Button-1>", lambda e, n=nome: self._selecionar(n))
            for filho in frame.winfo_children():
                filho.bind("<Button-1>", lambda e, n=nome: self._selecionar(n))

        ctk.CTkButton(
            self, text=t(controller, "seletor_dificuldade_confirmar"), width=200, height=42, corner_radius=12,
            fg_color="#2563eb", hover_color="#1d4ed8", font=("Poppins", 14, "bold"),
            command=self._confirmar
        ).pack(pady=(20, 20))

    def _selecionar(self, nome):
        self.nivel_escolhido = nome
        for n, frame in self.frames.items():
            selecionado = n == nome
            frame.configure(
                fg_color=self.cores["bg_hover"] if selecionado else self.cores["bg_input"],
                border_color="#2563eb" if selecionado else self.cores["borda"]
            )

    def _confirmar(self):
        self.destroy()
        self.ao_confirmar(self.nivel_escolhido)


# =====================================================
# 🔥 MAIN SCREEN
# =====================================================

class MainScreen(ctk.CTkFrame):
    def __init__(self, parent, controller, nivel):
        self.cores = obter_cores(controller.tema_atual)
        super().__init__(parent, fg_color=self.cores["bg"])
        self.controller = controller
        self.nivel = nivel
        self.aba_ativa = "comecar"

        self.sidebar = ctk.CTkFrame(
            self, fg_color=self.cores["bg_card"], width=280,
            corner_radius=0, border_width=1, border_color=self.cores["bg_input"]
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo_outer = ctk.CTkFrame(
            self.sidebar, fg_color=self.cores["bg"],
            corner_radius=14, border_width=2, border_color="#2563eb"
        )
        logo_outer.pack(pady=(20, 5), padx=15, fill="x")

        logo_inner = ctk.CTkFrame(logo_outer, fg_color="transparent")
        logo_inner.pack(padx=12, pady=10)

        try:
            logo_img = Image.open(CAMINHO_LOGO)
            logo_ctk = ctk.CTkImage(light_image=logo_img, size=(38, 38))
            self._logo_ref = logo_ctk
            ctk.CTkLabel(logo_inner, image=logo_ctk, text="").pack(side="left", padx=(0, 10))
        except Exception as e:
            print("ERRO LOGO SIDEBAR:", e)

        ctk.CTkLabel(logo_inner, text="Logos", font=("Poppins", 20, "bold"), text_color="#ffffff").pack(side="left")
        ctk.CTkLabel(logo_inner, text="Thekne", font=("Poppins", 20, "bold"), text_color="#2563eb").pack(side="left")

        linha_badges = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        linha_badges.pack(pady=(8, 25), padx=20, anchor="w")

        ctk.CTkLabel(
            linha_badges, text=f"{t(controller, 'sidebar_nivel')}: {traduzir_nivel(controller, nivel) or 'N/A'}",
            font=("Poppins", 12), text_color=self.cores["texto_apagado"],
            fg_color=self.cores["bg_input"], corner_radius=8, padx=10, pady=4
        ).pack(side="left", padx=(0, 8))

        self.badge_moedas = ctk.CTkLabel(
            linha_badges, text=f"🪙  {obter_moedas(controller.usuario_id)}",
            font=("Poppins", 12, "bold"), text_color="#f59e0b",
            fg_color=self.cores["bg_input"], corner_radius=8, padx=10, pady=4
        )
        self.badge_moedas.pack(side="left")

        # deixa uma referência acessível para as páginas atualizarem
        # o saldo de moedas exibido aqui assim que o jogador resgatar algo
        self.controller.mainscreen_atual = self

        ctk.CTkFrame(self.sidebar, fg_color=self.cores["bg_input"], height=1).pack(fill="x", padx=15, pady=(0, 15))

        self.botoes_sidebar = {}
        nav_items = [
            ("comecar", t(controller, "nav_estudar")),
            ("cursos",  t(controller, "nav_cursos")),
            ("missoes", t(controller, "nav_missoes")),
            ("perfil",  t(controller, "nav_perfil")),
            ("config",  t(controller, "nav_config")),
        ]

        for chave, texto in nav_items:
            btn = ctk.CTkButton(
                self.sidebar, text=texto, font=("Poppins", 14, "bold"),
                anchor="w", width=240, height=46, corner_radius=12,
                fg_color="transparent", hover_color=self.cores["bg_hover"], text_color=self.cores["texto_secundario"],
                command=lambda c=chave: self.trocar_aba(c)
            )
            btn.pack(pady=4, padx=15)
            self.botoes_sidebar[chave] = btn

        ctk.CTkLabel(self.sidebar, text="v1.0.0", font=("Poppins", 11), text_color=self.cores["borda"]).pack(side="bottom", pady=20)

        self.area_conteudo = ctk.CTkFrame(self, fg_color=self.cores["bg"])
        self.area_conteudo.pack(side="left", fill="both", expand=True)

        self.frame_pagina = ctk.CTkFrame(self.area_conteudo, fg_color=self.cores["bg"])
        self.frame_pagina.pack(fill="both", expand=True)

        self.paginas = {}
        self.paginas["comecar"] = PaginaComecar(self.frame_pagina, self.nivel, self.controller)
        self.paginas["cursos"]  = PaginaCursos(self.frame_pagina, self.controller)
        self.paginas["missoes"] = PaginaMissoes(self.frame_pagina, self.controller)
        self.paginas["perfil"]  = PaginaPerfil(self.frame_pagina, self.controller)
        self.paginas["config"]  = PaginaConfiguracoes(self.frame_pagina, self.controller)

        self.trocar_aba(self.controller.aba_atual)

    def trocar_aba(self, chave):
        self.aba_ativa = chave
        self.controller.aba_atual = chave

        for c, btn in self.botoes_sidebar.items():
            btn.configure(
                fg_color=self.cores["bg_hover"] if c == chave else "transparent",
                text_color="#ffffff" if c == chave else self.cores["texto_secundario"]
            )

        for pagina in self.paginas.values():
            pagina.pack_forget()

        self.paginas[chave].pack(fill="both", expand=True)

        if chave == "perfil":
            self.paginas["perfil"].carregar_perfil_salvo()

        if chave == "missoes":
            self.paginas["missoes"]._montar_tela()

    def atualizar_moedas(self):
        """Atualiza o saldo de moedas mostrado na barra lateral."""
        if hasattr(self, "badge_moedas") and self.badge_moedas.winfo_exists():
            self.badge_moedas.configure(text=f"🪙  {obter_moedas(self.controller.usuario_id)}")


# =====================================================
# 🔥 PÁGINA — ESTUDAR
# =====================================================

class PaginaComecar(ctk.CTkFrame):
    def __init__(self, parent, nivel, controller):
        super().__init__(parent, fg_color="transparent")
        self.nivel                 = nivel
        self.controller            = controller
        self.cores                 = obter_cores(controller.tema_atual)
        self.quiz_ativo            = False
        self.acertos_totais        = 0
        self.erros_totais          = 0
        self.questao_atual         = 0
        self.total_questoes        = 30
        
        self.ordem_niveis = [
            "Iniciante",
            "Intermediário",
            "Avançado"
        ]
        
        self.nivel_interno, self.acertos_para_nivel = carregar_level(self.controller.usuario_id)
        
        self.pack(fill="both", expand=True)
        self._mostrar_tela_inicial()

    # -----------------------------------------------
    # TELA INICIAL
    # -----------------------------------------------
    def _mostrar_tela_inicial(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.quiz_ativo            = False
        self.materias_selecionadas = set()

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        centro = ctk.CTkFrame(scroll, fg_color="transparent")
        centro.pack(pady=(10, 20))

        ctk.CTkLabel(centro, text="🚀", font=("Segoe UI Emoji", 40)).pack(pady=(0, 4))

        ctk.CTkLabel(
            centro, text=t(self.controller, "jornada_titulo"),
            font=("Poppins", 28, "bold"), text_color=self.cores["texto"]
        ).pack(pady=(0, 2))

        ctk.CTkLabel(
            centro, text=t(self.controller, "jornada_nivel_atual", nivel=traduzir_nivel(self.controller, self.nivel) or "N/A"),
            font=("Poppins", 13), text_color="#2563eb"
        ).pack(pady=(0, 10))

        # ── trilha de progresso estilo Duolingo ──
        self._desenhar_trilha_niveis(centro)

        ctk.CTkLabel(
            centro, text=t(self.controller, "jornada_escolher"),
            font=("Poppins", 14), text_color=self.cores["texto_secundario"]
        ).pack(pady=(30, 16))

        materias_info = [
            ("💻", "Hardware",    t(self.controller, "materia_desc_Hardware")),
            ("🌐", "Redes",       t(self.controller, "materia_desc_Redes")),
            ("⌨️", "Programação", t(self.controller, "materia_desc_Programação")),
        ]

        self.cards_materias = {}
        linha_cards = ctk.CTkFrame(centro, fg_color="transparent")
        linha_cards.pack(pady=(0, 25))
        self.linha_cards_ref = linha_cards

        for icone, nome, descricao in materias_info:
            card = ctk.CTkFrame(
                linha_cards, fg_color=self.cores["bg_card"],
                corner_radius=18, border_width=2, border_color=self.cores["bg_input"],
                width=175, height=130, cursor="hand2"
            )
            card.pack(side="left", padx=10)
            card.pack_propagate(False)

            ctk.CTkLabel(card, text=icone, font=("Segoe UI Emoji", 28)).pack(pady=(18, 4))
            ctk.CTkLabel(card, text=traduzir_materia(self.controller, nome), font=("Poppins", 14, "bold"), text_color=self.cores["texto"]).pack()
            ctk.CTkLabel(card, text=descricao, font=("Poppins", 10), text_color=self.cores["texto_apagado"], wraplength=150, justify="center").pack(pady=(2, 0))

            self.cards_materias[nome] = card

            card.bind("<Button-1>", lambda e, n=nome: self._toggle_materia(n))
            for filho in card.winfo_children():
                filho.bind("<Button-1>", lambda e, n=nome: self._toggle_materia(n))

        self.botao_comecar = ctk.CTkButton(
            centro, text=t(self.controller, "jornada_botao_comecar"),
            width=260, height=55, corner_radius=16,
            fg_color="#2563eb", hover_color="#1d4ed8",
            font=("Poppins", 18, "bold"),
            command=self._iniciar_quiz
        )

    # -----------------------------------------------
    # TRILHA DE NÍVEIS (estilo Duolingo)
    # -----------------------------------------------
    def _desenhar_trilha_niveis(self, parent):
        """
        Desenha a trilha de progresso: cada nó representa 1 acerto
        (são necessários 5 acertos para subir de nível interno).
        Nós verdes = já conquistados | nó azul = atual | cinza = bloqueado.
        """
        LARGURA, ALTURA = 300, 380
        RAIO = 26

        wrapper = tk.Frame(parent, bg=self.cores["bg"], width=LARGURA, height=ALTURA, highlightthickness=0)
        wrapper.pack()
        wrapper.pack_propagate(False)

        canvas = tk.Canvas(wrapper, width=LARGURA, height=ALTURA, bg=self.cores["bg"], highlightthickness=0, bd=0)
        canvas.pack()
        self._trilha_canvas = canvas

        # posições em zigue-zague, de baixo (nó 1) para cima (nó 5) + troféu no topo
        posicoes = [
            (150, 320),
            (215, 270),
            (150, 220),
            (85,  170),
            (150, 120),
            (150, 55),   # troféu = próximo nível
        ]

        # linha tracejada conectando os nós
        for i in range(len(posicoes) - 1):
            x1, y1 = posicoes[i]
            x2, y2 = posicoes[i + 1]
            canvas.create_line(x1, y1, x2, y2, fill=self.cores["bg_input"], width=4, dash=(6, 5))

        self._trilha_no_atual_pos = None
        self._trilha_robo_id      = None
        self._trilha_robo_img     = None
        self._trilha_tick         = 0.0

        for i in range(5):
            x, y = posicoes[i]

            if i < self.acertos_para_nivel:
                estado = "feito"
            elif i == self.acertos_para_nivel:
                estado = "atual"
            else:
                estado = "bloqueado"

            self._desenhar_no_trilha(canvas, x, y, RAIO, estado, i + 1)

            if estado == "atual":
                self._trilha_no_atual_pos = (x, y)

        # troféu — representa a conquista do próximo nível interno
        xt, yt = posicoes[5]
        quase_la = self.acertos_para_nivel >= 4
        cor_trofeu = "#f59e0b" if quase_la else self.cores["bg_input"]
        borda_trofeu = "#f59e0b" if quase_la else self.cores["borda"]

        canvas.create_oval(xt - 24, yt - 24, xt + 24, yt + 24, fill=cor_trofeu, outline=borda_trofeu, width=2)
        canvas.create_text(xt, yt, text="🏆", font=("Segoe UI Emoji", 18))
        canvas.create_text(xt, 18, text=t(self.controller, "trilha_proximo_nivel", n=self.nivel_interno + 1), font=("Poppins", 10, "bold"), fill=self.cores["texto_apagado"])

        # robô flutuando/pulando perto do nó atual
        if self._trilha_no_atual_pos:
            xr, yr = self._trilha_no_atual_pos
            self._trilha_robo_img = _carregar_robo_reacao("HappyF.png", 54)
            if self._trilha_robo_img:
                self._trilha_robo_id = canvas.create_image(xr, yr - 52, image=self._trilha_robo_img, anchor="center")
                self._animar_robo_trilha(canvas)

        canvas.create_text(
            150, 358,
            text=t(self.controller, "trilha_progresso", atual=self.acertos_para_nivel),
            font=("Poppins", 11), fill=self.cores["texto_apagado"]
        )

        # clicar no nó atual leva até a escolha de matéria (guia o olhar do usuário)
        def _clicar_trilha(event, raio=RAIO):
            if not self._trilha_no_atual_pos:
                return
            x, y = self._trilha_no_atual_pos
            if (event.x - x) ** 2 + (event.y - y) ** 2 <= (raio + 10) ** 2:
                self._focar_selecao_materia()

        canvas.bind("<Button-1>", _clicar_trilha)

    def _desenhar_no_trilha(self, canvas, x, y, raio, estado, numero):
        if estado == "feito":
            canvas.create_oval(x - raio, y - raio, x + raio, y + raio, fill="#22c55e", outline="#16a34a", width=2)
            canvas.create_text(x, y, text="✓", font=("Poppins", 18, "bold"), fill="#ffffff")
        elif estado == "atual":
            canvas.create_oval(x - raio - 6, y - raio - 6, x + raio + 6, y + raio + 6, outline="#2563eb", width=2)
            canvas.create_oval(x - raio, y - raio, x + raio, y + raio, fill="#2563eb", outline="#60a5fa", width=2)
            canvas.create_text(x, y, text=str(numero), font=("Poppins", 16, "bold"), fill="#ffffff")
        else:
            canvas.create_oval(x - raio, y - raio, x + raio, y + raio, fill=self.cores["bg_input"], outline=self.cores["borda"], width=2)
            canvas.create_text(x, y, text="🔒", font=("Segoe UI Emoji", 14))

    def _animar_robo_trilha(self, canvas):
        if not hasattr(self, "_trilha_canvas") or not canvas.winfo_exists() or self._trilha_robo_id is None:
            return
        try:
            self._trilha_tick += 0.1
            offset = math.sin(self._trilha_tick) * 5
            x, y = self._trilha_no_atual_pos
            canvas.coords(self._trilha_robo_id, x, (y - 52) + offset)
            self.after(35, lambda: self._animar_robo_trilha(canvas))
        except Exception:
            pass

    def _focar_selecao_materia(self):
        """Pisca a área de escolha de matéria, guiando o usuário após clicar no nó atual."""
        if not hasattr(self, "linha_cards_ref") or not self.linha_cards_ref.winfo_exists():
            return

        def piscar(vezes=4):
            if vezes <= 0 or not self.linha_cards_ref.winfo_exists():
                return
            for card in self.cards_materias.values():
                if card.cget("border_color") != "#2563eb":  # não mexe nas já selecionadas
                    cor = "#2563eb" if vezes % 2 == 0 else self.cores["bg_input"]
                    card.configure(border_color=cor)
            self.after(180, lambda: piscar(vezes - 1))

        piscar()


    #------------------------------------------------
    # TELA DE RESULTADO FINAL TROCAR NIVEL
    #------------------------------------------------
    
    def _mostrar_tela_trocar_nivel(self):

        # limpa tela atual
        for widget in self.winfo_children():
            widget.destroy()

        container = ctk.CTkFrame(
            self,
            fg_color=self.cores["bg"],
            corner_radius=25,
            border_width=2,
            border_color="#2563eb",
            width=500,
            height=450
        )
        container.place(relx=0.5, rely=0.5, anchor="center")
        container.pack_propagate(False)

        ctk.CTkLabel(
            container,
            text=t(self.controller, "trocar_nivel_titulo"),
            font=("Poppins", 22, "bold"),
            text_color=self.cores["texto"]
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            container,
            text=t(self.controller, "trocar_nivel_subtitulo"),
            font=("Poppins", 13),
            text_color=self.cores["texto_secundario"]
        ).pack(pady=(0, 15))

        # lista de níveis (usa sua ordem já definida)
        for nivel in self.ordem_niveis:
            
            cor_borda = "#22c55e" if nivel == self.nivel else self.cores["borda"]

            frame = ctk.CTkFrame(
                container,
                fg_color=self.cores["bg_input"],
                corner_radius=15,
                border_width=1,
                border_color=cor_borda,
                cursor="hand2",
                width=350,
                height=70
            )
            frame.pack(pady=8)
            frame.pack_propagate(False)

            label = ctk.CTkLabel(
                frame,
                text=traduzir_nivel(self.controller, nivel),
                font=("Poppins", 18, "bold"),
                text_color="#ffffff"
            )
            label.pack(expand=True)

            # clique no frame
            frame.bind(
                "<Button-1>",
                lambda e, n=nivel: self._selecionar_novo_nivel(n)
            )

            # clique no label também
            label.bind(
                "<Button-1>",
                lambda e, n=nivel: self._selecionar_novo_nivel(n)
            )

        # botão voltar
        ctk.CTkButton(
            container,
            text=t(self.controller, "trocar_nivel_voltar"),
            width=180,
            height=40,
            fg_color=self.cores["borda"],
            hover_color="#475569",
            command=self._mostrar_resultado_final  # ou tela anterior do quiz
        ).pack(pady=20)
    
    def _selecionar_novo_nivel(self, novo_nivel):

        self.nivel = novo_nivel

        salvar_nivel(
            self.controller.usuario_id,
            novo_nivel
        )

        self._mostrar_tela_inicial()

    # -----------------------------------------------
    # TOGGLE MATÉRIA
    # -----------------------------------------------
    def _toggle_materia(self, nome):
        card = self.cards_materias[nome]

        if nome in self.materias_selecionadas:
            self.materias_selecionadas.discard(nome)
            card.configure(border_color=self.cores["bg_input"], fg_color=self.cores["bg_card"])
        else:
            self.materias_selecionadas.add(nome)
            card.configure(border_color="#2563eb", fg_color=self.cores["bg_hover"])

        for filho in card.winfo_children():
            filho.bind("<Button-1>", lambda e, n=nome: self._toggle_materia(n))

        if self.materias_selecionadas:
            if not self.botao_comecar.winfo_ismapped():
                self.botao_comecar.pack(pady=(0, 0))
        else:
            self.botao_comecar.pack_forget()

    # -----------------------------------------------
    # INICIAR QUIZ
    # -----------------------------------------------
    def _iniciar_quiz(self):
        
        (
            self.questao_atual,
            self.acertos_totais,
            self.erros_totais
        ) = carregar_progresso_quiz(self.controller.usuario_id)

        
        self.nivel_interno, self.acertos_para_nivel = carregar_level(self.controller.usuario_id)
        
        # Parte removida devido ao carregamento do nível interno e progresso do usuário no banco de dados
        #self.acertos_para_nivel = 0
        #self.nivel_interno      = 1
        
        self.quiz_ativo         = True
        self.materia_atual      = random.choice(list(self.materias_selecionadas))

        self._mostrar_carregando()

    # -----------------------------------------------
    # TELA DE CARREGANDO
    # -----------------------------------------------
    def _mostrar_carregando(self):
        for widget in self.winfo_children():
            widget.destroy()

        centro = ctk.CTkFrame(self, fg_color="transparent")
        centro.place(relx=0.5, rely=0.5, anchor="center")

        spinner, iniciar_spinner, parar_spinner = criar_spinner(centro, self.cores, tamanho=56)
        spinner.pack(pady=(0, 15))
        self._spinner_parar = parar_spinner
        iniciar_spinner()

        ctk.CTkLabel(
            centro, text=t(self.controller, "quiz_gerando"),
            font=("Poppins", 18, "bold"), text_color=self.cores["texto"]
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            centro,
            text=t(self.controller, "quiz_materia_nivel", materia=traduzir_materia(self.controller, self.materia_atual), nivel=traduzir_nivel(self.controller, self.nivel)),
            font=("Poppins", 13), text_color=self.cores["texto_apagado"]
        ).pack()

        self.update()
        threading.Thread(target=self._buscar_pergunta, daemon=True).start()

    # -----------------------------------------------
    # BUSCAR PERGUNTA NA API
    # -----------------------------------------------
    def _buscar_pergunta(self):
        self.materia_atual = random.choice(list(self.materias_selecionadas))
        contexto = f"{self.materia_atual} - nível {self.nivel}"
        dados = gerar_pergunta(contexto, idioma=getattr(self.controller, "idioma", "pt"))

        if not dados:
            self.after(0, self._mostrar_erro_api)
            return

        self.dados_pergunta_atual = dados
        self.after(0, self._mostrar_questao)

    # -----------------------------------------------
    # ERRO DE API
    # -----------------------------------------------
    def _mostrar_erro_api(self):
        for widget in self.winfo_children():
            widget.destroy()

        centro = ctk.CTkFrame(self, fg_color="transparent")
        centro.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(centro, text="⚠️", font=("Segoe UI Emoji", 48)).pack(pady=(0, 15))

        ctk.CTkLabel(
            centro, text=t(self.controller, "quiz_erro_titulo"),
            font=("Poppins", 20, "bold"), text_color="#ef4444"
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            centro,
            text=t(self.controller, "quiz_erro_subtitulo"),
            font=("Poppins", 13), text_color=self.cores["texto_apagado"]
        ).pack(pady=(0, 25))

        ctk.CTkButton(
            centro, text=t(self.controller, "quiz_tentar_novamente"),
            width=220, height=48, corner_radius=12,
            fg_color="#2563eb", hover_color="#1d4ed8",
            font=("Poppins", 14, "bold"),
            command=self._mostrar_carregando
        ).pack(pady=(0, 12))

        ctk.CTkButton(
            centro, text=t(self.controller, "quiz_voltar"),
            width=220, height=40, corner_radius=12,
            fg_color="transparent", hover_color=self.cores["bg_input"],
            text_color=self.cores["texto_apagado"], font=("Poppins", 13),
            command=self._mostrar_tela_inicial
        ).pack()

    # -----------------------------------------------
    # MOSTRAR QUESTÃO
    # -----------------------------------------------
    def _mostrar_questao(self):
        for widget in self.winfo_children():
            widget.destroy()

        dados = self.dados_pergunta_atual

        # =================================================
        # BARRA FIXA DO TOPO — não rola, sempre visível
        # (aqui fica o botão "Continuar", pra nunca ficar
        # escondido/fora da tela em notebooks menores)
        # =================================================
        topo_fixo = ctk.CTkFrame(self, fg_color="transparent")
        topo_fixo.pack(fill="x", side="top")

        header = ctk.CTkFrame(topo_fixo, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(15, 5))

        ctk.CTkButton(
            header, text=t(self.controller, "quiz_header_voltar"),
            width=100, height=34, corner_radius=10,
            fg_color="transparent", hover_color=self.cores["bg_input"],
            text_color=self.cores["texto_apagado"], font=("Poppins", 13), anchor="w",
            command=self._mostrar_tela_inicial
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text=t(self.controller, "quiz_questao_de", atual=self.questao_atual + 1, total=self.total_questoes),
            font=("Poppins", 13, "bold"), text_color=self.cores["texto_secundario"]
        ).pack(side="left", padx=20)

        ctk.CTkLabel(
            header,
            text=f"✅ {self.acertos_totais}    ❌ {self.erros_totais}",
            font=("Poppins", 13), text_color=self.cores["texto_apagado"]
        ).pack(side="right")

        # botão "Continuar" — já existe aqui em cima, mas só aparece
        # (via .pack) depois que o usuário responder a pergunta
        self.botao_continuar = ctk.CTkButton(
            topo_fixo, text=t(self.controller, "quiz_continuar"),
            width=200, height=40, corner_radius=12,
            fg_color="#2563eb", hover_color="#1d4ed8",
            font=("Poppins", 13, "bold"),
            command=self._ao_clicar_continuar
        )

        # =================================================
        # CONTEÚDO ROLÁVEL — sempre acessível, não importa
        # o tamanho da tela/notebook do usuário
        # =================================================
        self.scroll_quiz = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_quiz.pack(fill="both", expand=True, padx=0, pady=(0, 10))
        conteudo = self.scroll_quiz

        # badge nível interno
        badge_quiz = ctk.CTkFrame(
            conteudo,
            fg_color=self.cores["bg_input"],
            corner_radius=30,
            border_width=2,
            border_color="#2563eb",
            width=56,
            height=56
        )
        badge_quiz.pack(pady=(5, 0))
        badge_quiz.pack_propagate(False)

        ctk.CTkLabel(
            badge_quiz, text="lvl",
            font=("Poppins", 11), text_color=self.cores["texto_apagado"]
        ).place(relx=0.5, rely=0.3, anchor="center")

        ctk.CTkLabel(
            badge_quiz, text=str(self.nivel_interno),
            font=("Poppins", 18, "bold"), text_color="#2563eb"
        ).place(relx=0.5, rely=0.65, anchor="center")

        # -----------------------------------------------
        # ROBÔ ANIMADO FAZENDO A PERGUNTA
        # -----------------------------------------------
        robo_wrapper = tk.Frame(conteudo, bg=self.cores["bg"], width=100, height=100, highlightthickness=0)
        robo_wrapper.pack(pady=(4, 0))
        robo_wrapper.pack_propagate(False)

        self._robo_canvas_quiz = tk.Canvas(
            robo_wrapper, width=100, height=100,
            bg=self.cores["bg"], highlightthickness=0, bd=0
        )
        self._robo_canvas_quiz.pack()

        self._robo_img_quiz = _carregar_robo_reacao("NeutralF.png", 92)
        self._robo_id_quiz  = None

        if self._robo_img_quiz:
            self._robo_id_quiz = self._robo_canvas_quiz.create_image(
                50, 50, image=self._robo_img_quiz, anchor="center"
            )
            self._robo_tick_quiz = 0.0
            self._animar_robo_quiz()

        # nível + matéria
        info = ctk.CTkFrame(conteudo, fg_color="transparent")
        info.pack(fill="x", padx=30, pady=(0, 5))

        ctk.CTkLabel(
            info,
            text=t(self.controller, "quiz_materia_label", materia=traduzir_materia(self.controller, self.materia_atual), nivel=traduzir_nivel(self.controller, self.nivel)),
            font=("Poppins", 13, "bold"), text_color="#2563eb"
        ).pack(side="left")

        # barra dupla: questões + progresso para próximo nível
        prog_frame = ctk.CTkFrame(conteudo, fg_color="transparent")
        prog_frame.pack(fill="x", padx=30, pady=(0, 4))

        # barra de questões
        barra_q = ctk.CTkProgressBar(
            prog_frame, height=6,
            progress_color="#2563eb", fg_color=self.cores["bg_input"]
        )
        barra_q.pack(fill="x", side="left", expand=True, padx=(0, 10))
        barra_q.set(self.questao_atual / self.total_questoes)

        ctk.CTkLabel(
            prog_frame,
            text=f"{self.questao_atual}/{self.total_questoes}",
            font=("Poppins", 11), text_color=self.cores["borda"]
        ).pack(side="left")

        # barra de acertos para nível (verde)
        nivel_frame = ctk.CTkFrame(conteudo, fg_color="transparent")
        nivel_frame.pack(fill="x", padx=30, pady=(0, 12))

        barra_n = ctk.CTkProgressBar(
            nivel_frame, height=5,
            progress_color="#22c55e", fg_color=self.cores["bg_input"]
        )
        barra_n.pack(fill="x", side="left", expand=True, padx=(0, 10))
        barra_n.set(self.acertos_para_nivel / 5)

        ctk.CTkLabel(
            nivel_frame,
            text=f"⬆️ {self.acertos_para_nivel}/5",
            font=("Poppins", 11), text_color="#22c55e"
        ).pack(side="left")

        # CARD DA PERGUNTA
        card = ctk.CTkFrame(
            conteudo, fg_color=self.cores["bg_card"],
            corner_radius=20, border_width=1, border_color=self.cores["bg_input"]
        )
        card.pack(fill="x", padx=30, pady=(0, 15))

        ctk.CTkLabel(
            card,
            text=dados["pergunta"],
            font=("Poppins", 16, "bold"),
            text_color=self.cores["texto"],
            wraplength=680, justify="left"
        ).pack(anchor="w", padx=25, pady=25)

        # OPÇÕES
        self.botoes_opcoes = {}

        for letra in ["A", "B", "C", "D"]:
            opcao = dados["opcoes"][letra]

            btn = ctk.CTkButton(
                card,
                text=f"  {letra}.  {opcao['texto']}",
                height=50, corner_radius=12,
                fg_color=self.cores["bg_input"], hover_color=self.cores["bg_hover"],
                text_color="#e2e8f0", font=("Poppins", 14),
                anchor="w",
                command=lambda l=letra: self._responder(l)
            )
            btn.pack(fill="x", padx=25, pady=5)
            self.botoes_opcoes[letra] = btn

        ctk.CTkFrame(card, fg_color="transparent", height=10).pack()

    # -----------------------------------------------
    # ANIMAÇÃO DO ROBÔ NO QUIZ (sobe e desce, tipo "pulando")
    # -----------------------------------------------
    def _animar_robo_quiz(self):
        if not hasattr(self, "_robo_canvas_quiz"):
            return
        if not self._robo_canvas_quiz.winfo_exists() or self._robo_id_quiz is None:
            return
        try:
            self._robo_tick_quiz += 0.12
            offset_y = math.sin(self._robo_tick_quiz) * 6
            self._robo_canvas_quiz.coords(self._robo_id_quiz, 50, 50 + offset_y)
            self.after(30, self._animar_robo_quiz)
        except Exception:
            pass

    def _trocar_robo_quiz(self, nome_arquivo):
        """Troca a expressão do robô (feliz ao acertar, triste ao errar)."""
        if not hasattr(self, "_robo_canvas_quiz") or not self._robo_canvas_quiz.winfo_exists():
            return
        nova_img = _carregar_robo_reacao(nome_arquivo, 92)
        if nova_img and self._robo_id_quiz is not None:
            self._robo_img_quiz = nova_img  # mantém referência viva (senão o GC apaga a imagem)
            self._robo_canvas_quiz.itemconfig(self._robo_id_quiz, image=nova_img)

    # -----------------------------------------------
    # PAINEL DE EXPLICAÇÃO (acerto/erro)
    # -----------------------------------------------
    def _mostrar_explicacao(self, acertou, correta, explicacao):
        cor_fundo = "#052e1a" if acertou else "#3f0d0d"
        cor_borda = "#22c55e" if acertou else "#ef4444"
        titulo    = t(self.controller, "quiz_acertou") if acertou else t(self.controller, "quiz_errou", letra=correta)

        painel = ctk.CTkFrame(
            self.scroll_quiz, fg_color=cor_fundo, corner_radius=16,
            border_width=1, border_color=cor_borda
        )
        painel.pack(fill="x", padx=30, pady=(0, 15))

        ctk.CTkLabel(
            painel, text=titulo,
            font=("Poppins", 14, "bold"), text_color=cor_borda,
            anchor="w"
        ).pack(anchor="w", padx=20, pady=(14, 2))

        if explicacao:
            ctk.CTkLabel(
                painel, text=explicacao,
                font=("Poppins", 13), text_color="#e2e8f0",
                wraplength=640, justify="left", anchor="w"
            ).pack(anchor="w", padx=20, pady=(0, 14))
        else:
            ctk.CTkFrame(painel, fg_color="transparent", height=6).pack()

        # rola automaticamente até o final, garantindo que a explicação
        # apareça na tela mesmo em notebooks com resolução menor
        try:
            self.scroll_quiz.update_idletasks()
            self.scroll_quiz._parent_canvas.yview_moveto(1.0)
        except Exception:
            pass


    def _responder(self, letra_escolhida):
        dados       = self.dados_pergunta_atual
        correta     = obter_resposta_correta(dados)
        acertou     = verificar_resposta(dados, letra_escolhida)
        explicacao  = dados.get("explicacao", "").strip()

        for btn in self.botoes_opcoes.values():
            btn.configure(state="disabled")

        if acertou:
            sons.tocar_acerto()

            self.botoes_opcoes[letra_escolhida].configure(
                fg_color="#166534", text_color="#ffffff"
            )
            self.acertos_totais     += 1

            nivel_interno_antes = self.nivel_interno
            self.nivel_interno, self.acertos_para_nivel = adicionar_progresso(self.controller.usuario_id)
            registrar_acerto_global(self.controller.usuario_id)
            self._trocar_robo_quiz("Happy2F.png")

            if self.nivel_interno > nivel_interno_antes:
                self._animar_subida_nivel()
                # espera a animação de "subiu de nível" terminar antes de perguntar
                self.after(1800, self._verificar_sugestao_dificuldade)

        else:
            sons.tocar_erro()

            self.botoes_opcoes[letra_escolhida].configure(
                fg_color="#7f1d1d", text_color="#ffffff"
            )
            self.botoes_opcoes[correta].configure(
                fg_color="#166534", text_color="#ffffff"
            )
            self.erros_totais += 1
            self._trocar_robo_quiz("DecepcaoF.png")

        # explica por que acertou/errou, com a ajuda do robô
        self._mostrar_explicacao(acertou, correta, explicacao)

        self.questao_atual += 1
        
        salvar_progresso_quiz(
            self.controller.usuario_id,
            self.questao_atual,
            self.acertos_totais,
            self.erros_totais
            )

        # mostra o botão "Continuar" já fixo no topo — sempre visível,
        # não importa o tamanho da tela do notebook do usuário
        e_ultima = self.questao_atual >= self.total_questoes
        self.botao_continuar.configure(
            text=t(self.controller, "quiz_ver_resultado") if e_ultima else t(self.controller, "quiz_continuar")
        )
        self.botao_continuar.pack(pady=(0, 8))

    def _ao_clicar_continuar(self):
        if self.questao_atual >= self.total_questoes:
            self._mostrar_resultado_final()
        else:
            self._mostrar_carregando()

    # -----------------------------------------------
    # ANIMAÇÃO DE SUBIDA DE NÍVEL
    # -----------------------------------------------
    def _animar_subida_nivel(self):
        # pega a janela raiz para passar como parent
        janela_raiz = self.winfo_toplevel()
        AnimacaoNivel(janela_raiz, self.controller, traduzir_nivel(self.controller, self.nivel) or f"Nível {self.nivel_interno}")

    # -----------------------------------------------
    # SUGESTÃO AUTOMÁTICA DE DIFICULDADE
    # -----------------------------------------------
    # Quando o jogo percebe que o usuário está indo muito bem no
    # nível atual (nível interno alto), ele PERGUNTA se o usuário
    # quer subir de dificuldade — nunca muda sozinho.
    SUGESTAO_DIFICULDADE = {
        "Iniciante":     (5,  "Intermediário"),
        "Intermediário": (10, "Avançado"),
    }

    def _verificar_sugestao_dificuldade(self):
        if not self.winfo_exists():
            return

        regra = self.SUGESTAO_DIFICULDADE.get(self.nivel)
        if not regra:
            return  # já está no nível mais avançado

        limite, proximo_nivel = regra
        if self.nivel_interno < limite:
            return  # ainda não rendeu o suficiente pra sugerir

        recusados = getattr(self.controller, "dificuldades_recusadas", set())
        if proximo_nivel in recusados:
            return  # o usuário já disse "não" pra essa sugestão nesta sessão

        self._mostrar_popup_sugestao_dificuldade(proximo_nivel)

    def _mostrar_popup_sugestao_dificuldade(self, proximo_nivel):
        janela = ctk.CTkToplevel(self.winfo_toplevel())
        janela.title(t(self.controller, "sugestao_titulo_janela"))
        janela.geometry("380x260")
        janela.configure(fg_color=self.cores["bg"])
        janela.resizable(False, False)
        janela.grab_set()

        ctk.CTkLabel(janela, text="🚀", font=("Segoe UI Emoji", 40)).pack(pady=(25, 5))

        ctk.CTkLabel(
            janela, text=t(self.controller, "sugestao_titulo"),
            font=("Poppins", 18, "bold"), text_color=self.cores["texto"]
        ).pack()

        ctk.CTkLabel(
            janela,
            text=t(self.controller, "sugestao_texto", nivel=traduzir_nivel(self.controller, self.nivel), proximo=traduzir_nivel(self.controller, proximo_nivel)),
            font=("Poppins", 13), text_color=self.cores["texto_secundario"],
            justify="center", wraplength=320
        ).pack(pady=(8, 20))

        linha = ctk.CTkFrame(janela, fg_color="transparent")
        linha.pack()

        ctk.CTkButton(
            linha, text=t(self.controller, "sugestao_sim", proximo=traduzir_nivel(self.controller, proximo_nivel)),
            width=185, height=42, corner_radius=10,
            fg_color="#2563eb", hover_color="#1d4ed8", font=("Poppins", 13, "bold"),
            command=lambda: self._confirmar_sugestao_dificuldade(proximo_nivel, janela)
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            linha, text=t(self.controller, "sugestao_nao"),
            width=140, height=42, corner_radius=10,
            fg_color=self.cores["bg_input"], hover_color=self.cores["bg_hover"],
            text_color=self.cores["texto_secundario"], font=("Poppins", 13, "bold"),
            command=lambda: self._recusar_sugestao_dificuldade(proximo_nivel, janela)
        ).pack(side="left")

    def _confirmar_sugestao_dificuldade(self, novo_nivel, janela):
        janela.destroy()
        salvar_nivel(self.controller.usuario_id, novo_nivel)
        self.controller.nivel_usuario = novo_nivel
        self.controller.ir_para_main(novo_nivel)

    def _recusar_sugestao_dificuldade(self, nivel_recusado, janela):
        if not hasattr(self.controller, "dificuldades_recusadas"):
            self.controller.dificuldades_recusadas = set()
        self.controller.dificuldades_recusadas.add(nivel_recusado)
        janela.destroy()

    # -----------------------------------------------
    # RESULTADO FINAL
    # -----------------------------------------------
    def _mostrar_resultado_final(self):
        
        for widget in self.winfo_children():
            widget.destroy()

        registrar_atividade_concluida(self.controller.usuario_id)
        missoes_prontas = [m for m in obter_missoes(self.controller.usuario_id) if m["pode_resgatar"]]

        centro = ctk.CTkFrame(self, fg_color="transparent")
        centro.place(relx=0.5, rely=0.5, anchor="center")

        pct = self.acertos_totais / self.total_questoes
        emoji = "🏆" if pct >= 0.8 else "👍" if pct >= 0.5 else "📚"

        ctk.CTkLabel(
            centro,
            text=emoji,
            font=("Segoe UI Emoji", 52)
        ).pack(pady=(0, 10))

        ctk.CTkLabel(
            centro,
            text=t(self.controller, "resultado_titulo"),
            font=("Poppins", 28, "bold"),
            text_color=self.cores["texto"]
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            centro,
            text=t(self.controller, "resultado_acertos", acertos=self.acertos_totais, total=self.total_questoes),
            font=("Poppins", 16),
            text_color=self.cores["texto_secundario"]
        ).pack(pady=(0, 5))

        ctk.CTkLabel(
            centro,
            text=t(self.controller, "resultado_nivel_interno", nivel=self.nivel_interno),
            font=("Poppins", 13),
            text_color="#22c55e"
        ).pack(pady=(0, 5))

        ctk.CTkLabel(
            centro,
            text=t(self.controller, "resultado_nivel_atual", nivel=traduzir_nivel(self.controller, self.nivel)),
            font=("Poppins", 14, "bold"),
            text_color="#2563eb"
        ).pack(pady=(0, 20))

        if missoes_prontas:
            aviso = ctk.CTkFrame(
                centro, fg_color="#052e1a", corner_radius=14,
                border_width=1, border_color="#22c55e"
            )
            aviso.pack(pady=(0, 15))

            nomes = ", ".join(traduzir_missao_titulo(self.controller, m) for m in missoes_prontas)
            ctk.CTkLabel(
                aviso,
                text=t(self.controller, "resultado_missao_pronta", nomes=nomes),
                font=("Poppins", 12, "bold"), text_color="#22c55e",
                wraplength=380, justify="center"
            ).pack(padx=18, pady=12)

        # ==========================
        # BOTÕES PRINCIPAIS
        # ==========================
        linha = ctk.CTkFrame(centro, fg_color="transparent")
        linha.pack(pady=10)

        # 🔁 REINICIAR
        ctk.CTkButton(
            linha,
            text=t(self.controller, "resultado_reiniciar"),
            width=180,
            height=48,
            corner_radius=12,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            font=("Poppins", 14, "bold"),
            command=self.reiniciar_nivel
        ).pack(side="left", padx=(0, 12))

        # 🔄 TROCAR NÍVEL
        ctk.CTkButton(
            linha,
            text=t(self.controller, "resultado_trocar_nivel"),
            width=180,
            height=48,
            corner_radius=12,
            fg_color=self.cores["bg_input"],
            hover_color=self.cores["borda"],
            text_color=self.cores["texto_secundario"],
            font=("Poppins", 14, "bold"),
            command=self._mostrar_tela_trocar_nivel
        ).pack(side="left")

        # ==========================
        # BOTÃO VOLTAR INÍCIO
        # ==========================
        ctk.CTkButton(
            centro,
            text=t(self.controller, "resultado_voltar_inicio"),
            width=200,
            height=40,
            corner_radius=10,
            fg_color="transparent",
            hover_color=self.cores["bg_input"],
            text_color=self.cores["texto_apagado"],
            font=("Poppins", 13),
            command=self._mostrar_tela_inicial
        ).pack(pady=(15, 0))
        
    def _selecionar_novo_nivel(self, novo_nivel):

        self.nivel = novo_nivel
        self.controller.nivel_usuario = novo_nivel

        salvar_nivel(
            self.controller.usuario_id,
            novo_nivel
        )

        # reset progresso ao trocar nível
        self.questao_atual = 0
        self.acertos_totais = 0
        self.erros_totais = 0

        self._mostrar_tela_inicial()
        
    def reiniciar_nivel(self):

        self.questao_atual = 0
        self.acertos_totais = 0
        self.erros_totais = 0

        salvar_progresso_quiz(
            self.controller.usuario_id,
            0,
            0,
            0
        )

        self._iniciar_quiz()

# =====================================================
# 🔥 PÁGINA — CURSOS
# =====================================================

class PaginaCursos(ctk.CTkFrame):
    """
    Aba de cursos: o usuário escolhe uma matéria (Hardware, Redes ou
    Programação) e um nível (Iniciante, Intermediário ou Avançado) e
    recebe uma aula gerada por IA, com conteúdo, exemplo prático e dica.
    """

    def _materias_info(self):
        return [
            ("💻", "Hardware",    t(self.controller, "materia_desc_Hardware")),
            ("🌐", "Redes",       t(self.controller, "materia_desc_Redes")),
            ("⌨️", "Programação", t(self.controller, "materia_desc_Programação")),
        ]

    def _niveis_info(self):
        return [
            (t(self.controller, "cursos_nivel_emoji_Iniciante"),     "Iniciante",     t(self.controller, "cursos_nivel_desc_Iniciante")),
            (t(self.controller, "cursos_nivel_emoji_Intermediário"), "Intermediário", t(self.controller, "cursos_nivel_desc_Intermediário")),
            (t(self.controller, "cursos_nivel_emoji_Avançado"),      "Avançado",      t(self.controller, "cursos_nivel_desc_Avançado")),
        ]

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.cores = obter_cores(controller.tema_atual)

        self.materia_escolhida = None
        self.nivel_escolhido   = None
        self.licao_atual       = None

        self.pack(fill="both", expand=True)
        self._mostrar_selecao_materia()

    # -----------------------------------------------
    # TELA 1 — ESCOLHER MATÉRIA
    # -----------------------------------------------
    def _mostrar_selecao_materia(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.materia_escolhida = None
        self.nivel_escolhido   = None

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=35, pady=35)

        ctk.CTkLabel(
            scroll, text=t(self.controller, "titulo_cursos"),
            font=("Poppins", 30, "bold"), text_color=self.cores["texto"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            scroll,
            text=t(self.controller, "cursos_subtitulo"),
            font=("Poppins", 13), text_color=self.cores["texto_secundario"],
            justify="left"
        ).pack(anchor="w", pady=(4, 25))

        grid = ctk.CTkFrame(scroll, fg_color="transparent")
        grid.pack(fill="x")
        for col in range(3):
            grid.grid_columnconfigure(col, weight=1, uniform="col")

        for i, (icone, nome, descricao) in enumerate(self._materias_info()):
            card = ctk.CTkFrame(
                grid, fg_color=self.cores["bg_card"], corner_radius=18,
                border_width=1, border_color=self.cores["borda"],
                width=220, height=170, cursor="hand2"
            )
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            card.grid_propagate(False)

            ctk.CTkLabel(card, text=icone, font=("Segoe UI Emoji", 36)).pack(pady=(24, 8))
            ctk.CTkLabel(
                card, text=traduzir_materia(self.controller, nome), font=("Poppins", 16, "bold"), text_color=self.cores["texto"]
            ).pack()
            ctk.CTkLabel(
                card, text=descricao, font=("Poppins", 11),
                text_color=self.cores["texto_secundario"], wraplength=180, justify="center"
            ).pack(pady=(4, 0))

            card.bind("<Button-1>", lambda e, n=nome: self._selecionar_materia(n))
            for filho in card.winfo_children():
                filho.bind("<Button-1>", lambda e, n=nome: self._selecionar_materia(n))

    def _selecionar_materia(self, nome):
        self.materia_escolhida = nome
        self._mostrar_selecao_nivel()

    # -----------------------------------------------
    # TELA 2 — ESCOLHER NÍVEL
    # -----------------------------------------------
    def _mostrar_selecao_nivel(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.nivel_escolhido = None

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=35, pady=35)

        topo = ctk.CTkFrame(scroll, fg_color="transparent")
        topo.pack(fill="x", pady=(0, 15))

        ctk.CTkButton(
            topo, text=t(self.controller, "quiz_header_voltar"), width=100, height=34, corner_radius=10,
            fg_color="transparent", hover_color=self.cores["bg_input"],
            text_color=self.cores["texto_secundario"], font=("Poppins", 13),
            command=self._mostrar_selecao_materia
        ).pack(side="left")

        ctk.CTkLabel(
            scroll, text=t(self.controller, "cursos_de", materia=traduzir_materia(self.controller, self.materia_escolhida)),
            font=("Poppins", 26, "bold"), text_color=self.cores["texto"]
        ).pack(anchor="w", pady=(10, 4))

        ctk.CTkLabel(
            scroll,
            text=t(self.controller, "cursos_escolha_nivel"),
            font=("Poppins", 13), text_color=self.cores["texto_secundario"]
        ).pack(anchor="w", pady=(0, 20))

        for icone, nome, descricao in self._niveis_info():
            card = ctk.CTkFrame(
                scroll, fg_color=self.cores["bg_card"], corner_radius=16,
                border_width=1, border_color=self.cores["borda"], cursor="hand2"
            )
            card.pack(fill="x", pady=8)

            linha = ctk.CTkFrame(card, fg_color="transparent")
            linha.pack(fill="x", padx=20, pady=16)

            ctk.CTkLabel(linha, text=icone, font=("Segoe UI Emoji", 26)).pack(side="left", padx=(0, 16))

            info = ctk.CTkFrame(linha, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True)

            ctk.CTkLabel(
                info, text=traduzir_nivel(self.controller, nome), font=("Poppins", 15, "bold"), text_color=self.cores["texto"]
            ).pack(anchor="w")
            ctk.CTkLabel(
                info, text=descricao, font=("Poppins", 12),
                text_color=self.cores["texto_secundario"], wraplength=420, justify="left"
            ).pack(anchor="w")

            ctk.CTkLabel(linha, text="→", font=("Poppins", 18, "bold"), text_color="#2563eb").pack(side="right")

            for alvo in (card, linha, info, *info.winfo_children(), *linha.winfo_children()):
                alvo.bind("<Button-1>", lambda e, n=nome: self._selecionar_nivel(n))

    def _selecionar_nivel(self, nome):
        self.nivel_escolhido = nome
        self._gerar_licao()

    # -----------------------------------------------
    # TELA DE CARREGANDO
    # -----------------------------------------------
    def _gerar_licao(self):
        for widget in self.winfo_children():
            widget.destroy()

        centro = ctk.CTkFrame(self, fg_color="transparent")
        centro.place(relx=0.5, rely=0.5, anchor="center")

        spinner, iniciar_spinner, parar_spinner = criar_spinner(centro, self.cores, tamanho=56)
        spinner.pack(pady=(0, 15))
        self._spinner_parar = parar_spinner
        iniciar_spinner()

        ctk.CTkLabel(
            centro, text=t(self.controller, "cursos_preparando"),
            font=("Poppins", 18, "bold"), text_color=self.cores["texto"]
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            centro,
            text=t(self.controller, "quiz_materia_nivel", materia=traduzir_materia(self.controller, self.materia_escolhida), nivel=traduzir_nivel(self.controller, self.nivel_escolhido)),
            font=("Poppins", 13), text_color=self.cores["texto_apagado"]
        ).pack()

        self.update()
        threading.Thread(target=self._buscar_licao, daemon=True).start()

    # -----------------------------------------------
    # BUSCAR AULA NA API
    # -----------------------------------------------
    def _buscar_licao(self):
        dados = gerar_licao(self.materia_escolhida, self.nivel_escolhido, idioma=getattr(self.controller, "idioma", "pt"))

        if not dados:
            self.after(0, self._mostrar_erro_licao)
            return

        self.licao_atual = dados
        self.after(0, self._mostrar_licao)

    # -----------------------------------------------
    # ERRO DE API
    # -----------------------------------------------
    def _mostrar_erro_licao(self):
        for widget in self.winfo_children():
            widget.destroy()

        centro = ctk.CTkFrame(self, fg_color="transparent")
        centro.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(centro, text="⚠️", font=("Segoe UI Emoji", 48)).pack(pady=(0, 15))

        ctk.CTkLabel(
            centro, text=t(self.controller, "cursos_erro_titulo"),
            font=("Poppins", 20, "bold"), text_color="#ef4444"
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            centro,
            text=t(self.controller, "cursos_erro_texto"),
            font=("Poppins", 13), text_color=self.cores["texto_apagado"]
        ).pack(pady=(0, 25))

        ctk.CTkButton(
            centro, text=t(self.controller, "quiz_tentar_novamente"),
            width=220, height=48, corner_radius=12,
            fg_color="#2563eb", hover_color="#1d4ed8",
            font=("Poppins", 14, "bold"),
            command=self._gerar_licao
        ).pack(pady=(0, 12))

        ctk.CTkButton(
            centro, text=t(self.controller, "quiz_voltar"),
            width=220, height=40, corner_radius=12,
            fg_color="transparent", hover_color=self.cores["bg_input"],
            text_color=self.cores["texto_apagado"], font=("Poppins", 13),
            command=self._mostrar_selecao_nivel
        ).pack()

    # -----------------------------------------------
    # TELA DA AULA
    # -----------------------------------------------
    def _mostrar_licao(self):
        for widget in self.winfo_children():
            widget.destroy()

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=35, pady=35)

        topo = ctk.CTkFrame(scroll, fg_color="transparent")
        topo.pack(fill="x", pady=(0, 15))

        ctk.CTkButton(
            topo, text=t(self.controller, "cursos_trocar_nivel"), width=140, height=34, corner_radius=10,
            fg_color="transparent", hover_color=self.cores["bg_input"],
            text_color=self.cores["texto_secundario"], font=("Poppins", 13),
            command=self._mostrar_selecao_nivel
        ).pack(side="left")

        ctk.CTkLabel(
            topo, text=f"{traduzir_materia(self.controller, self.materia_escolhida)}  •  {traduzir_nivel(self.controller, self.nivel_escolhido)}",
            font=("Poppins", 13, "bold"), text_color=self.cores["texto_apagado"],
            fg_color=self.cores["bg_input"], corner_radius=10
        ).pack(side="right", ipadx=14, ipady=6)

        dados = self.licao_atual or {}

        card = ctk.CTkFrame(
            scroll, fg_color=self.cores["bg_card"], corner_radius=20,
            border_width=1, border_color=self.cores["borda"]
        )
        card.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            card, text=dados.get("titulo") or t(self.controller, "cursos_aula_generica"),
            font=("Poppins", 22, "bold"), text_color=self.cores["texto"],
            wraplength=650, justify="left"
        ).pack(anchor="w", padx=28, pady=(24, 10))

        ctk.CTkLabel(
            card, text=dados.get("conteudo", ""),
            font=("Poppins", 14), text_color=self.cores["texto_secundario"],
            wraplength=650, justify="left"
        ).pack(anchor="w", padx=28, pady=(0, 16))

        if dados.get("exemplo"):
            exemplo_frame = ctk.CTkFrame(card, fg_color=self.cores["bg_input"], corner_radius=14)
            exemplo_frame.pack(fill="x", padx=28, pady=(0, 16))

            ctk.CTkLabel(
                exemplo_frame, text=t(self.controller, "cursos_exemplo"),
                font=("Poppins", 13, "bold"), text_color="#2563eb"
            ).pack(anchor="w", padx=16, pady=(12, 2))

            ctk.CTkLabel(
                exemplo_frame, text=dados["exemplo"],
                font=("Consolas", 13), text_color=self.cores["texto"],
                wraplength=600, justify="left"
            ).pack(anchor="w", padx=16, pady=(0, 14))

        if dados.get("dica"):
            ctk.CTkLabel(
                card, text=t(self.controller, "cursos_dica", dica=dados["dica"]),
                font=("Poppins", 13), text_color="#22c55e",
                wraplength=650, justify="left"
            ).pack(anchor="w", padx=28, pady=(0, 24))

        botoes = ctk.CTkFrame(scroll, fg_color="transparent")
        botoes.pack(fill="x")

        ctk.CTkButton(
            botoes, text=t(self.controller, "cursos_novo_topico"), width=200, height=46, corner_radius=12,
            fg_color="#2563eb", hover_color="#1d4ed8", font=("Poppins", 14, "bold"),
            command=self._gerar_licao
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            botoes, text=t(self.controller, "cursos_trocar_nivel"), width=180, height=46, corner_radius=12,
            fg_color="transparent", hover_color=self.cores["bg_input"],
            border_width=1, border_color=self.cores["borda"],
            text_color=self.cores["texto"], font=("Poppins", 14),
            command=self._mostrar_selecao_nivel
        ).pack(side="left")


# =====================================================
# 🔥 PÁGINA — MISSÕES
# =====================================================

class PaginaMissoes(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.cores = obter_cores(controller.tema_atual)
        self.pack(fill="both", expand=True)

        self._montar_tela()

    def _montar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=35, pady=35)

        topo = ctk.CTkFrame(scroll, fg_color="transparent")
        topo.pack(fill="x", pady=(0, 5))

        ctk.CTkLabel(
            topo, text=t(self.controller, "titulo_missoes"),
            font=("Poppins", 30, "bold"), text_color=self.cores["texto"]
        ).pack(side="left")

        moedas = obter_moedas(self.controller.usuario_id)
        ctk.CTkLabel(
            topo, text=t(self.controller, "missoes_moedas", moedas=moedas),
            font=("Poppins", 16, "bold"), text_color="#f59e0b",
            fg_color=self.cores["bg_input"], corner_radius=10, padx=14, pady=6
        ).pack(side="right")

        ctk.CTkFrame(scroll, fg_color=self.cores["bg_input"], height=1).pack(fill="x", pady=(15, 10))

        ctk.CTkLabel(
            scroll,
            text=t(self.controller, "missoes_subtitulo"),
            font=("Poppins", 12), text_color=self.cores["texto_secundario"],
            justify="left"
        ).pack(anchor="w", pady=(0, 20))

        missoes = obter_missoes(self.controller.usuario_id)

        for missao in missoes:
            self._criar_card_missao(scroll, missao)

    def _criar_card_missao(self, parent, missao):
        if missao["resgatada"]:
            cor_borda = "#22c55e"
        elif missao["pode_resgatar"]:
            cor_borda = "#f59e0b"
        else:
            cor_borda = self.cores["bg_input"]

        card = ctk.CTkFrame(
            parent, fg_color=self.cores["bg_card"],
            corner_radius=18, border_width=1, border_color=cor_borda
        )
        card.pack(fill="x", pady=8)

        linha = ctk.CTkFrame(card, fg_color="transparent")
        linha.pack(fill="x", padx=22, pady=(18, 6))

        ctk.CTkLabel(linha, text=missao["icone"], font=("Segoe UI Emoji", 26)).pack(side="left", padx=(0, 14))

        info = ctk.CTkFrame(linha, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            info, text=traduzir_missao_titulo(self.controller, missao),
            font=("Poppins", 15, "bold"), text_color=self.cores["texto"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            info, text=traduzir_missao_descricao(self.controller, missao),
            font=("Poppins", 12), text_color=self.cores["texto_secundario"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            linha, text=f"🪙 +{missao['recompensa']}",
            font=("Poppins", 13, "bold"), text_color="#f59e0b"
        ).pack(side="right", padx=(10, 0))

        # barra de progresso + texto "x/meta"
        rodape = ctk.CTkFrame(card, fg_color="transparent")
        rodape.pack(fill="x", padx=22, pady=(0, 10))

        barra = ctk.CTkProgressBar(
            rodape, height=8,
            progress_color="#22c55e" if missao["concluida"] else "#2563eb",
            fg_color=self.cores["bg_input"]
        )
        barra.pack(fill="x", side="left", expand=True, padx=(0, 10))
        barra.set(missao["progresso"] / missao["meta"])

        ctk.CTkLabel(
            rodape, text=f"{missao['progresso']}/{missao['meta']}",
            font=("Poppins", 11, "bold"), text_color=self.cores["texto_secundario"]
        ).pack(side="left")

        # rodapé de ação
        if missao["resgatada"]:
            ctk.CTkLabel(
                card, text=t(self.controller, "missoes_resgatada"),
                font=("Poppins", 12, "bold"), text_color="#22c55e"
            ).pack(anchor="w", padx=22, pady=(0, 16))

        elif missao["pode_resgatar"]:
            ctk.CTkButton(
                card, text=t(self.controller, "missoes_resgatar", valor=missao["recompensa"]),
                width=220, height=38, corner_radius=10,
                fg_color="#f59e0b", hover_color="#d97706",
                text_color="#111827", font=("Poppins", 13, "bold"),
                command=lambda c=missao["chave"]: self._resgatar(c)
            ).pack(anchor="w", padx=22, pady=(0, 16))

        else:
            ctk.CTkLabel(
                card, text=t(self.controller, "missoes_em_progresso"),
                font=("Poppins", 11), text_color=self.cores["texto_apagado"]
            ).pack(anchor="w", padx=22, pady=(0, 16))

    def _resgatar(self, missao_chave):
        sucesso, moedas_ganhas = resgatar_missao(self.controller.usuario_id, missao_chave)

        if sucesso:
            # atualiza o saldo mostrado na barra lateral, se ela existir
            mainscreen = getattr(self.controller, "mainscreen_atual", None)
            if mainscreen and mainscreen.winfo_exists():
                mainscreen.atualizar_moedas()

        # redesenha a tela com os dados atualizados (missão resgatada, saldo novo)
        self._montar_tela()


# =====================================================
# 🔥 PÁGINA — PERFIL
# =====================================================

class PaginaPerfil(ctk.CTkFrame):

    def carregar_perfil_salvo(self):
        try:
            dados = carregar_perfil(self.controller.usuario_id)
            if not dados:
                return

            bio, foto_blob = dados

            self.entrada_bio.delete("1.0", "end")
            if bio:
                self.entrada_bio.insert("1.0", bio)

            if foto_blob:
                foto = blob_para_foto_circular(foto_blob, 110)
                self._foto_ref = foto
                self.lbl_foto.configure(image=foto)
            else:
                self.lbl_foto.configure(image=self._placeholder)
                self._foto_ref = self._placeholder

        except Exception as e:
            print("Erro ao carregar perfil:", e)
            self.lbl_foto.configure(image=self._placeholder)

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.cores = obter_cores(controller.tema_atual)
        self._foto_ref = None
        self._foto_caminho = None

        self.pack(fill="both", expand=True)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=35, pady=25)

        topo = ctk.CTkFrame(self.scroll, fg_color="transparent")
        topo.pack(fill="x", pady=(0, 5))

        ctk.CTkLabel(
            topo, text=t(controller, "titulo_perfil"),
            font=("Poppins", 30, "bold"), text_color=self.cores["texto"]
        ).pack(side="left")

        texto_tema = t(controller, "config_tema_claro") if controller.tema_atual == "dark" else t(controller, "config_tema_escuro")

        self.btn_tema = ctk.CTkButton(
            topo,
            text=texto_tema,
            width=140, height=36, corner_radius=10,
            fg_color=self.cores["bg_input"], hover_color=self.cores["bg_hover"],
            text_color=self.cores["texto_secundario"], font=("Poppins", 12, "bold"),
            command=self.alternar_tema
        )
        self.btn_tema.pack(side="right")

        ctk.CTkFrame(self.scroll, fg_color=self.cores["bg_input"], height=1).pack(fill="x", pady=(8, 20))

        card = ctk.CTkFrame(
            self.scroll, fg_color=self.cores["bg_card"],
            corner_radius=20, border_width=1, border_color=self.cores["bg_input"]
        )
        card.pack(fill="x", pady=(0, 20))

        foto_area = ctk.CTkFrame(card, fg_color="transparent")
        foto_area.pack(pady=(30, 10))

        foto_container = ctk.CTkFrame(
            foto_area, fg_color=self.cores["bg_card"],
            corner_radius=60, width=120, height=120, cursor="hand2"
        )
        foto_container.pack()
        foto_container.pack_propagate(False)

        self._placeholder = fazer_placeholder_circular(110)
        self.lbl_foto = ctk.CTkLabel(
            foto_container, image=self._placeholder, text="", cursor="hand2"
        )
        self.lbl_foto.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_dica = ctk.CTkLabel(
            foto_container, text="✏️",
            font=("Poppins", 13), text_color="#2563eb",
            fg_color="transparent", cursor="hand2"
        )
        self.lbl_dica.place(relx=0.95, rely=0.75)

        foto_container.bind("<Button-1>", lambda e: self.abrir_seletor())
        self.lbl_foto.bind("<Button-1>",  lambda e: self.abrir_seletor())
        self.lbl_dica.bind("<Button-1>",  lambda e: self.abrir_seletor())

        ctk.CTkLabel(card, text=t(controller, "perfil_nome_label"), font=("Poppins", 11), text_color=self.cores["texto_apagado"]).pack()

        self.entrada_nome = ctk.CTkEntry(
            card, placeholder_text=t(controller, "perfil_nome_placeholder"),
            width=260, height=40, corner_radius=10,
            font=("Poppins", 15, "bold"),
            fg_color=self.cores["bg_input"], border_color=self.cores["borda"], justify="center"
        )
        self.entrada_nome.pack(pady=(4, 20))

        if controller.nome_usuario:
            self.entrada_nome.insert(0, controller.nome_usuario)

        bio_frame = ctk.CTkFrame(card, fg_color="transparent")
        bio_frame.pack(fill="x", padx=30, pady=(0, 10))

        ctk.CTkLabel(bio_frame, text=t(controller, "perfil_bio_label"), font=("Poppins", 12), text_color=self.cores["texto_apagado"]).pack(anchor="w")

        self.entrada_bio = ctk.CTkTextbox(
            bio_frame, height=90, corner_radius=10,
            font=("Poppins", 13), fg_color=self.cores["bg_input"],
            border_color=self.cores["borda"], border_width=1, wrap="word"
        )
        self.entrada_bio.pack(fill="x", pady=(4, 0))

        self.lbl_sucesso = ctk.CTkLabel(
            card,
            text=t(controller, "perfil_sucesso"),
            font=("Poppins", 13, "bold"),
            text_color="#22c55e", fg_color="transparent"
        )

        ctk.CTkButton(
            card, text=t(controller, "perfil_salvar"),
            width=180, height=40, corner_radius=10,
            fg_color="#2563eb", hover_color="#1d4ed8",
            font=("Poppins", 13, "bold"),
            command=self.salvar_perfil
        ).pack(anchor="e", padx=30, pady=(10, 25))

        ctk.CTkFrame(self.scroll, fg_color=self.cores["bg_input"], height=1).pack(fill="x", pady=(10, 20))

        card_conta = ctk.CTkFrame(
            self.scroll, fg_color=self.cores["bg_card"],
            corner_radius=20, border_width=1, border_color=self.cores["bg_input"]
        )
        card_conta.pack(fill="x", pady=(0, 30))

        ctk.CTkLabel(
            card_conta, text=t(controller, "perfil_conta"),
            font=("Poppins", 16, "bold"), text_color=self.cores["texto_secundario"]
        ).pack(anchor="w", padx=25, pady=(20, 15))

        ctk.CTkFrame(card_conta, fg_color=self.cores["bg_input"], height=1).pack(fill="x", padx=25, pady=(0, 15))

        linha_dificuldade = ctk.CTkFrame(card_conta, fg_color="transparent")
        linha_dificuldade.pack(fill="x", padx=25, pady=(0, 20))

        ctk.CTkLabel(
            linha_dificuldade,
            text=t(controller, "perfil_dificuldade_atual", nivel=traduzir_nivel(controller, controller.nivel_usuario) or "N/A"),
            font=("Poppins", 13, "bold"), text_color=self.cores["texto"]
        ).pack(side="left")

        ctk.CTkButton(
            linha_dificuldade,
            text=t(controller, "perfil_mudar_dificuldade"),
            width=180, height=38, corner_radius=10,
            fg_color=self.cores["bg_input"], hover_color=self.cores["bg_hover"],
            text_color="#2563eb", font=("Poppins", 12, "bold"),
            command=self.abrir_seletor_dificuldade
        ).pack(side="right")

        self.carregar_perfil_salvo()

    def abrir_seletor(self):
        SeletorAvatar(self, ao_selecionar=self.aplicar_avatar, controller=self.controller)

    def aplicar_avatar(self, caminho: str):
        try:
            nova_foto = fazer_foto_circular(caminho, 110)
            self._foto_ref     = nova_foto
            self._foto_caminho = caminho
            self.lbl_foto.configure(image=nova_foto)
        except Exception as e:
            print("Erro ao aplicar avatar:", e)

    def abrir_seletor_dificuldade(self):
        SeletorDificuldade(
            self.winfo_toplevel(), self.controller, self.cores,
            self.controller.nivel_usuario, self._mudar_dificuldade
        )

    def _mudar_dificuldade(self, novo_nivel):
        if not novo_nivel or novo_nivel == self.controller.nivel_usuario:
            return
        salvar_nivel(self.controller.usuario_id, novo_nivel)
        self.controller.nivel_usuario = novo_nivel
        self.controller.ir_para_main(novo_nivel)

    def alternar_tema(self):
        # o controller reconstrói a tela inteira com o novo tema,
        # então esta página (e o botão) já são recriados do zero
        # com o texto/ícone corretos — não precisa mexer neles aqui.
        self.controller.alternar_tema()

    def salvar_perfil(self):
        nome = self.entrada_nome.get().strip()
        bio  = self.entrada_bio.get("1.0", "end-1c").strip()

        salvar_informacoes_perfil(
            usuario_id=self.controller.usuario_id,
            nome=nome,
            biografia=bio,
            caminho_foto=self._foto_caminho
        )

        self.controller.nome_usuario = nome
        self.lbl_sucesso.pack(pady=(0, 8))
        self.after(3000, self._esconder_sucesso)

    def _esconder_sucesso(self):
        self.lbl_sucesso.pack_forget()


# =====================================================
# 🔥 PÁGINA — CONFIGURAÇÕES
# =====================================================

class PaginaConfiguracoes(ctk.CTkFrame):
    """
    Aba de configurações: idioma da interface (PT-BR / EN),
    aparência (modo claro/escuro) e ações de conta
    (sair da conta / deletar conta).
    """

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.cores = obter_cores(controller.tema_atual)

        self.pack(fill="both", expand=True)
        self._montar_tela()

    def _montar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

        c = self.controller

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=35, pady=35)

        ctk.CTkLabel(
            scroll, text=t(c, "config_titulo"),
            font=("Poppins", 30, "bold"), text_color=self.cores["texto"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            scroll, text=t(c, "config_subtitulo"),
            font=("Poppins", 13), text_color=self.cores["texto_secundario"]
        ).pack(anchor="w", pady=(4, 25))

        # -------------------------------------------
        # CARD — IDIOMA
        # -------------------------------------------
        card_idioma = ctk.CTkFrame(
            scroll, fg_color=self.cores["bg_card"],
            corner_radius=20, border_width=1, border_color=self.cores["bg_input"]
        )
        card_idioma.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            card_idioma, text=t(c, "config_idioma_titulo"),
            font=("Poppins", 16, "bold"), text_color=self.cores["texto"]
        ).pack(anchor="w", padx=25, pady=(20, 2))

        ctk.CTkLabel(
            card_idioma, text=t(c, "config_idioma_subtitulo"),
            font=("Poppins", 12), text_color=self.cores["texto_apagado"]
        ).pack(anchor="w", padx=25, pady=(0, 15))

        linha_idioma = ctk.CTkFrame(card_idioma, fg_color="transparent")
        linha_idioma.pack(fill="x", padx=25, pady=(0, 20))

        ativo   = "#2563eb"
        inativo = self.cores["bg_input"]

        self.btn_pt = ctk.CTkButton(
            linha_idioma, text="🇧🇷  Português (BR)",
            width=190, height=42, corner_radius=10,
            fg_color=ativo if c.idioma == "pt" else inativo,
            hover_color="#1d4ed8" if c.idioma == "pt" else self.cores["bg_hover"],
            text_color="#ffffff" if c.idioma == "pt" else self.cores["texto_secundario"],
            font=("Poppins", 13, "bold"),
            command=lambda: c.alternar_idioma("pt")
        )
        self.btn_pt.pack(side="left", padx=(0, 12))

        self.btn_en = ctk.CTkButton(
            linha_idioma, text="🇺🇸  English",
            width=190, height=42, corner_radius=10,
            fg_color=ativo if c.idioma == "en" else inativo,
            hover_color="#1d4ed8" if c.idioma == "en" else self.cores["bg_hover"],
            text_color="#ffffff" if c.idioma == "en" else self.cores["texto_secundario"],
            font=("Poppins", 13, "bold"),
            command=lambda: c.alternar_idioma("en")
        )
        self.btn_en.pack(side="left")

        # -------------------------------------------
        # CARD — APARÊNCIA (tema claro/escuro)
        # -------------------------------------------
        card_tema = ctk.CTkFrame(
            scroll, fg_color=self.cores["bg_card"],
            corner_radius=20, border_width=1, border_color=self.cores["bg_input"]
        )
        card_tema.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            card_tema, text=t(c, "config_tema_titulo"),
            font=("Poppins", 16, "bold"), text_color=self.cores["texto"]
        ).pack(anchor="w", padx=25, pady=(20, 2))

        ctk.CTkLabel(
            card_tema, text=t(c, "config_tema_subtitulo"),
            font=("Poppins", 12), text_color=self.cores["texto_apagado"]
        ).pack(anchor="w", padx=25, pady=(0, 15))

        texto_tema = t(c, "config_tema_claro") if c.tema_atual == "dark" else t(c, "config_tema_escuro")

        ctk.CTkButton(
            card_tema, text=texto_tema,
            width=190, height=42, corner_radius=10,
            fg_color=self.cores["bg_input"], hover_color=self.cores["bg_hover"],
            text_color=self.cores["texto_secundario"], font=("Poppins", 13, "bold"),
            command=c.alternar_tema
        ).pack(anchor="w", padx=25, pady=(0, 20))

        # -------------------------------------------
        # CARD — CONTA (sair / deletar)
        # -------------------------------------------
        card_conta = ctk.CTkFrame(
            scroll, fg_color=self.cores["bg_card"],
            corner_radius=20, border_width=1, border_color=self.cores["bg_input"]
        )
        card_conta.pack(fill="x", pady=(0, 30))

        ctk.CTkLabel(
            card_conta, text=t(c, "config_conta_titulo"),
            font=("Poppins", 16, "bold"), text_color=self.cores["texto"]
        ).pack(anchor="w", padx=25, pady=(20, 2))

        ctk.CTkLabel(
            card_conta, text=t(c, "config_conta_subtitulo"),
            font=("Poppins", 12), text_color=self.cores["texto_apagado"]
        ).pack(anchor="w", padx=25, pady=(0, 15))

        ctk.CTkFrame(card_conta, fg_color=self.cores["bg_input"], height=1).pack(fill="x", padx=25, pady=(0, 15))

        linha_botoes = ctk.CTkFrame(card_conta, fg_color="transparent")
        linha_botoes.pack(fill="x", padx=25, pady=(0, 20))

        ctk.CTkButton(
            linha_botoes,
            text=t(c, "config_sair"),
            width=180, height=42, corner_radius=10,
            fg_color=self.cores["bg_input"], hover_color=self.cores["borda"],
            text_color=self.cores["texto_secundario"], font=("Poppins", 13, "bold"),
            command=self.confirmar_sair
        ).pack(side="left", padx=(0, 15))

        ctk.CTkButton(
            linha_botoes,
            text=t(c, "config_deletar"),
            width=180, height=42, corner_radius=10,
            fg_color=self.cores["bg_input"], hover_color="#450a0a",
            text_color="#ef4444", font=("Poppins", 13, "bold"),
            border_width=1, border_color="#7f1d1d",
            command=self.confirmar_deletar
        ).pack(side="left")

    def confirmar_sair(self):
        c = self.controller
        resposta = messagebox.askyesno(
            t(c, "confirmar_sair_titulo"),
            t(c, "confirmar_sair_texto"),
            icon="question"
        )
        if resposta:
            c.sair_da_conta()

    def confirmar_deletar(self):
        c = self.controller

        resposta = messagebox.askyesno(
            t(c, "confirmar_deletar_titulo"),
            t(c, "confirmar_deletar_texto"),
            icon="warning"
        )
        if not resposta:
            return

        resposta2 = messagebox.askyesno(
            t(c, "confirmar_deletar2_titulo"),
            t(c, "confirmar_deletar2_texto", nome=c.nome_usuario),
            icon="warning"
        )
        if not resposta2:
            return

        try:
            deletar_usuario(c.usuario_id)
            messagebox.showinfo(t(c, "conta_deletada_titulo"), t(c, "conta_deletada_texto"))
            c.sair_da_conta()
        except Exception as e:
            messagebox.showerror(t(c, "erro_titulo"), t(c, "erro_deletar_texto", erro=e))