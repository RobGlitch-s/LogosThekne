"""
Módulo de internacionalização (i18n) do LogosThekne.

Guarda as traduções da interface em um dicionário e oferece uma
função `t()` que devolve o texto certo de acordo com o idioma
selecionado pelo usuário (guardado em controller.idioma).

Cobre o app inteiro: login, seleção de nível, menu lateral, Estudar
(jornada + quiz), Cursos, Missões, Perfil e Configurações.

IMPORTANTE: "Iniciante"/"Intermediário"/"Avançado" e "Hardware"/
"Redes"/"Programação" continuam salvos no banco de dados e usados
internamente SEMPRE em português (são identificadores, não texto de
tela) — só o que é MOSTRADO na tela é traduzido, via
`traduzir_nivel()` e `traduzir_materia()` abaixo.
"""

TRADUCOES = {
    "pt": {
        # -------------------------------------------------
        # LOGIN (start_screen.py)
        # -------------------------------------------------
        "login_passo":            "Passo 1 de 3",
        "login_bemvindo":         "Bem-vindo ao LogosThekne",
        "login_subtitulo":        "Seu aplicativo para evoluir no mundo da tecnologia",
        "login_placeholder_user": "Nome de usuário ou e-mail",
        "login_placeholder_senha": "Digite sua senha",
        "login_botao":            "Começar",
        "login_erro_campos":      "Preencha usuário/e-mail e senha.",
        "login_erro_credenciais": "Usuário, e-mail ou senha incorretos.",
        "login_erro_buscar":      "Erro ao buscar usuário.",
        "registrar_botao":        "Registrar",

        # -------------------------------------------------
        # SELEÇÃO DE NÍVEL (level_screen.py)
        # -------------------------------------------------
        "nivel_passo":     "Passo 3 de 3",
        "nivel_titulo":    "Qual nível você deseja\ncomeçar sua jornada?",
        "nivel_botao":     "Começar",

        # -------------------------------------------------
        # NOMES DE NÍVEL / MATÉRIA (apenas para EXIBIÇÃO)
        # -------------------------------------------------
        "nivel_nome_Iniciante":         "Iniciante",
        "nivel_nome_Intermediário":     "Intermediário",
        "nivel_nome_Avançado":          "Avançado",
        "nivel_desc_Iniciante":         "Ideal para quem está começando agora na tecnologia",
        "nivel_desc_Intermediário":     "Para quem já possui conhecimentos básicos",
        "nivel_desc_Avançado":          "Indicado para usuários com experiência em tecnologia",

        "materia_nome_Hardware":     "Hardware",
        "materia_nome_Redes":        "Redes",
        "materia_nome_Programação":  "Programação",
        "materia_desc_Hardware":     "Peças físicas do computador",
        "materia_desc_Redes":        "Conectividade e internet",
        "materia_desc_Programação":  "Criação de sistemas e apps",

        # -------------------------------------------------
        # MENU LATERAL
        # -------------------------------------------------
        "nav_estudar": "🚀  Estudar",
        "nav_cursos":  "📚  Cursos",
        "nav_missoes": "🎯  Missões",
        "nav_perfil":  "👤  Perfil",
        "nav_config":  "⚙️  Configurações",
        "sidebar_nivel": "Nível",

        # -------------------------------------------------
        # ESTUDAR — JORNADA (PaginaComecar: tela inicial)
        # -------------------------------------------------
        "jornada_titulo":         "Sua Jornada",
        "jornada_nivel_atual":    "Nível atual:  {nivel}",
        "jornada_escolher":       "Escolha o que deseja estudar:",
        "jornada_botao_comecar":  "▶   Começar",
        "trilha_proximo_nivel":   "Nível {n}",
        "trilha_progresso":       "{atual}/5 acertos para o próximo nível",

        # -------------------------------------------------
        # ESTUDAR — TROCAR NÍVEL
        # -------------------------------------------------
        "trocar_nivel_titulo":    "🔄 Trocar nível",
        "trocar_nivel_subtitulo": "Escolha para qual nível deseja mudar",
        "trocar_nivel_voltar":    "Voltar",

        # -------------------------------------------------
        # ESTUDAR — CARREGANDO / ERRO
        # -------------------------------------------------
        "quiz_gerando":       "Gerando pergunta...",
        "quiz_materia_nivel": "Matéria: {materia}  |  Nível: {nivel}",
        "quiz_erro_titulo":   "Erro ao conectar com a IA",
        "quiz_erro_subtitulo": "Verifique sua conexão e tente novamente.",
        "quiz_tentar_novamente": "🔄  Tentar novamente",
        "quiz_voltar":        "← Voltar",

        # -------------------------------------------------
        # ESTUDAR — TELA DA PERGUNTA
        # -------------------------------------------------
        "quiz_header_voltar":   "←  Voltar",
        "quiz_questao_de":      "Questão {atual} de {total}",
        "quiz_continuar":       "Continuar  →",
        "quiz_ver_resultado":   "Ver resultado  🏁",
        "quiz_materia_label":   "🎯  {materia}  |  Nível: {nivel}",
        "quiz_acertou":         "✅  Você acertou!",
        "quiz_errou":           "❌  Você errou! A resposta certa é a {letra}.",

        # -------------------------------------------------
        # SUGESTÃO DE DIFICULDADE (popup)
        # -------------------------------------------------
        "sugestao_titulo_janela":  "Você está indo muito bem!",
        "sugestao_titulo":         "Você está mandando bem!",
        "sugestao_texto":          "Parece que você já domina o nível {nivel}.\nQuer subir para o nível {proximo}?",
        "sugestao_sim":            "Sim, ir para {proximo}",
        "sugestao_nao":            "Continuar aqui",

        # -------------------------------------------------
        # SUBIDA DE NÍVEL (popup AnimacaoNivel)
        # -------------------------------------------------
        "subida_titulo":   "NÍVEL ACIMA!",
        "subida_texto":    "Você avançou para  {nivel}",
        "subida_rodape":   "Continue assim! 🚀",

        # -------------------------------------------------
        # ESTUDAR — RESULTADO FINAL
        # -------------------------------------------------
        "resultado_titulo":        "Rodada finalizada!",
        "resultado_acertos":       "Você acertou {acertos} de {total} questões",
        "resultado_nivel_interno": "Nível interno: {nivel}",
        "resultado_nivel_atual":   "Nível atual: {nivel}",
        "resultado_missao_pronta": "🎁  Você tem missão pronta pra resgatar: {nomes}!",
        "resultado_reiniciar":     "🔁 Reiniciar",
        "resultado_trocar_nivel":  "🔄 Trocar nível",
        "resultado_voltar_inicio": "🏠 Voltar ao início",

        # -------------------------------------------------
        # CURSOS (PaginaCursos)
        # -------------------------------------------------
        "titulo_cursos":       "📚  Cursos",
        "cursos_subtitulo":    "Escolha uma área para se aprofundar com aulas geradas por IA.",
        "cursos_de":           "📚  Cursos de {materia}",
        "cursos_escolha_nivel": "Escolha o nível de dificuldade da aula.",
        "cursos_preparando":   "Preparando sua aula...",
        "cursos_erro_titulo":  "Erro ao gerar a aula",
        "cursos_erro_texto":   "Verifique sua conexão e tente novamente.",
        "cursos_exemplo":      "💡  Exemplo",
        "cursos_dica":         "✅  Dica: {dica}",
        "cursos_novo_topico":  "🔄  Novo tópico",
        "cursos_trocar_nivel": "📖  Trocar nível",
        "cursos_aula_generica": "Aula",

        "cursos_nivel_emoji_Iniciante":     "🌱",
        "cursos_nivel_emoji_Intermediário": "⚙️",
        "cursos_nivel_emoji_Avançado":      "🚀",
        "cursos_nivel_desc_Iniciante":     "Pega a base e a lógica do assunto, começando do zero",
        "cursos_nivel_desc_Intermediário": "Aprofunda conceitos pra quem já manja o básico",
        "cursos_nivel_desc_Avançado":      "Tópicos avançados pra quem quer se especializar",

        # -------------------------------------------------
        # MISSÕES (PaginaMissoes)
        # -------------------------------------------------
        "titulo_missoes":       "🎯  Missões",
        "missoes_moedas":       "🪙  {moedas} moedas",
        "missoes_subtitulo":    "Complete as missões abaixo para ganhar moedas.\nNo futuro, você vai poder trocar suas moedas por itens e skins!",
        "missoes_resgatar":     "🎁  Resgatar +{valor} moedas",
        "missoes_resgatada":    "✅  Recompensa já resgatada",
        "missoes_em_progresso": "Em progresso...",

        "missao_concluir_5_atividades_titulo":    "Maratonista",
        "missao_concluir_5_atividades_desc":      "Conclua 5 atividades (rodadas de perguntas)",
        "missao_acertar_20_perguntas_titulo":     "Sabe-Tudo",
        "missao_acertar_20_perguntas_desc":       "Acerte 20 perguntas no total",
        "missao_subir_3_niveis_titulo":           "Em Ascensão",
        "missao_subir_3_niveis_desc":             "Suba de nível 3 vezes",

        # -------------------------------------------------
        # PERFIL (PaginaPerfil)
        # -------------------------------------------------
        "perfil_nome_label":   "Nome",
        "perfil_nome_placeholder": "Seu nome",
        "perfil_bio_label":    "Biografia",
        "perfil_sucesso":      "✅  Suas informações foram salvas com sucesso!",
        "perfil_salvar":       "💾  Salvar perfil",
        "perfil_conta":        "Conta",
        "perfil_dificuldade_atual": "🎚️  Dificuldade atual:  {nivel}",
        "perfil_mudar_dificuldade": "🔄  Mudar dificuldade",

        # -------------------------------------------------
        # SELETOR DE DIFICULDADE (popup)
        # -------------------------------------------------
        "seletor_dificuldade_titulo":    "Escolha sua dificuldade",
        "seletor_dificuldade_subtitulo": "Você pode mudar de dificuldade quando quiser.",
        "seletor_dificuldade_confirmar": "Confirmar",

        # -------------------------------------------------
        # SELETOR DE AVATAR (popup)
        # -------------------------------------------------
        "seletor_avatar_titulo":    "🤖  Escolha seu Avatar",
        "seletor_avatar_subtitulo": "Clique em um robô para usar como foto de perfil",
        "seletor_avatar_rosa":      "🌸  Rosa",
        "seletor_avatar_azul":      "🔵  Azul",

        # -------------------------------------------------
        # REGISTRO (registro.py)
        # -------------------------------------------------
        "registro_titulo":          "Criar Conta",
        "registro_subtitulo":       "Preencha os dados para se registrar",
        "registro_nome":            "Nome de usuário",
        "registro_email":           "E-mail",
        "registro_senha":           "Senha",
        "registro_confirmar_senha": "Confirmar senha",
        "registro_botao":           "Registrar",
        "registro_erro_campos":     "Preencha todos os campos antes de continuar.",
        "registro_erro_senha_diff": "Sua senha está diferente, tente novamente.",
        "registro_erro_email_existe": "Este e-mail já está cadastrado.",
        "registro_sucesso":         "Cadastro realizado com sucesso!",

        # -------------------------------------------------
        # PÁGINA DE CONFIGURAÇÕES
        # -------------------------------------------------
        "config_titulo":            "⚙️  Configurações",
        "config_subtitulo":         "Gerencie suas preferências e sua conta.",
        "config_idioma_titulo":     "🌐  Idioma",
        "config_idioma_subtitulo": "Escolha o idioma da interface do aplicativo.",
        "config_tema_titulo":       "🎨  Aparência",
        "config_tema_subtitulo":    "Alterne entre modo claro e escuro.",
        "config_tema_claro":        "☀️  Modo claro",
        "config_tema_escuro":       "🌙  Modo escuro",
        "config_conta_titulo":      "Conta",
        "config_conta_subtitulo":   "Ações relacionadas à sua conta no LogosThekne.",
        "config_sair":              "🚪  Sair da conta",
        "config_deletar":           "🗑️  Deletar conta",

        # diálogos de confirmação
        "confirmar_sair_titulo":   "Sair da conta",
        "confirmar_sair_texto":    "Tem certeza que deseja sair da sua conta?",
        "confirmar_deletar_titulo": "Deletar conta",
        "confirmar_deletar_texto": "⚠️ Tem certeza que deseja DELETAR sua conta?\n\nEssa ação é permanente e não pode ser desfeita.",
        "confirmar_deletar2_titulo": "Confirmar exclusão",
        "confirmar_deletar2_texto": "Você está prestes a deletar a conta de '{nome}' permanentemente.\n\nDeseja continuar?",
        "conta_deletada_titulo":  "Conta deletada",
        "conta_deletada_texto":   "Sua conta foi deletada com sucesso.",
        "erro_titulo":             "Erro",
        "erro_deletar_texto":      "Não foi possível deletar a conta:\n{erro}",
    },

    "en": {
        # -------------------------------------------------
        # LOGIN
        # -------------------------------------------------
        "login_passo":            "Step 1 of 3",
        "login_bemvindo":         "Welcome to LogosThekne",
        "login_subtitulo":        "Your app to level up in the world of technology",
        "login_placeholder_user": "Username or email",
        "login_placeholder_senha": "Enter your password",
        "login_botao":            "Start",
        "login_erro_campos":      "Fill in username/email and password.",
        "login_erro_credenciais": "Incorrect username, email or password.",
        "login_erro_buscar":      "Error fetching user.",
        "registrar_botao":        "Sign up",

        # -------------------------------------------------
        # LEVEL SELECTION
        # -------------------------------------------------
        "nivel_passo":     "Step 3 of 3",
        "nivel_titulo":    "Which level do you want\nto start your journey?",
        "nivel_botao":     "Start",

        # -------------------------------------------------
        # LEVEL / SUBJECT DISPLAY NAMES
        # -------------------------------------------------
        "nivel_nome_Iniciante":         "Beginner",
        "nivel_nome_Intermediário":     "Intermediate",
        "nivel_nome_Avançado":          "Advanced",
        "nivel_desc_Iniciante":         "Ideal for those just starting out in technology",
        "nivel_desc_Intermediário":     "For those who already have basic knowledge",
        "nivel_desc_Avançado":          "Recommended for users with experience in technology",

        "materia_nome_Hardware":     "Hardware",
        "materia_nome_Redes":        "Networking",
        "materia_nome_Programação":  "Programming",
        "materia_desc_Hardware":     "The physical parts of a computer",
        "materia_desc_Redes":        "Connectivity and the internet",
        "materia_desc_Programação":  "Building systems and apps",

        # -------------------------------------------------
        # SIDEBAR
        # -------------------------------------------------
        "nav_estudar": "🚀  Study",
        "nav_cursos":  "📚  Courses",
        "nav_missoes": "🎯  Missions",
        "nav_perfil":  "👤  Profile",
        "nav_config":  "⚙️  Settings",
        "sidebar_nivel": "Level",

        # -------------------------------------------------
        # STUDY — JOURNEY (home screen)
        # -------------------------------------------------
        "jornada_titulo":         "Your Journey",
        "jornada_nivel_atual":    "Current level:  {nivel}",
        "jornada_escolher":       "Choose what you want to study:",
        "jornada_botao_comecar":  "▶   Start",
        "trilha_proximo_nivel":   "Level {n}",
        "trilha_progresso":       "{atual}/5 correct answers to next level",

        # -------------------------------------------------
        # STUDY — CHANGE LEVEL
        # -------------------------------------------------
        "trocar_nivel_titulo":    "🔄 Change level",
        "trocar_nivel_subtitulo": "Choose which level you want to switch to",
        "trocar_nivel_voltar":    "Back",

        # -------------------------------------------------
        # STUDY — LOADING / ERROR
        # -------------------------------------------------
        "quiz_gerando":       "Generating question...",
        "quiz_materia_nivel": "Subject: {materia}  |  Level: {nivel}",
        "quiz_erro_titulo":   "Error connecting to the AI",
        "quiz_erro_subtitulo": "Check your connection and try again.",
        "quiz_tentar_novamente": "🔄  Try again",
        "quiz_voltar":        "← Back",

        # -------------------------------------------------
        # STUDY — QUESTION SCREEN
        # -------------------------------------------------
        "quiz_header_voltar":   "←  Back",
        "quiz_questao_de":      "Question {atual} of {total}",
        "quiz_continuar":       "Continue  →",
        "quiz_ver_resultado":   "See results  🏁",
        "quiz_materia_label":   "🎯  {materia}  |  Level: {nivel}",
        "quiz_acertou":         "✅  You got it right!",
        "quiz_errou":           "❌  You got it wrong! The correct answer is {letra}.",

        # -------------------------------------------------
        # DIFFICULTY SUGGESTION (popup)
        # -------------------------------------------------
        "sugestao_titulo_janela":  "You're doing great!",
        "sugestao_titulo":         "You're doing great!",
        "sugestao_texto":          "Looks like you've mastered the {nivel} level.\nWant to move up to {proximo}?",
        "sugestao_sim":            "Yes, go to {proximo}",
        "sugestao_nao":            "Stay here",

        # -------------------------------------------------
        # LEVEL UP (popup)
        # -------------------------------------------------
        "subida_titulo":   "LEVEL UP!",
        "subida_texto":    "You advanced to  {nivel}",
        "subida_rodape":   "Keep it up! 🚀",

        # -------------------------------------------------
        # STUDY — FINAL RESULTS
        # -------------------------------------------------
        "resultado_titulo":        "Round complete!",
        "resultado_acertos":       "You got {acertos} out of {total} questions right",
        "resultado_nivel_interno": "Internal level: {nivel}",
        "resultado_nivel_atual":   "Current level: {nivel}",
        "resultado_missao_pronta": "🎁  You have a mission ready to claim: {nomes}!",
        "resultado_reiniciar":     "🔁 Restart",
        "resultado_trocar_nivel":  "🔄 Change level",
        "resultado_voltar_inicio": "🏠 Back to home",

        # -------------------------------------------------
        # COURSES
        # -------------------------------------------------
        "titulo_cursos":       "📚  Courses",
        "cursos_subtitulo":    "Choose an area to dive deeper into with AI-generated lessons.",
        "cursos_de":           "📚  {materia} Courses",
        "cursos_escolha_nivel": "Choose the difficulty level of the lesson.",
        "cursos_preparando":   "Preparing your lesson...",
        "cursos_erro_titulo":  "Error generating the lesson",
        "cursos_erro_texto":   "Check your connection and try again.",
        "cursos_exemplo":      "💡  Example",
        "cursos_dica":         "✅  Tip: {dica}",
        "cursos_novo_topico":  "🔄  New topic",
        "cursos_trocar_nivel": "📖  Change level",
        "cursos_aula_generica": "Lesson",

        "cursos_nivel_emoji_Iniciante":     "🌱",
        "cursos_nivel_emoji_Intermediário": "⚙️",
        "cursos_nivel_emoji_Avançado":      "🚀",
        "cursos_nivel_desc_Iniciante":     "Covers the basics and core logic, starting from zero",
        "cursos_nivel_desc_Intermediário": "Goes deeper for those who already know the basics",
        "cursos_nivel_desc_Avançado":      "Advanced topics for those who want to specialize",

        # -------------------------------------------------
        # MISSIONS
        # -------------------------------------------------
        "titulo_missoes":       "🎯  Missions",
        "missoes_moedas":       "🪙  {moedas} coins",
        "missoes_subtitulo":    "Complete the missions below to earn coins.\nIn the future, you'll be able to trade your coins for items and skins!",
        "missoes_resgatar":     "🎁  Claim +{valor} coins",
        "missoes_resgatada":    "✅  Reward already claimed",
        "missoes_em_progresso": "In progress...",

        "missao_concluir_5_atividades_titulo":    "Marathoner",
        "missao_concluir_5_atividades_desc":      "Complete 5 activities (question rounds)",
        "missao_acertar_20_perguntas_titulo":     "Know-It-All",
        "missao_acertar_20_perguntas_desc":       "Answer 20 questions correctly in total",
        "missao_subir_3_niveis_titulo":           "On the Rise",
        "missao_subir_3_niveis_desc":             "Level up 3 times",

        # -------------------------------------------------
        # PROFILE
        # -------------------------------------------------
        "perfil_nome_label":   "Name",
        "perfil_nome_placeholder": "Your name",
        "perfil_bio_label":    "Bio",
        "perfil_sucesso":      "✅  Your info was saved successfully!",
        "perfil_salvar":       "💾  Save profile",
        "perfil_conta":        "Account",
        "perfil_dificuldade_atual": "🎚️  Current difficulty:  {nivel}",
        "perfil_mudar_dificuldade": "🔄  Change difficulty",

        # -------------------------------------------------
        # DIFFICULTY SELECTOR (popup)
        # -------------------------------------------------
        "seletor_dificuldade_titulo":    "Choose your difficulty",
        "seletor_dificuldade_subtitulo": "You can change difficulty whenever you want.",
        "seletor_dificuldade_confirmar": "Confirm",

        # -------------------------------------------------
        # AVATAR SELECTOR (popup)
        # -------------------------------------------------
        "seletor_avatar_titulo":    "🤖  Choose your Avatar",
        "seletor_avatar_subtitulo": "Click a robot to use it as your profile picture",
        "seletor_avatar_rosa":      "🌸  Pink",
        "seletor_avatar_azul":      "🔵  Blue",

        # -------------------------------------------------
        # SIGN UP
        # -------------------------------------------------
        "registro_titulo":          "Create Account",
        "registro_subtitulo":       "Fill in your details to sign up",
        "registro_nome":            "Username",
        "registro_email":           "Email",
        "registro_senha":           "Password",
        "registro_confirmar_senha": "Confirm password",
        "registro_botao":           "Sign up",
        "registro_erro_campos":     "Fill in all fields before continuing.",
        "registro_erro_senha_diff": "Your passwords don't match, try again.",
        "registro_erro_email_existe": "This email is already registered.",
        "registro_sucesso":         "Account created successfully!",

        # -------------------------------------------------
        # SETTINGS PAGE
        # -------------------------------------------------
        "config_titulo":            "⚙️  Settings",
        "config_subtitulo":         "Manage your preferences and your account.",
        "config_idioma_titulo":     "🌐  Language",
        "config_idioma_subtitulo": "Choose the app interface language.",
        "config_tema_titulo":       "🎨  Appearance",
        "config_tema_subtitulo":    "Switch between light and dark mode.",
        "config_tema_claro":        "☀️  Light mode",
        "config_tema_escuro":       "🌙  Dark mode",
        "config_conta_titulo":      "Account",
        "config_conta_subtitulo":   "Actions related to your LogosThekne account.",
        "config_sair":              "🚪  Log out",
        "config_deletar":           "🗑️  Delete account",

        # confirmation dialogs
        "confirmar_sair_titulo":   "Log out",
        "confirmar_sair_texto":    "Are you sure you want to log out of your account?",
        "confirmar_deletar_titulo": "Delete account",
        "confirmar_deletar_texto": "⚠️ Are you sure you want to DELETE your account?\n\nThis action is permanent and cannot be undone.",
        "confirmar_deletar2_titulo": "Confirm deletion",
        "confirmar_deletar2_texto": "You are about to permanently delete the account '{nome}'.\n\nDo you want to continue?",
        "conta_deletada_titulo":  "Account deleted",
        "conta_deletada_texto":   "Your account has been deleted successfully.",
        "erro_titulo":             "Error",
        "erro_deletar_texto":      "Could not delete the account:\n{erro}",
    },
}


def t(controller, chave, **kwargs):
    """
    Retorna o texto traduzido de acordo com o idioma atual do controller.
    Aceita placeholders opcionais via kwargs (ex: t(c, "x", nome="Ana")).
    """
    idioma = getattr(controller, "idioma", "pt")
    texto = TRADUCOES.get(idioma, TRADUCOES["pt"]).get(chave, chave)

    if kwargs:
        try:
            texto = texto.format(**kwargs)
        except Exception:
            pass

    return texto


def traduzir_nivel(controller, nivel: str) -> str:
    """
    Traduz o NOME de um nível (Iniciante/Intermediário/Avançado) só
    para exibição — o valor salvo no banco continua em português.
    """
    if not nivel:
        return nivel
    idioma = getattr(controller, "idioma", "pt")
    chave = f"nivel_nome_{nivel}"
    return TRADUCOES.get(idioma, {}).get(chave, nivel)


def traduzir_materia(controller, materia: str) -> str:
    """
    Traduz o NOME de uma matéria (Hardware/Redes/Programação) só
    para exibição — o valor salvo no banco continua em português.
    """
    if not materia:
        return materia
    idioma = getattr(controller, "idioma", "pt")
    chave = f"materia_nome_{materia}"
    return TRADUCOES.get(idioma, {}).get(chave, materia)


def traduzir_missao_titulo(controller, missao: dict) -> str:
    """Traduz o título de uma missão (dict vindo de database.obter_missoes)."""
    chave = f"missao_{missao['chave']}_titulo"
    idioma = getattr(controller, "idioma", "pt")
    return TRADUCOES.get(idioma, {}).get(chave, missao.get("titulo", ""))


def traduzir_missao_descricao(controller, missao: dict) -> str:
    """Traduz a descrição de uma missão (dict vindo de database.obter_missoes)."""
    chave = f"missao_{missao['chave']}_desc"
    idioma = getattr(controller, "idioma", "pt")
    return TRADUCOES.get(idioma, {}).get(chave, missao.get("descricao", ""))