import re
import socket

import customtkinter as ctk
from database import salvar_usuario, email_existe, usuario_existe
from idioma import t

# =====================================================
# VALIDAÇÃO DE E-MAIL
# =====================================================
# Tentamos usar a biblioteca "email-validator", que checa o
# formato E também se o domínio do e-mail realmente existe
# (consultando os registros MX do domínio na internet).
#
# Para instalar (recomendado):
#     pip install email-validator
#
# Caso ela não esteja instalada, o código continua funcionando
# usando um método alternativo (fallback) mais simples, que
# verifica ao menos se o domínio do e-mail existe na internet.
try:
    from email_validator import validate_email, EmailNotValidError
    EMAIL_VALIDATOR_DISPONIVEL = True
except ImportError:
    EMAIL_VALIDATOR_DISPONIVEL = False

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+$")


def validar_email(email: str, idioma: str = "pt"):
    """
    Verifica se o e-mail é válido:
      1) Precisa conter '@'
      2) Precisa ter um formato correto (usuário@dominio.com)
      3) Precisa ter um domínio que realmente exista (funcional)

    Retorna (True, "") se for válido,
    ou (False, "mensagem explicando o erro") se não for.
    """

    email = email.strip()

    en = idioma == "en"

    if "@" not in email:
        return False, "The email must contain '@'." if en else "O e-mail precisa conter '@'."

    if not EMAIL_REGEX.match(email):
        return False, ("Enter a valid email format (ex: name@domain.com)." if en
                        else "Digite um e-mail em um formato válido (ex: nome@dominio.com).")

    dominio = email.split("@")[-1]

    if EMAIL_VALIDATOR_DISPONIVEL:
        try:
            # check_deliverability=True consulta o DNS do domínio
            # para confirmar que ele existe e aceita e-mails.
            validate_email(email, check_deliverability=True)
            return True, ""
        except EmailNotValidError:
            return False, "This email doesn't exist or is invalid." if en else "Este e-mail não existe ou não é válido."
    else:
        # Fallback (sem a biblioteca email-validator instalada):
        # verifica se o domínio do e-mail resolve na internet.
        try:
            socket.setdefaulttimeout(4)
            socket.gethostbyname(dominio)
            return True, ""
        except (socket.gaierror, socket.timeout):
            return False, "This email's domain doesn't exist." if en else "O domínio deste e-mail não existe."


# =====================================================
# VALIDAÇÃO DE NOME DE USUÁRIO
# =====================================================

NOME_REGEX = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9_]{3,20}$")


def validar_nome(nome: str, idioma: str = "pt"):
    """
    Regras do nome de usuário:
      - mínimo 3 caracteres
      - máximo 20 caracteres
      - apenas letras, números e '_' (sem espaços ou símbolos)

    Retorna (True, "") se o nome for válido,
    ou (False, "mensagem explicando o erro") caso contrário.
    """

    en = idioma == "en"

    if len(nome) < 3:
        return False, "The username must have at least 3 characters." if en else "O nome de usuário precisa ter no mínimo 3 caracteres."

    if len(nome) > 20:
        return False, "The username can have at most 20 characters." if en else "O nome de usuário pode ter no máximo 20 caracteres."

    if not NOME_REGEX.match(nome):
        return False, ("The username can only have letters, numbers and '_' (no spaces)." if en
                        else "O nome de usuário só pode ter letras, números e '_' (sem espaços).")

    return True, ""


# =====================================================
# VALIDAÇÃO DE SENHA FORTE
# =====================================================

REGEX_MAIUSCULA = re.compile(r"[A-Z]")
REGEX_MINUSCULA = re.compile(r"[a-z]")
REGEX_NUMERO = re.compile(r"[0-9]")
REGEX_ESPECIAL = re.compile(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\\[\];']")


def validar_senha_forte(senha: str, idioma: str = "pt"):
    """
    Regras de senha forte:
      - mínimo 8 caracteres
      - pelo menos 1 letra maiúscula
      - pelo menos 1 letra minúscula
      - pelo menos 1 número
      - pelo menos 1 caractere especial

    Retorna (True, "") se a senha for forte,
    ou (False, "mensagem explicando o que falta") caso contrário.
    """

    en = idioma == "en"

    if len(senha) < 8:
        return False, "The password must have at least 8 characters." if en else "A senha precisa ter no mínimo 8 caracteres."

    if not REGEX_MAIUSCULA.search(senha):
        return False, "The password needs at least 1 uppercase letter." if en else "A senha precisa ter ao menos 1 letra maiúscula."

    if not REGEX_MINUSCULA.search(senha):
        return False, "The password needs at least 1 lowercase letter." if en else "A senha precisa ter ao menos 1 letra minúscula."

    if not REGEX_NUMERO.search(senha):
        return False, "The password needs at least 1 number." if en else "A senha precisa ter ao menos 1 número."

    if not REGEX_ESPECIAL.search(senha):
        return False, ("The password needs at least 1 special character (!@#$%...)." if en
                        else "A senha precisa ter ao menos 1 caractere especial (!@#$%...).")

    return True, ""


class RegistroScreen(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.controller = getattr(parent, "controller", None)
        self.title(t(self.controller, "registro_titulo"))
        self.geometry("420x640")
        self.configure(fg_color="#0f172a")
        self.grab_set()

        container = ctk.CTkFrame(
            self,
            fg_color="#111827",
            corner_radius=20,
            border_width=2,
            border_color="#2563eb"
        )
        container.pack(fill="both", expand=True, padx=25, pady=25)

        ctk.CTkLabel(
            container,
            text=t(self.controller, "registro_titulo"),
            font=("Poppins", 28, "bold"),
            text_color="#f8fafc"
        ).pack(pady=(30, 5))

        ctk.CTkLabel(
            container,
            text=t(self.controller, "registro_subtitulo"),
            font=("Poppins", 14),
            text_color="#94a3b8"
        ).pack(pady=(0, 15))

        # -----------------------------------------------
        # LABEL DE ERRO — sempre no layout, invisível por padrão
        # -----------------------------------------------
        self.lbl_erro = ctk.CTkLabel(
            container,
            text="",
            font=("Poppins", 12, "bold"),
            text_color="#ef4444",
            fg_color="transparent",
            wraplength=260,
            justify="center",
            height=0
        )
        self.lbl_erro.pack(pady=(0, 5))

        self.entry_nome = ctk.CTkEntry(
            container,
            placeholder_text=t(self.controller, "registro_nome"),
            width=260, height=42, corner_radius=12
        )
        self.entry_nome.pack(pady=8)

        self.entry_email = ctk.CTkEntry(
            container,
            placeholder_text=t(self.controller, "registro_email"),
            width=260, height=42, corner_radius=12
        )
        self.entry_email.pack(pady=8)

        # -----------------------------------------------
        # CAMPO DE SENHA (com botão de mostrar/ocultar)
        # -----------------------------------------------
        self.entry_senha = self._criar_campo_senha(
            container, t(self.controller, "registro_senha")
        )

        # Dica de requisitos da senha
        ctk.CTkLabel(
            container,
            text="Mínimo 8 caracteres, com maiúscula, minúscula,\nnúmero e caractere especial." if getattr(self.controller, "idioma", "pt") == "pt"
                 else "Minimum 8 characters, with uppercase, lowercase,\nnumber and special character.",
            font=("Poppins", 10),
            text_color="#64748b",
            justify="center"
        ).pack(pady=(0, 4))

        self.entry_confirmar = self._criar_campo_senha(
            container, t(self.controller, "registro_confirmar_senha")
        )

        ctk.CTkButton(
            container,
            text=t(self.controller, "registro_botao"),
            width=260, height=45, corner_radius=12,
            fg_color="#2563eb", hover_color="#1d4ed8",
            font=("Poppins", 15, "bold"),
            command=self.registrar
        ).pack(pady=(20, 10))

    # -----------------------------------------------
    # CRIA UM CAMPO DE SENHA COM BOTÃO "MOSTRAR/OCULTAR"
    # -----------------------------------------------

    def _criar_campo_senha(self, container, placeholder):
        frame = ctk.CTkFrame(container, fg_color="transparent")
        frame.pack(pady=8)

        entry = ctk.CTkEntry(
            frame,
            placeholder_text=placeholder,
            width=218, height=42, corner_radius=12,
            show="*"
        )
        entry.pack(side="left")

        botao_olho = ctk.CTkButton(
            frame,
            text="👁",
            width=36, height=42, corner_radius=12,
            fg_color="#1f2937", hover_color="#334155",
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
    # HELPERS DE ERRO
    # -----------------------------------------------

    def mostrar_erro(self, mensagem: str):
        self.lbl_erro.configure(
            text=f"⚠️  {mensagem}",
            text_color="#ef4444",
            height=30
        )

    def mostrar_info(self, mensagem: str):
        self.lbl_erro.configure(
            text=f"⏳  {mensagem}",
            text_color="#94a3b8",
            height=30
        )

    def mostrar_sucesso(self, mensagem: str):
        self.lbl_erro.configure(
            text=f"✅  {mensagem}",
            text_color="#22c55e",
            height=30
        )

    def limpar_erro(self):
        self.lbl_erro.configure(text="", height=0)

    def resetar_bordas(self):
        self.entry_nome.configure(border_color="#334155")
        self.entry_email.configure(border_color="#334155")
        self.entry_senha.configure(border_color="#334155")
        self.entry_confirmar.configure(border_color="#334155")

    # -----------------------------------------------
    # REGISTRAR
    # -----------------------------------------------

    def registrar(self):
        nome      = self.entry_nome.get().strip()
        email     = self.entry_email.get().strip()
        senha     = self.entry_senha.get()
        confirmar = self.entry_confirmar.get()

        self.limpar_erro()
        self.resetar_bordas()

        idioma = getattr(self.controller, "idioma", "pt")

        # campos vazios
        if not nome or not email or not senha or not confirmar:
            self.mostrar_erro(t(self.controller, "registro_erro_campos"))
            return

        # -----------------------------------------------
        # NOME — formato e disponibilidade
        # -----------------------------------------------
        nome_valido, msg_nome = validar_nome(nome, idioma)
        if not nome_valido:
            self.mostrar_erro(msg_nome)
            self.entry_nome.configure(border_color="#ef4444")
            return

        if usuario_existe(nome):
            self.mostrar_erro(
                "This username is already taken." if idioma == "en" else "Este nome de usuário já está em uso."
            )
            self.entry_nome.configure(border_color="#ef4444")
            return

        # -----------------------------------------------
        # E-MAIL — formato e existência real do domínio
        # -----------------------------------------------
        self.mostrar_info("Checking email..." if idioma == "en" else "Verificando e-mail...")
        self.update_idletasks()

        email_valido, msg_email = validar_email(email, idioma)
        if not email_valido:
            self.mostrar_erro(msg_email)
            self.entry_email.configure(border_color="#ef4444")
            return

        if email_existe(email):
            self.mostrar_erro(t(self.controller, "registro_erro_email_existe"))
            self.entry_email.configure(border_color="#ef4444")
            return

        # -----------------------------------------------
        # SENHA — força e confirmação
        # -----------------------------------------------
        senha_valida, msg_senha = validar_senha_forte(senha, idioma)
        if not senha_valida:
            self.mostrar_erro(msg_senha)
            self.entry_senha.configure(border_color="#ef4444")
            return

        if senha != confirmar:
            self.mostrar_erro(t(self.controller, "registro_erro_senha_diff"))
            self.entry_senha.configure(border_color="#ef4444")
            self.entry_confirmar.configure(border_color="#ef4444")
            return

        # -----------------------------------------------
        # TUDO CERTO — salva, avisa e fecha
        # -----------------------------------------------
        salvar_usuario(nome, email, senha)

        self.resetar_bordas()
        self.entry_nome.configure(border_color="#22c55e")
        self.entry_email.configure(border_color="#22c55e")
        self.entry_senha.configure(border_color="#22c55e")
        self.entry_confirmar.configure(border_color="#22c55e")
        self.mostrar_sucesso(t(self.controller, "registro_sucesso"))

        print("Usuário registrado com sucesso!")

        # aguarda 1.5s mostrando a confirmação antes de fechar a tela
        self.after(1500, self.destroy)