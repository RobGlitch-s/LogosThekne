"""
Módulo responsável pelos efeitos sonoros do quiz (acerto/erro),
no estilo do Duolingo.

Os sons são pequenos "jingles" gerados por código (ondas senoidais),
salvos como .wav dentro de assets/sons/ na primeira execução — assim
o projeto não depende de nenhum arquivo de áudio externo.

A reprodução é feita em uma thread separada para não travar a
interface, e usa apenas bibliotecas padrão do sistema operacional
(sem novas dependências no requirements do projeto):
- Windows -> winsound
- macOS   -> afplay
- Linux   -> paplay/aplay
"""

import math
import shutil
import struct
import subprocess
import sys
import threading
import wave

from utils import BASE_DIR

PASTA_SONS = BASE_DIR / "assets" / "sons"
PASTA_SONS.mkdir(parents=True, exist_ok=True)

CAMINHO_ACERTO = PASTA_SONS / "acerto.wav"
CAMINHO_ERRO   = PASTA_SONS / "erro.wav"

TAXA_AMOSTRAGEM = 44100


def _gerar_amostras(notas, taxa_amostragem=TAXA_AMOSTRAGEM, volume=0.35):
    """
    Gera as amostras (PCM 16 bits) de uma sequência de notas.
    'notas' é uma lista de tuplas (frequencia_hz, duracao_segundos).
    """
    amostras = []

    for frequencia, duracao in notas:
        n_amostras = max(1, int(taxa_amostragem * duracao))
        for i in range(n_amostras):
            t = i / taxa_amostragem
            # fade-out suave no fim de cada nota, pra não "estalar"
            fade = 1.0 - (i / n_amostras) * 0.35
            valor = math.sin(2 * math.pi * frequencia * t) * volume * fade
            amostras.append(int(max(-1.0, min(1.0, valor)) * 32767))

    return amostras


def _salvar_wav(caminho, amostras, taxa_amostragem=TAXA_AMOSTRAGEM):
    with wave.open(str(caminho), "w") as arquivo:
        arquivo.setnchannels(1)
        arquivo.setsampwidth(2)
        arquivo.setframerate(taxa_amostragem)
        dados = struct.pack("<" + "h" * len(amostras), *amostras)
        arquivo.writeframes(dados)


def _garantir_sons():
    """Cria os arquivos de som (uma única vez) caso ainda não existam."""
    try:
        if not CAMINHO_ACERTO.exists():
            # "ding-ding" curto e alegre, subindo de tom (acerto)
            amostras = _gerar_amostras([
                (880.00, 0.09),   # A5
                (1174.66, 0.16),  # D6
            ])
            _salvar_wav(CAMINHO_ACERTO, amostras)

        if not CAMINHO_ERRO.exists():
            # "buzz" curto e grave, descendo de tom (erro)
            amostras = _gerar_amostras([
                (220.00, 0.10),  # A3
                (174.61, 0.18),  # F3
            ], volume=0.30)
            _salvar_wav(CAMINHO_ERRO, amostras)
    except Exception as erro:
        print("Aviso: não foi possível gerar os sons do quiz:", erro)


def _tocar_arquivo(caminho):
    caminho = str(caminho)
    try:
        if sys.platform.startswith("win"):
            import winsound
            winsound.PlaySound(caminho, winsound.SND_FILENAME | winsound.SND_ASYNC)

        elif sys.platform == "darwin":
            subprocess.run(
                ["afplay", caminho], check=False,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )

        else:
            tocador = shutil.which("paplay") or shutil.which("aplay")
            if tocador:
                subprocess.run(
                    [tocador, caminho], check=False,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
    except Exception as erro:
        # se não tiver placa/servidor de áudio disponível, apenas ignora
        print("Aviso: não foi possível tocar o som:", erro)


def tocar_acerto():
    """Toca o som de resposta correta (assíncrono, não trava a interface)."""
    _garantir_sons()
    threading.Thread(target=_tocar_arquivo, args=(CAMINHO_ACERTO,), daemon=True).start()


def tocar_erro():
    """Toca o som de resposta errada (assíncrono, não trava a interface)."""
    _garantir_sons()
    threading.Thread(target=_tocar_arquivo, args=(CAMINHO_ERRO,), daemon=True).start()