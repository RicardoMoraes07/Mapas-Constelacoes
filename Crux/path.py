
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def dms_to_deg(g, m, s):
    return g + m / 60 + s / 3600


# ============================================================
# ARQUIVOS SELECIONADOS
# Formato dos nomes: MM-DD-AA.txt
# ============================================================

pasta = os.path.dirname(os.path.abspath(__file__))

nomes_arquivos = [
    "06-01-26.txt",  # 01/06/26
    "07-01-26.txt",  # 01/07/26
    "08-03-26.txt",  # 03/08/26
    "08-30-26.txt"   # 30/08/26
]

dados = []

# ============================================================
# LÊ OS QUATRO ARQUIVOS
# ============================================================

for nome_arquivo in nomes_arquivos:

    arquivo = os.path.join(pasta, nome_arquivo)

    if not os.path.isfile(arquivo):
        print(f"Arquivo não encontrado: {nome_arquivo}")
        continue

    # Converte a data do nome para DD/MM/AA
    data = pd.to_datetime(
        nome_arquivo.replace(".txt", ""),
        format="%m-%d-%y"
    )

    data_legenda = data.strftime("%d/%m/%y")

    print(f"Lendo: {nome_arquivo} ({data_legenda})")

    with open(arquivo, "r", encoding="utf-8") as f:

        # Ignora o cabeçalho
        next(f, None)

        for linha in f:

            partes = linha.split()

            if len(partes) < 8:
                continue

            try:
                estrela = partes[0]

                az = dms_to_deg(
                    float(partes[2]),
                    float(partes[3]),
                    float(partes[4])
                )

                alt = dms_to_deg(
                    float(partes[5]),
                    float(partes[6]),
                    float(partes[7])
                )

                dados.append({
                    "Estrela": estrela,
                    "Data": data_legenda,
                    "Azimute": az,
                    "Altitude": alt
                })

            except ValueError:
                continue


# ============================================================
# VERIFICA SE EXISTEM DADOS
# ============================================================

df = pd.DataFrame(dados)

if df.empty:
    raise ValueError(
        "Nenhum dado foi encontrado nos arquivos selecionados."
    )


# ============================================================
# CRIA O GRÁFICO ALT-AZ
# ============================================================

fig, ax = plt.subplots(
    figsize=(9, 9),
    subplot_kw={"projection": "polar"}
)


# ============================================================
# PLOTA AS ESTRELAS POR DATA
# ============================================================

cores = {
    "01/06/26": "yellow",
    "01/07/26": "cyan",
    "03/08/26": "lime",
    "30/08/26": "magenta"
}

for data, cor in cores.items():

    grupo = df[df["Data"] == data]

    if grupo.empty:
        continue

    az = np.deg2rad(grupo["Azimute"].to_numpy())
    alt = grupo["Altitude"].to_numpy()

    visivel = (alt >= 0) & (alt <= 90)

    ax.scatter(
        az[visivel],
        alt[visivel],
        s=25,
        c=cor,
        edgecolors="black",
        linewidths=0.4,
        label=data,
        zorder=5
    )


# ============================================================
# POLO SUL CELESTE (PSC)
# ============================================================

# Latitude de Nova Venécia: 18°42'49" S
latitude = dms_to_deg(18, 42, 49)

ax.scatter(
    np.deg2rad(180),
    latitude,
    s=120,
    c="red",
    marker="x",
    linewidths=2.5,
    zorder=10
)

ax.annotate(
    "PSC",
    (np.deg2rad(180), latitude),
    xytext=(8, 8),
    textcoords="offset points",
    color="red",
    fontsize=11,
    fontweight="bold"
)


# ============================================================
# SISTEMA DE COORDENADAS ALT-AZ
# ============================================================

ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)


# ============================================================
# ALTITUDE
# ============================================================

ax.set_rlim(90, 0)
ax.set_yticks(np.arange(0, 91, 10))
ax.set_yticklabels([])


# ============================================================
# AZIMUTE
# ============================================================

ax.set_xticks(
    np.deg2rad([
        0, 45, 90, 135,
        180, 225, 270, 315
    ])
)

ax.set_xticklabels([
    "N", "NE", "L", "SE",
    "S", "SO", "O", "NO"
])


# ============================================================
# APARÊNCIA
# ============================================================

ax.set_facecolor("black")

ax.grid(
    True,
    color="gray",
    alpha=0.5,
    linestyle="-"
)

ax.tick_params(axis="x", colors="black", labelsize=12)
ax.tick_params(axis="y", colors="white", labelsize=9)

for spine in ax.spines.values():
    spine.set_color("black")


# ============================================================
# TÍTULO E LEGENDA
# ============================================================

ax.set_title(
    "Posições das estrelas no céu de Nova Venécia",
    color="black",
    fontsize=14,
    pad=20
)

ax.legend(
    title="Data (DD/MM/AA)",
    loc="upper left",
    bbox_to_anchor=(1.08, 1.0),
    frameon=False,
    labelcolor="black",
    title_fontsize=10
)


# ============================================================
# SALVA A IMAGEM
# ============================================================

nome_saida = os.path.join(
    pasta,
    "estrelas_quatro_datas.png"
)

plt.savefig(
    nome_saida,
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

plt.close()

print(f"\nTotal de registros: {len(df)}")
print(f"Imagem salva: {nome_saida}")
print("Processamento concluído.")
