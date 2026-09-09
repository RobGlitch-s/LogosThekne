import customtkinter as ctk

from screens.start_screen import StartScreen
from screens.level_screen import LevelScreen
from screens.main_screen import MainScreen
from database import *
from utils import carregar_tema, obter_cores, salvar_tema

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        
        self.tema_atual = carregar_tema()
        ctk.set_appearance_mode(self.tema_atual)

        self.title("LogosThekne")
        self.geometry("500x720")
        self.resizable(False, False)
        self.configure(fg_color="#0f172a")

        # ==========================================
        # DADOS DA SESSÃO
        # ==========================================

        self.usuario_id = None
        self.nome_usuario = ""
        self.senha_usuario = ""

        self.materias_usuario = []
        self.nivel_usuario = ""

        self.jornada_iniciada = False

        self.idioma = "pt"

        # dificuldades que o usuário já recusou subir nesta sessão
        # (evita ficar sugerindo a mesma coisa toda hora)
        self.dificuldades_recusadas = set()

        # guarda a última rota/tela visitada, para conseguir
        # reconstruir a tela atual quando o tema mudar
        self._rota_atual = self.ir_para_inicio
        # guarda a última aba ativa dentro da MainScreen (Estudar/Missões/Perfil)
        self.aba_atual = "comecar"

        # ==========================================
        # CONTAINER PRINCIPAL
        # ==========================================

        self.frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.frame.pack(fill="both", expand=True)

        # ==========================================
        # PRIMEIRA TELA
        # ==========================================

        self.ir_para_inicio()

    # =====================================================
    # MÉTODO BASE DE TROCA DE TELAS
    # =====================================================

    def mostrar_tela(self, tela):
        self.focus_force()

        try:
            for widget in self.frame.winfo_children():
                widget.destroy()
        except:
            pass

        tela(self.frame, self).pack(fill="both", expand=True)

    # =====================================================
    # ROTAS
    # =====================================================

    def ir_para_inicio(self):
        self._rota_atual = self.ir_para_inicio

        self.geometry("500x720")
        self.resizable(True, True)

        self.mostrar_tela(StartScreen)

    def ir_para_level(self):
        self._rota_atual = self.ir_para_level

        self.geometry("500x720")
        self.resizable(True, True)

        self.mostrar_tela(
            lambda parent, controller:
                LevelScreen(parent, controller))
        
    def iniciar_jornada(self, nivel):

        if self.jornada_iniciada:
            return

        self.jornada_iniciada = True

        salvar_nivel(self.usuario_id, nivel)

        self.ir_para_main(nivel)
        

    # =====================================================
    # MAIN SCREEN
    # =====================================================

    def ir_para_main(self, nivel=None):

        if nivel:
            self.nivel_usuario = nivel

        self._rota_atual = lambda: self.ir_para_main(self.nivel_usuario)

        # garante estado correto da janela principal
        self.geometry("1100x700")
        self.resizable(True, True)

        # limpa tela atual
        for widget in self.frame.winfo_children():
            widget.destroy()

        # cria MainScreen
        MainScreen(
            self.frame,
            self,
            self.nivel_usuario
        ).pack(fill="both", expand=True)

        # garante foco correto da janela
        self.focus_force()
        self.update_idletasks()

    # =====================================================
    # LOGIN / SESSÃO
    # =====================================================

    def iniciar_sessao(
        self,
        usuario_id,
        nome,
        nivel=None
    ):

        self.usuario_id = usuario_id
        self.nome_usuario = nome

        self.nivel_usuario = nivel or ""

        # Usuário já configurou tudo
        if self.nivel_usuario:
            self.ir_para_main()

        # Ainda precisa escolher nível/matérias
        else:
            self.ir_para_level()

    # =====================================================
    # TEMA
    # =====================================================

    def alternar_tema(self):

        if self.tema_atual == "dark":
            self.tema_atual = "light"
        else:
            self.tema_atual = "dark"
            
        # 🔥 2. SALVA APENAS O TEMA (geral, sem o id do usuário)
        salvar_tema(self.tema_atual)

        ctk.set_appearance_mode(self.tema_atual)

        cores = obter_cores(self.tema_atual)
        self.configure(fg_color=cores["bg"])
        self.frame.configure(fg_color=cores["bg"])

        # Evita o erro de foco do Tkinter ao destruir a tela atual
        try:
            self.focus_set()
        except:
            pass

        # reconstrói a tela atual já com as cores do novo tema
        if self._rota_atual:
            self._rota_atual()

    # =====================================================
    # IDIOMA
    # =====================================================

    def alternar_idioma(self, novo_idioma):

        if novo_idioma not in ("pt", "en") or novo_idioma == self.idioma:
            return

        self.idioma = novo_idioma

        # reconstrói a tela atual já com os textos no idioma novo
        if self._rota_atual:
            self._rota_atual()

    # =====================================================
    # LOGOUT
    # =====================================================

    def sair_da_conta(self):

        self.nome_usuario = ""
        self.senha_usuario = ""
        self.materias_usuario = []
        self.nivel_usuario = ""
        self.usuario_id = None

        self.jornada_iniciada = False

        self.dificuldades_recusadas = set()

        self.reset_window()

        for widget in self.frame.winfo_children():
            widget.destroy()

        self.mostrar_tela(StartScreen)

        self.deiconify()

    # =====================================================
    # RESET COMPLETO DA SESSÃO
    # =====================================================

    def reset_window(self):
        self.geometry("500x720")
        self.resizable(True, True)
    
    def limpar_sessao(self):    

        self.usuario_id = None
        self.nome_usuario = ""
        self.senha_usuario = ""

        self.materias_usuario = []
        self.nivel_usuario = ""
        self.jornada_iniciada = False