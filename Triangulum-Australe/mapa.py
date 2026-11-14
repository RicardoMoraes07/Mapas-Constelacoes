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

    # ========================================================
    # Lê o arquivo
    # ========================================================

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

            # Converte DMS para graus decimais
            az = dms_to_deg(az_g, az_m, az_s)
            alt = dms_to_deg(alt_g, alt_m, alt_s)

            dados.append({
                "Estrela": estrela,
                "Data": data,
                "Azimute": az,
                "Altitude": alt
            })


    # ========================================================
    # Cria DataFrame
    # ========================================================

    df = pd.DataFrame(dados)

    if df.empty:
        print("  Arquivo vazio ou sem dados válidos.")
        continue


    # ========================================================
    # Data da observação
    # ========================================================

    data = df["Data"].iloc[0]


    # ========================================================
    # Cria o gráfico Alt-Az
    # ========================================================

    fig, ax = plt.subplots(
        figsize=(8, 8),
        subplot_kw={"projection": "polar"}
    )


    # ========================================================
    # Coordenadas
    # ========================================================

    az = np.deg2rad(df["Azimute"])
    alt = df["Altitude"]


    # ========================================================
    # Estrelas
    # ========================================================

    ax.scatter(
        az,
        alt,
        s=50,
        c="yellow",
        edgecolors="black",
        zorder=5
    )

 # ========================================================
    # POLO SUL CELESTE (PSC)
    # ========================================================

    # Latitude de Nova Venécia: 18°42'49" S
    latitude = dms_to_deg(18, 42, 49)

    # O PSC está a uma altitude igual ao módulo da latitude
    altitude_psc = latitude

    # O PSC está na direção Sul (azimute = 180°)
    azimute_psc = np.deg2rad(180)

    # Marca a posição do Polo Sul Celeste
    ax.scatter(
        azimute_psc,
        altitude_psc,
        s=120,
        c="red",
        marker="x",
        linewidths=2.5,
        zorder=10
    )

    # Identificação do PSC
    ax.annotate(
        "PSC",
        (azimute_psc, altitude_psc),
        xytext=(8, 8),
        textcoords="offset points",
        color="red",
        fontsize=11,
        fontweight="bold",
        zorder=11
    )
    
    # ========================================================
    # SISTEMA ALT-AZ
    # ========================================================

    # Norte = 0°
    # Leste = 90°
    # Sul = 180°
    # Oeste = 270°

    ax.set_theta_zero_location("N")

    # Sentido horário:
    # N -> L -> S -> O

    ax.set_theta_direction(-1)


    # ========================================================
    # ALTITUDE
    # ========================================================

    # Horizonte = 0°
    # Zênite = 90°

    ax.set_rlim(90, 0)

    # Marcas de altitude a cada 10°
    ax.set_yticks(np.arange(0, 91, 10))

    ax.set_yticklabels([])


    # ========================================================
    # AZIMUTE
    # ========================================================

    ax.set_xticks(
        np.deg2rad([
            0, 45, 90, 135,
            180, 225, 270, 315
        ])
    )

    ax.set_xticklabels([
        "N",
        "NE",
        "L",
        "SE",
        "S",
        "SO",
        "O",
        "NO"
    ])


    # ========================================================
    # APARÊNCIA DO CÉU
    # ========================================================

    # Área circular do céu
    ax.set_facecolor("black")

    # Grade
    ax.grid(
        True,
        color="gray",
        alpha=0.5,
        linestyle="-"
    )


    # ========================================================
    # CORES DAS MARCAÇÕES
    # ========================================================

    ax.tick_params(
        axis="x",
        colors="black",
        labelsize=12
    )

    ax.tick_params(
        axis="y",
        colors="white",
        labelsize=9
    )


    # ========================================================
    # BORDA DO CÉU
    # ========================================================

    for spine in ax.spines.values():
        spine.set_color("black")


    # ========================================================
    # TÍTULO
    # ========================================================

    ax.set_title(
        f"Data: {data}",
        color="black",
        fontsize=14,
        pad=20
    )


    # ========================================================
    # SALVA A IMAGEM
    # ========================================================

    nome_saida = os.path.splitext(arquivo)[0] + ".png"

    plt.savefig(
        nome_saida,
        dpi=300,
        bbox_inches="tight",
        facecolor="white"
    )

    plt.close()

    print(f"  Imagem salva: {os.path.basename(nome_saida)}")


print("\nProcessamento concluído.")
