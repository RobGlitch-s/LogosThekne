import math
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
 
from database import *
from registro import RegistroScreen
 
from utils import *
from idioma import t

 
 
class StartScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.cores = obter_cores(controller.tema_atual)
 
        self._anim_tick = 0.0
        self._anim_job  = None
        self._robo_id   = None
 
        adicionar_logo(self, CAMINHO_LOGO)
        adicionar_registro(self, command=self.abrir_registro, texto=t(controller, "registrar_botao"))
 
        container = ctk.CTkFrame(
            self, fg_color=self.cores["bg_card"], corner_radius=25,
            border_width=2, border_color="#2563eb",
            width=LARGURA_CONTAINER, height=ALTURA_CONTAINER + 40
        )
        container.place(relx=0.5, rely=POSICAO_VERTICAL_CONTAINER, anchor="center")
        container.pack_propagate(False)
 
        ctk.CTkLabel(container, text=t(controller, "login_passo"), font=("Poppins", 11), text_color=self.cores["texto_apagado"]).pack(pady=(16, 5))
 
        barra = ctk.CTkProgressBar(container, width=LARGURA_PROGRESSO, progress_color="#2563eb", fg_color=self.cores["bg_input"])
        barra.set(0.33)
        barra.pack(pady=(0, 10))
 
        # Frame tk puro como wrapper — necessário para o Canvas animar dentro do CTkFrame
        wrapper = tk.Frame(container, bg=self.cores["bg_card"], width=180, height=195)
        wrapper.pack(pady=(2, 2))
        wrapper.pack_propagate(False)
 
        self._canvas = tk.Canvas(
            wrapper,
            width=180, height=195,
            bg=self.cores["bg_card"],
            highlightthickness=0,
            bd=0
        )
        self._canvas.place(x=0, y=0)
 
        try:
            robo_pil = Image.open(CAMINHO_ROBO).convert("RGBA").resize((170, 170), Image.LANCZOS)
            self._robo_tk = ImageTk.PhotoImage(robo_pil)
            self._robo_id = self._canvas.create_image(90, 97, image=self._robo_tk, anchor="center")
            self.after(100, self._animar_robo)
        except Exception as e:
            print("ERRO ROBO:", e)
 
        ctk.CTkLabel(container, text=t(controller, "login_bemvindo"), font=("Poppins", 28, "bold"), text_color=self.cores["texto"]).pack(pady=4)
        ctk.CTkLabel(container, text=t(controller, "login_subtitulo"),
                     font=("Poppins", 15), text_color=self.cores["texto_secundario"], wraplength=320, justify="center").pack(pady=(0, 8))

        # -----------------------------------------------
        # LABEL DE ERRO — sempre no layout, invisível por padrão
        # -----------------------------------------------
        self.lbl_erro_login = ctk.CTkLabel(
            container,
            text="",
            font=("Poppins", 12, "bold"),
            text_color="#ef4444",
            fg_color="transparent",
            wraplength=280,
            justify="center",
            height=0
        )
        self.lbl_erro_login.pack(pady=(0, 4))
 
        self.entrada_nome = ctk.CTkEntry(container, placeholder_text=t(controller, "login_placeholder_user"), width=240, height=42, corner_radius=12)
        self.entrada_nome.pack(pady=8)
 
        self.entrada_senha = self._criar_campo_senha(container, t(controller, "login_placeholder_senha"))
 
        ctk.CTkButton(
            container, text=t(controller, "login_botao"), width=270, height=54, corner_radius=14,
            fg_color="#2563eb", hover_color="#1d4ed8", font=("Poppins", 17, "bold"),
            command=self.ir_para_boas_vindas
        ).pack(pady=(4, 10))
 
        self.bind("<Destroy>", self._parar_animacao)

    def _criar_campo_senha(self, container, placeholder):
        """Cria o campo de senha com um botão de olho para mostrar/ocultar."""
        frame = ctk.CTkFrame(container, fg_color="transparent")
        frame.pack(pady=8)

        entry = ctk.CTkEntry(
            frame,
            placeholder_text=placeholder,
            width=198, height=42, corner_radius=12,
            show="*"
        )
        entry.pack(side="left")

        botao_olho = ctk.CTkButton(
            frame,
            text="👁",
            width=36, height=42, corner_radius=12,
            fg_color="#1f2937", hover_color=self.cores["borda"],
            font=("Poppins", 14),
            command=lambda: self._alternar_visibilidade(entry, botao_olho)
        )
        botao_olho.pack(side="left", padx=(6, 0))

        return entry

    def _alternar_visibilidade(self, entry, botao):
        if entry.cget("show") == "*":
            entry.configure(show="")
            botao.configure(text="🙈")
        else:
            entry.configure(show="*")
            botao.configure(text="👁")

    # -----------------------------------------------
    # HELPERS DE ERRO DO LOGIN
    # -----------------------------------------------

    def mostrar_erro_login(self, mensagem: str):
        self.lbl_erro_login.configure(text=f"⚠️  {mensagem}", height=30)

    def limpar_erro_login(self):
        self.lbl_erro_login.configure(text="", height=0)

    def resetar_bordas_login(self):
        self.entrada_nome.configure(border_color=self.cores["borda"])
        self.entrada_senha.configure(border_color=self.cores["borda"])
 
    def _animar_robo(self):
        if not self.winfo_exists() or self._robo_id is None:
            return
        try:
            self._anim_tick += 0.05
            offset_y = math.sin(self._anim_tick) * 12
            self._canvas.coords(self._robo_id, 90, 97 + offset_y)
            self._anim_job = self.after(20, self._animar_robo)
        except Exception:
            pass
 
    def _parar_animacao(self, event=None):
        if self._anim_job is not None:
            try:
                self.after_cancel(self._anim_job)
            except Exception:
                pass
            self._anim_job = None
 
    def abrir_registro(self):
        RegistroScreen(self)
 
    def ir_para_boas_vindas(self):
        # aceita tanto o nome de usuário quanto o e-mail
        identificador = self.entrada_nome.get().strip()
        senha = self.entrada_senha.get()

        self.limpar_erro_login()
        self.resetar_bordas_login()

        if not identificador or not senha:
            self.mostrar_erro_login(t(self.controller, "login_erro_campos"))
            if not identificador:
                self.entrada_nome.configure(border_color="#ef4444")
            if not senha:
                self.entrada_senha.configure(border_color="#ef4444")
            return

        usuario = verificar_login(identificador, senha)
        if not usuario:
            # mensagem genérica de propósito: não revela se o erro foi
            # no usuário/e-mail ou na senha (mais seguro para o login)
            self.mostrar_erro_login(t(self.controller, "login_erro_credenciais"))
            self.entrada_nome.configure(border_color="#ef4444")
            self.entrada_senha.configure(border_color="#ef4444")
            return
 
        dados = buscar_usuario(identificador)
        if not dados:
            self.mostrar_erro_login(t(self.controller, "login_erro_buscar"))
            return
 
        usuario_id = dados[0]
        nome_real  = dados[1]   # nome de usuário de verdade (mesmo logando por e-mail)
        nivel      = dados[3]
 
        self._parar_animacao()
 
        self.controller.iniciar_sessao(
            usuario_id=usuario_id,
            nome=nome_real,
            nivel=nivel
        )