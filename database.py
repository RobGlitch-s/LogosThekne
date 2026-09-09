import sqlite3
import hashlib

# =====================================================
# 🔥 SISTEMA DE MOEDAS / MISSÕES
# =====================================================
# Cada missão observa um "contador" que já existe (ou passa a existir)
# na tabela usuarios. Quando o contador atinge a meta, a missão fica
# pronta pra ser resgatada — e só quando o jogador clica em "Resgatar"
# é que as moedas entram de fato na conta dele.
#
# Pensado para crescer: no futuro, dá pra trocar essas moedas por
# itens/skins numa loja dentro do app.

MISSOES = [
    {
        "chave":      "concluir_5_atividades",
        "titulo":     "Maratonista",
        "descricao":  "Conclua 5 atividades (rodadas de perguntas)",
        "icone":      "🏃",
        "meta":       5,
        "recompensa": 50,
        "campo":      "atividades_concluidas",
    },
    {
        "chave":      "acertar_20_perguntas",
        "titulo":     "Sabe-Tudo",
        "descricao":  "Acerte 20 perguntas no total",
        "icone":      "🧠",
        "meta":       20,
        "recompensa": 30,
        "campo":      "acertos_globais",
    },
    {
        "chave":      "subir_3_niveis",
        "titulo":     "Em Ascensão",
        "descricao":  "Suba de nível 3 vezes",
        "icone":      "⬆️",
        "meta":       3,
        "recompensa": 40,
        "campo":      "nivel_interno",
    },
]

# =====================================================
# CRIAR BANCO
# =====================================================

def criar_banco():

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    # -----------------------------------------------
    # TABELA USUÁRIOS
    # -----------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        nome        TEXT UNIQUE NOT NULL,
        email       TEXT UNIQUE NOT NULL,
        senha       TEXT NOT NULL,
        nivel       TEXT,
        biografia   TEXT,
        
        level_barra_progresso INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        
        quiz_questao_atual INTEGER DEFAULT 0,
        quiz_acertos INTEGER DEFAULT 0,
        quiz_erros INTEGER DEFAULT 0,
        
        foto        BLOB
    )
    """)

    # -----------------------------------------------
    # 🔥 MIGRAÇÃO: colunas do sistema de moedas/missões
    # (ALTER TABLE dá erro se a coluna já existir — ignoramos
    # esse erro, pois só precisamos garantir que ela exista)
    # -----------------------------------------------
    colunas_novas = [
        ("moedas",                "INTEGER DEFAULT 0"),
        ("atividades_concluidas", "INTEGER DEFAULT 0"),
        ("acertos_globais",       "INTEGER DEFAULT 0"),
    ]

    for nome_coluna, tipo in colunas_novas:
        try:
            cursor.execute(f"ALTER TABLE usuarios ADD COLUMN {nome_coluna} {tipo}")
        except sqlite3.OperationalError:
            pass  # coluna já existe, tudo certo

    # -----------------------------------------------
    # TABELA DE MISSÕES JÁ RESGATADAS
    # -----------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progresso_missoes (
        usuario_id    INTEGER NOT NULL,
        missao_chave  TEXT NOT NULL,
        resgatada     INTEGER DEFAULT 0,
        PRIMARY KEY (usuario_id, missao_chave),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    """)

    # -----------------------------------------------
    # TABELA MATÉRIAS (fixas, populadas automaticamente)
    # -----------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materias (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_materia  TEXT UNIQUE NOT NULL
    )
    """)

    # -----------------------------------------------
    # TABELA DE RELACIONAMENTO usuario <-> materia
    # com progresso individual
    # -----------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario_materia (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id  INTEGER NOT NULL,
        materia_id  INTEGER NOT NULL,
        progresso   INTEGER DEFAULT 0,
        UNIQUE(usuario_id, materia_id),
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY(materia_id) REFERENCES materias(id)
    )
    """)

    # -----------------------------------------------
    # POPULA MATÉRIAS SE AINDA NÃO EXISTIREM
    # -----------------------------------------------
    materias_padrao = ["Hardware", "Redes", "Programação"]

    for materia in materias_padrao:
        cursor.execute("""
        INSERT OR IGNORE INTO materias (nome_materia)
        VALUES (?)
        """, (materia,))

    conn.commit()
    conn.close()


# =====================================================
# CRIPTOGRAFAR SENHA
# =====================================================

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


# =====================================================
# LOGIN
# =====================================================

def verificar_login(identificador, senha):
    """
    Faz login usando o nome de usuário OU o e-mail cadastrado.
    'identificador' pode ser o nome de usuário ou o e-mail.
    """

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    senha_hash = criptografar_senha(senha)
    identificador = identificador.strip()

    cursor.execute("""
    SELECT * FROM usuarios
    WHERE (nome = ? OR email = ?) AND senha = ?
    """, (identificador, identificador, senha_hash))

    usuario = cursor.fetchone()
    conn.close()
    return usuario


# =====================================================
# VERIFICAR SE EXISTE
# =====================================================

def usuario_existe(nome):

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM usuarios
    WHERE nome = ?
    """, (nome,))

    usuario = cursor.fetchone()
    conn.close()
    return usuario


# =====================================================
# SALVAR USUÁRIO
# =====================================================

def salvar_usuario(nome, email, senha):

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    senha_hash = criptografar_senha(senha)

    cursor.execute("""
    INSERT INTO usuarios (nome, email, senha)
    VALUES (?, ?, ?)
    """, (nome, email, senha_hash))

    conn.commit()
    conn.close()

    print("Usuário registrado!")


# =====================================================
# VERIFICAR EMAIL
# =====================================================

def email_existe(email):

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM usuarios
    WHERE email = ?
    """, (email,))

    usuario = cursor.fetchone()
    conn.close()
    return usuario


# =====================================================
# BUSCAR USUÁRIO COMPLETO
# =====================================================

def buscar_usuario(identificador):
    """
    Busca o usuário pelo nome de usuário OU pelo e-mail.
    """

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    identificador = identificador.strip()

    cursor.execute("""
    SELECT id, nome, email, nivel, biografia, foto
    FROM usuarios
    WHERE nome = ? OR email = ?
    """, (identificador, identificador))

    usuario = cursor.fetchone()
    conn.close()
    return usuario


# =====================================================
# SALVAR NÍVEL
# =====================================================

def salvar_nivel(usuario_id, nivel):

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE usuarios
    SET nivel = ?
    WHERE id = ?
    """, (nivel, usuario_id))

    conn.commit()
    conn.close()


# =====================================================
# BUSCAR ID DA MATÉRIA PELO NOME
# =====================================================

def buscar_id_materia(nome_materia):

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id FROM materias
    WHERE nome_materia = ?
    """, (nome_materia,))

    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None


# =====================================================
# INSCREVER USUÁRIO EM UMA MATÉRIA
# (cria o relacionamento com progresso 0)
# =====================================================

def inscrever_usuario_materia(usuario_id, nome_materia):

    materia_id = buscar_id_materia(nome_materia)

    if not materia_id:
        print(f"Matéria '{nome_materia}' não encontrada.")
        return

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO usuario_materia (usuario_id, materia_id, progresso)
    VALUES (?, ?, 0)
    """, (usuario_id, materia_id))

    conn.commit()
    conn.close()


# =====================================================
# BUSCAR MATÉRIAS DO USUÁRIO (com progresso)
# =====================================================

def buscar_materias_usuario(usuario_id):
    """
    Retorna lista de dicts:
    [{"materia": "Hardware", "progresso": 0}, ...]
    """

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT m.nome_materia, um.progresso
    FROM usuario_materia um
    JOIN materias m ON m.id = um.materia_id
    WHERE um.usuario_id = ?
    """, (usuario_id,))

    resultado = cursor.fetchall()
    conn.close()

    return [{"materia": row[0], "progresso": row[1]} for row in resultado]


# =====================================================
# BUSCAR NOMES DAS MATÉRIAS DO USUÁRIO (só nomes)
# =====================================================

def buscar_materias(usuario_id):
    """
    Retorna lista simples de nomes:
    ["Hardware", "Redes"]
    """

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT m.nome_materia
    FROM usuario_materia um
    JOIN materias m ON m.id = um.materia_id
    WHERE um.usuario_id = ?
    """, (usuario_id,))

    resultado = cursor.fetchall()
    conn.close()

    return [row[0] for row in resultado]


# =====================================================
# ATUALIZAR PROGRESSO DO USUÁRIO EM UMA MATÉRIA
# =====================================================

def atualizar_progresso(usuario_id, nome_materia, novo_progresso):

    materia_id = buscar_id_materia(nome_materia)

    if not materia_id:
        print(f"Matéria '{nome_materia}' não encontrada.")
        return

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE usuario_materia
    SET progresso = ?
    WHERE usuario_id = ? AND materia_id = ?
    """, (novo_progresso, usuario_id, materia_id))

    conn.commit()
    conn.close()


# =====================================================
# BUSCAR PROGRESSO DO USUÁRIO EM UMA MATÉRIA
# =====================================================

def buscar_progresso(usuario_id, nome_materia):

    materia_id = buscar_id_materia(nome_materia)

    if not materia_id:
        return 0

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT progresso
    FROM usuario_materia
    WHERE usuario_id = ? AND materia_id = ?
    """, (usuario_id, materia_id))

    resultado = cursor.fetchone()
    conn.close()

    return resultado[0] if resultado else 0


# =====================================================
# SALVAR MATÉRIA (compatibilidade com código antigo)
# =====================================================

def salvar_materia(usuario_id, materia):
    inscrever_usuario_materia(usuario_id, materia)


# =====================================================
# ATUALIZAR CONFIG DO USUÁRIO (nível)
# =====================================================

def atualizar_usuario_config(usuario_id, nivel):

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE usuarios
    SET nivel = ?
    WHERE id = ?
    """, (nivel, usuario_id))

    conn.commit()
    conn.close()


# =====================================================
# DELETAR USUÁRIO
# =====================================================

def deletar_usuario(usuario_id):

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM usuario_materia
    WHERE usuario_id = ?
    """, (usuario_id,))

    cursor.execute("""
    DELETE FROM usuarios
    WHERE id = ?
    """, (usuario_id,))

    conn.commit()
    conn.close()


# =====================================================
# SALVAR PERFIL
# =====================================================

def salvar_informacoes_perfil(
    usuario_id,
    nome=None,
    biografia=None,
    caminho_foto=None
):

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    campos = []
    valores = []

    if nome is not None:
        campos.append("nome = ?")
        valores.append(nome)

    if biografia is not None:
        campos.append("biografia = ?")
        valores.append(biografia)

    if caminho_foto is not None:
        try:
            with open(caminho_foto, "rb") as f:
                foto_bytes = f.read()
            campos.append("foto = ?")
            valores.append(sqlite3.Binary(foto_bytes))
        except Exception as e:
            print(f"Erro ao carregar foto: {e}")

    if campos:
        query = f"""
        UPDATE usuarios
        SET {', '.join(campos)}
        WHERE id = ?
        """
        valores.append(usuario_id)
        cursor.execute(query, valores)
        conn.commit()

    conn.close()


# =====================================================
# CARREGAR PERFIL
# =====================================================

def carregar_perfil(usuario_id):

    try:
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT biografia, foto
        FROM usuarios
        WHERE id = ?
        """, (usuario_id,))

        dados = cursor.fetchone()
        return dados if dados else (None, None)

    except Exception as e:
        print(f"Erro ao carregar perfil: {e}")
        return (None, None)

    finally:
        conn.close()


# =====================================================
# LISTAR TODAS AS MATÉRIAS DISPONÍVEIS
# =====================================================

def listar_materias():
    """
    Retorna todas as matérias cadastradas no sistema:
    ["Hardware", "Redes", "Programação"]
    """

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT nome_materia FROM materias
    ORDER BY id
    """)

    resultado = cursor.fetchall()
    conn.close()

    return [row[0] for row in resultado]

# ====================================================
# Level_manager
# ====================================================

def carregar_level(usuario_id):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT level, level_barra_progresso
        FROM usuarios
        WHERE id = ?
    """, (usuario_id,))

    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return resultado

    return (1, 0)


def salvar_level(usuario_id, level, progresso):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET level = ?,
            level_barra_progresso = ?
        WHERE id = ?
    """, (level, progresso, usuario_id))

    conn.commit()
    conn.close()
    
def adicionar_progresso(usuario_id):
    level, progresso = carregar_level(usuario_id)

    progresso += 1

    if progresso >= 5:
        level += 1
        progresso = 0

    salvar_level(usuario_id, level, progresso)

    return level, progresso

def resetar_level(usuario_id):
    salvar_level(usuario_id, 1, 0)
    
#====================================================
# Carregar progresso do quiz
#====================================================

def carregar_progresso_quiz(usuario_id):

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        quiz_questao_atual,
        quiz_acertos,
        quiz_erros
    FROM usuarios
    WHERE id = ?
    """, (usuario_id,))

    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return resultado

    return (0, 0, 0)

#=====================================================
# Salvar progresso do quiz
#=====================================================

def salvar_progresso_quiz(
    usuario_id,
    questao_atual,
    acertos,
    erros
):

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE usuarios
    SET
        quiz_questao_atual = ?,
        quiz_acertos = ?,
        quiz_erros = ?
    WHERE id = ?
    """,
    (
        questao_atual,
        acertos,
        erros,
        usuario_id
    ))

    conn.commit()
    conn.close()


# =====================================================
# 🔥 SISTEMA DE MOEDAS
# =====================================================

def obter_moedas(usuario_id):
    """Retorna o saldo de moedas atual do usuário."""
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT moedas FROM usuarios WHERE id = ?", (usuario_id,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado and resultado[0] is not None else 0


def registrar_acerto_global(usuario_id):
    """Chamada toda vez que o jogador acerta uma pergunta (não reseta nunca)."""
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuarios
        SET acertos_globais = COALESCE(acertos_globais, 0) + 1
        WHERE id = ?
    """, (usuario_id,))
    conn.commit()
    conn.close()


def registrar_atividade_concluida(usuario_id):
    """Chamada quando o jogador termina uma rodada completa de perguntas."""
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuarios
        SET atividades_concluidas = COALESCE(atividades_concluidas, 0) + 1
        WHERE id = ?
    """, (usuario_id,))
    conn.commit()
    conn.close()


def obter_missoes(usuario_id):
    """
    Monta a lista de missões com o progresso atual de cada uma,
    pronta pra tela desenhar (progresso, se está concluída,
    se já foi resgatada e se pode resgatar agora).
    """
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COALESCE(atividades_concluidas, 0),
            COALESCE(acertos_globais, 0),
            COALESCE(level, 1)
        FROM usuarios WHERE id = ?
    """, (usuario_id,))
    linha = cursor.fetchone()
    atividades, acertos, level = linha if linha else (0, 0, 1)

    cursor.execute("""
        SELECT missao_chave FROM progresso_missoes
        WHERE usuario_id = ? AND resgatada = 1
    """, (usuario_id,))
    ja_resgatadas = {linha[0] for linha in cursor.fetchall()}
    conn.close()

    valores_atuais = {
        "atividades_concluidas": atividades,
        "acertos_globais":       acertos,
        "nivel_interno":         max(level - 1, 0),  # quantas vezes já subiu
    }

    missoes = []
    for missao in MISSOES:
        progresso_bruto = valores_atuais.get(missao["campo"], 0)
        progresso = min(progresso_bruto, missao["meta"])
        concluida = progresso >= missao["meta"]
        resgatada = missao["chave"] in ja_resgatadas

        missoes.append({
            **missao,
            "progresso":     progresso,
            "concluida":     concluida,
            "resgatada":     resgatada,
            "pode_resgatar": concluida and not resgatada,
        })

    return missoes


def resgatar_missao(usuario_id, missao_chave):
    """
    Efetiva o resgate de uma missão concluída: marca como resgatada
    e credita as moedas de recompensa na conta do usuário.
    Retorna (sucesso, quantidade_de_moedas_ganhas).
    """
    missao = next((m for m in MISSOES if m["chave"] == missao_chave), None)
    if not missao:
        return False, 0

    missoes_atuais = obter_missoes(usuario_id)
    alvo = next((m for m in missoes_atuais if m["chave"] == missao_chave), None)

    if not alvo or not alvo["pode_resgatar"]:
        return False, 0  # ainda não concluiu, ou já resgatou antes

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO progresso_missoes (usuario_id, missao_chave, resgatada)
        VALUES (?, ?, 1)
    """, (usuario_id, missao_chave))

    cursor.execute("""
        UPDATE usuarios
        SET moedas = COALESCE(moedas, 0) + ?
        WHERE id = ?
    """, (missao["recompensa"], usuario_id))

    conn.commit()
    conn.close()

    return True, missao["recompensa"]