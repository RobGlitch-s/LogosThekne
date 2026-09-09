from groq import Groq
import json
import random

client = Groq(
    api_key="Insira aqui sua Api Key da Groq"
)

PROMPT = """
Você é um professor técnico de informática.

Crie uma pergunta de múltipla escolha.

Responda SOMENTE JSON válido.

Formato obrigatório:

{
    "pergunta": "",
    "opcoes": {
        "A": {
            "texto": "",
            "correta": 0
        },
        "B": {
            "texto": "",
            "correta": 0
        },
        "C": {
            "texto": "",
            "correta": 0
        },
        "D": {
            "texto": "",
            "correta": 0
        }
    },
    "explicacao": ""
}

REGRAS:

- Exatamente 4 alternativas.
- Apenas UMA alternativa deve ter "correta": 1.
- A alternativa correta deve ser escolhida ALEATORIAMENTE entre A, B, C ou D — não use sempre a mesma letra.
- Varie bastante qual letra é a correta a cada pergunta.
- O campo "explicacao" deve conter de 1 a 2 frases curtas, em português, explicando
  de forma simples por que a alternativa correta está certa (e, se ajudar, por que
  as outras estão erradas). Escreva como se estivesse explicando para um aluno.
- Apenas JSON.
- Sem markdown.
- Sem texto fora do JSON.
"""


def gerar_pergunta(materia, idioma="pt"):
    try:
        # passa uma letra aleatória no prompt para forçar variação
        letra_sugerida = random.choice(["A", "B", "C", "D"])

        instrucao_idioma = (
            "Responda em português do Brasil."
            if idioma == "pt" else
            "Answer in English."
        )

        resposta = client.chat.completions.create(
            model="groq/compound",
            messages=[
                {
                    "role": "system",
                    "content": PROMPT
                },
                {
                    "role": "user",
                    "content": (
                        f"Crie uma pergunta sobre {materia}. "
                        f"Desta vez, a resposta correta deve ser a alternativa {letra_sugerida}. "
                        f"{instrucao_idioma}"
                    )
                }
            ],
            temperature=0.9
        )

        texto = resposta.choices[0].message.content.strip()

        if texto.startswith("```json"):
            texto = texto.replace("```json", "").replace("```", "")

        texto = texto.strip()

        dados = json.loads(texto)

        # validação extra: se a IA ignorou e colocou tudo errado,
        # verifica se tem exatamente 1 correta
        corretas = sum(
            1 for letra in ["A", "B", "C", "D"]
            if dados["opcoes"][letra]["correta"] == 1
        )

        if corretas != 1:
            print(f"IA retornou {corretas} respostas corretas — descartando e tentando novamente")
            return gerar_pergunta(materia, idioma)

        # garante que o campo sempre exista, mesmo se a IA esquecer
        if "explicacao" not in dados or not dados["explicacao"]:
            letra_correta = obter_resposta_correta(dados)
            texto_correta = dados["opcoes"][letra_correta]["texto"]
            if idioma == "pt":
                dados["explicacao"] = f"A alternativa correta é a {letra_correta}: {texto_correta}."
            else:
                dados["explicacao"] = f"The correct answer is {letra_correta}: {texto_correta}."

        return dados

    except Exception as erro:
        print(f"Erro Groq: {erro}")
        return None


PROMPT_LICAO = """
Você é um professor técnico de informática que cria aulas curtas e didáticas
para um curso dentro de um aplicativo de estudos.

Responda SOMENTE JSON válido, sem markdown, sem texto fora do JSON.

Formato obrigatório:

{
    "titulo": "",
    "conteudo": "",
    "exemplo": "",
    "dica": ""
}

REGRAS:

- "titulo": nome curto e chamativo do tópico da aula (máx. 8 palavras).
- "conteudo": explicação didática do tópico, em português, entre 2 e 4 parágrafos
  curtos (separados por \\n\\n), adequada ao nível pedido. Use uma linguagem clara,
  com analogias quando ajudar a entender.
- "exemplo": um exemplo prático e concreto do conteúdo explicado (pode ser um
  trecho de código, uma situação do dia a dia, ou um cenário real). Curto e direto.
- "dica": uma dica prática de 1 frase para o aluno fixar o conteúdo ou ir além.
- Escolha um tópico ALEATÓRIO e específico dentro da matéria e nível pedidos
  (não repita sempre o tópico mais óbvio) — varie bastante a cada chamada.
- Apenas JSON.
"""


def gerar_licao(materia, nivel, idioma="pt"):
    """Gera o conteúdo de uma aula (curso) para uma matéria e nível específicos."""
    try:
        instrucao_idioma = (
            "Responda em português do Brasil."
            if idioma == "pt" else
            "Answer in English."
        )

        resposta = client.chat.completions.create(
            model="groq/compound",
            messages=[
                {
                    "role": "system",
                    "content": PROMPT_LICAO
                },
                {
                    "role": "user",
                    "content": (
                        f"Crie uma aula sobre {materia}, nível {nivel}. "
                        f"Escolha um tópico específico e interessante dentro desse tema. "
                        f"{instrucao_idioma}"
                    )
                }
            ],
            temperature=1.0
        )

        texto = resposta.choices[0].message.content.strip()

        if texto.startswith("```json"):
            texto = texto.replace("```json", "").replace("```", "")
        elif texto.startswith("```"):
            texto = texto.replace("```", "")

        texto = texto.strip()

        dados = json.loads(texto)

        for campo in ("titulo", "conteudo", "exemplo", "dica"):
            dados.setdefault(campo, "")

        return dados

    except Exception as erro:
        print(f"Erro Groq (gerar_licao): {erro}")
        return None


def obter_resposta_correta(dados):
    for letra in ["A", "B", "C", "D"]:
        if dados["opcoes"][letra]["correta"] == 1:
            return letra
    return None


def verificar_resposta(dados, resposta_usuario):
    correta = obter_resposta_correta(dados)
    return resposta_usuario.upper() == correta