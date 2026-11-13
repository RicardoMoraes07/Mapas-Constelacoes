#Sistema de coordenadas antigo
import os
import glob
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def dms_to_deg(g, m, s):
    return g + m / 60 + s / 3600


# ============================================================
# Procura automaticamente todos os arquivos .txt da pasta
# ============================================================

pasta = os.path.dirname(os.path.abspath(__file__))

arquivos = glob.glob(os.path.join(pasta, "*.txt"))

# Ordena os arquivos pelo nome
arquivos.sort()


# ============================================================
# Processa cada arquivo
# ============================================================

for arquivo in arquivos:

    print(f"Processando: {os.path.basename(arquivo)}")

    dados = []

    # Lê o arquivo
    with open(arquivo, "r", encoding="utf-8") as f:

        # Ignora a primeira linha (cabeçalho)
        next(f)

        for linha in f:

            partes = linha.split()

            if len(partes) < 8:
                continue

            estrela = partes[0]
            data = partes[1]

            az_g = float(partes[2])
            az_m = float(partes[3])
            az_s = float(partes[4])

            alt_g = float(partes[5])
            alt_m = float(partes[6])
            alt_s = float(partes[7])

            az = dms_to_deg(az_g, az_m, az_s)
            alt = dms_to_deg(alt_g, alt_m, alt_s)

            dados.append({
                "Estrela": estrela,
                "Data": data,
                "Azimute": az,
                "Altitude": alt
            })


    # Cria DataFrame
    df = pd.DataFrame(dados)

    if df.empty:
        print("  Arquivo vazio ou sem dados válidos.")
        continue


    # ========================================================
    # Data da observação
    # ========================================================

    data = df["Data"].iloc[0]


    # ========================================================
    # Cria o gráfico
    # ========================================================

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})

    az = np.deg2rad(df["Azimute"])
    alt = df["Altitude"]


    # Estrelas
    ax.scatter(
        az,
        alt,
        s=100,
        c="yellow",
        edgecolors="black"
    )


    # ========================================================
    # Configuração do céu
    # ========================================================

    # Sul no topo
    ax.set_theta_zero_location("S")

    # Sentido horário
    ax.set_theta_direction(-1)

    # Altitude: 0° até 90°
    ax.set_rlim(0, 90)


    # Fundo preto
    ax.set_facecolor("black")

    # Grade
    ax.grid(True, color="gray", alpha=0.5)


    # ========================================================
    # Data
    # ========================================================

    ax.set_title(
        f"Data: {data}",
        color="black",
        fontsize=14,
        pad=20
    )


    # ========================================================
    # Salva a imagem com o mesmo nome do arquivo .txt
    # ========================================================

    nome_saida = os.path.splitext(arquivo)[0] + ".png"

    plt.savefig(
        nome_saida,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"  Imagem salva: {os.path.basename(nome_saida)}")


print("\nProcessamento concluído.")