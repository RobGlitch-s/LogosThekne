import customtkinter as ctk
from PIL import Image

from database import *

from utils import *
from idioma import t, traduzir_nivel

class LevelScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.cores = obter_cores(controller.tema_atual)
        self.nivel_selecionado = None
        self.frames_niveis = {}

        adicionar_logo(self, CAMINHO_LOGO)

        container = ctk.CTkFrame(
            self, fg_color=self.cores["bg_card"], corner_radius=25,
            border_width=2, border_color="#2563eb",
            width=LARGURA_CONTAINER, height=ALTURA_CONTAINER
        )
        container.place(relx=0.5, rely=POSICAO_VERTICAL_CONTAINER, anchor="center")
        container.pack_propagate(False)

        ctk.CTkLabel(container, text=t(controller, "nivel_passo"), font=("Poppins", 11), text_color="#64748b").pack(pady=(20, 5))

        barra = ctk.CTkProgressBar(container, width=LARGURA_PROGRESSO, progress_color="#2563eb", fg_color=self.cores["bg_input"])
        barra.set(1.0)
        barra.pack(pady=(0, 10))

        ctk.CTkLabel(
            container, text=t(controller, "nivel_titulo"),
            font=("Poppins", 24, "bold"), text_color=self.cores["texto"], justify="center"
        ).pack(pady=(5, 12))

        niveis = ["Iniciante", "Intermediário", "Avançado"]

        for nome_nivel in niveis:
            descricao = t(controller, f"nivel_desc_{nome_nivel}")
            frame = ctk.CTkFrame(
                container, fg_color=self.cores["bg_input"], corner_radius=18,
                border_width=1, border_color=self.cores["borda"], width=360, height=85, cursor="hand2"
            )
            frame.pack(pady=5)
            frame.pack_propagate(False)

            ctk.CTkLabel(frame, text=traduzir_nivel(controller, nome_nivel), font=("Poppins", 18, "bold"), text_color=self.cores["texto"]).pack(anchor="w", padx=20, pady=(12, 2))
            ctk.CTkLabel(frame, text=descricao, font=("Poppins", 11), text_color=self.cores["texto_secundario"]).pack(anchor="w", padx=20)

            self.frames_niveis[nome_nivel] = frame
            frame.bind("<Button-1>", lambda e, n=nome_nivel: self.selecionar_nivel(n))
            for widget in frame.winfo_children():
                widget.bind("<Button-1>", lambda e, n=nome_nivel: self.selecionar_nivel(n))

        self.botao_comecar = ctk.CTkButton(
            container, text=t(controller, "nivel_botao"), width=220, height=45, corner_radius=12,
            fg_color="#2563eb", hover_color="#1d4ed8", font=("Poppins", 15, "bold"),
            command=self.finalizar
        )

    def selecionar_nivel(self, nome_nivel):
        for nome, frame in self.frames_niveis.items():
            frame.configure(border_color=self.cores["borda"], fg_color=self.cores["bg_input"])
        self.frames_niveis[nome_nivel].configure(border_color="#2563eb", fg_color=self.cores["bg_hover"])
        
        self.nivel_selecionado = nome_nivel
        
        self.botao_comecar.pack(pady=15)

    def finalizar(self):

        if not self.nivel_selecionado:
            return

        usuario_id = self.controller.usuario_id

        # só guarda estado
        self.controller.nivel_usuario = self.nivel_selecionado

        self.controller.iniciar_jornada(self.nivel_selecionado)