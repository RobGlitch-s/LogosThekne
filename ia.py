import json
import random
import ollama

MODELO = "qwen2.5:7b"   # use "qwen2.5:3b" se tiver pouca RAM
cliente = ollama.Client(host="http://localhost:11434")

SCHEMA_PERGUNTA = {
    "type": "object",
    "properties": {
        "pergunta": {"type": "string"},
        "correta": {"type": "string"},
        "erradas": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 3,
            "maxItems": 3,
        },
        "explicacao": {"type": "string"},
    },
    "required": ["pergunta", "correta", "erradas", "explicacao"],
}

SCHEMA_LICAO = {
    "type": "object",
    "properties": {
        "titulo": {"type": "string"},
        "conteudo": {"type": "string"},
        "exemplo": {"type": "string"},
        "dica": {"type": "string"},
    },
    "required": ["titulo", "conteudo", "exemplo", "dica"],
}

PROMPT = """Você é um professor técnico de informática.
Crie UMA pergunta de múltipla escolha.

REGRAS:
- "pergunta": a pergunta.
- "correta": o texto da única alternativa correta.
- "erradas": exatamente 3 alternativas incorretas, plausíveis, mas claramente erradas.
- "explicacao": 1 a 2 frases curtas explicando por que a correta está certa,
  como se falasse com um aluno.
- Não coloque letras (A, B, C) nas alternativas.
"""

PROMPT_LICAO = """Você é um professor técnico de informática que cria aulas curtas
e didáticas para um curso dentro de um aplicativo de estudos.

REGRAS:
- "titulo": nome curto do tópico (máx. 8 palavras).
- "conteudo": explicação didática em 2 a 4 parágrafos curtos separados por \\n\\n,
  adequada ao nível pedido, com analogias quando ajudar.
- "exemplo": um exemplo prático e concreto, curto e direto.
- "dica": uma dica prática de 1 frase.
- Escolha um tópico específico dentro da matéria (não o mais óbvio).
"""

def _idioma(idioma):
    return "Responda em português do Brasil." if idioma == "pt" else "Answer in English."

def _chamar(system, user, schema, temperatura):
    resposta = cliente.chat(
        model=MODELO,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        format=schema,
        options={"temperature": temperatura},
        keep_alive="15m",   # mantém o modelo na memória entre chamadas
    )
    return json.loads(resposta["message"]["content"])

def gerar_pergunta(materia, idioma="pt", tentativas=3):
    for _ in range(tentativas):
        try:
            bruto = _chamar(
                PROMPT,
                f"Crie uma pergunta sobre {materia}. {_idioma(idioma)}",
                SCHEMA_PERGUNTA,
                temperatura=0.6,
            )

            correta = bruto["correta"].strip()
            erradas = [e.strip() for e in bruto["erradas"]]
            alternativas = [correta] + erradas

            # validações: 4 textos não vazios e sem repetição
            if len(erradas) != 3 or any(not a for a in alternativas):
                continue
            if len({a.lower() for a in alternativas}) != 4:
                continue

            # o Python sorteia a posição da correta
            random.shuffle(alternativas)
            dados = {
                "pergunta": bruto["pergunta"].strip(),
                "opcoes": {
                    letra: {"texto": texto, "correta": 1 if texto == correta else 0}
                    for letra, texto in zip("ABCD", alternativas)
                },
                "explicacao": bruto.get("explicacao", "").strip(),
            }

            if not dados["explicacao"]:
                letra = obter_resposta_correta(dados)
                dados["explicacao"] = (
                    f"A alternativa correta é a {letra}: {correta}."
                    if idioma == "pt"
                    else f"The correct answer is {letra}: {correta}."
                )
            return dados

        except Exception as erro:
            print(f"Erro Ollama (gerar_pergunta): {erro}")

    return None

def gerar_licao(materia, nivel, idioma="pt"):
    """Gera o conteúdo de uma aula para uma matéria e nível específicos."""
    try:
        dados = _chamar(
            PROMPT_LICAO,
            f"Crie uma aula sobre {materia}, nível {nivel}. "
            f"Escolha um tópico específico dentro desse tema. {_idioma(idioma)}",
            SCHEMA_LICAO,
            temperatura=0.8,
        )
        for campo in ("titulo", "conteudo", "exemplo", "dica"):
            dados.setdefault(campo, "")
        return dados
    except Exception as erro:
        print(f"Erro Ollama (gerar_licao): {erro}")
        return None

def obter_resposta_correta(dados):
    for letra in ["A", "B", "C", "D"]:
        if dados["opcoes"][letra]["correta"] == 1:
            return letra
    return None

def verificar_resposta(dados, resposta_usuario):
    correta = obter_resposta_correta(dados)
    return resposta_usuario.upper() == correta