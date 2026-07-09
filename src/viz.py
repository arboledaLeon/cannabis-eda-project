"""Estilo y colores para que todos los gráficos del proyecto se vean iguales y profesionales.

La idea: llamar a set_style() una vez al inicio del notebook, y usar los colores de PALETTE
para que todo tenga una identidad visual coherente (tema verde, apropiado al tema).

Regla del proyecto: nombres en INGLÉS, comentarios en ESPAÑOL.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parents[1]
IMAGES_DIR = PROJECT_ROOT / "images"

# Paleta del proyecto (tonos verdes + acentos). Úsala así: color=PALETTE["green"]
PALETTE = {
    "green": "#2e7d32",       # verde principal
    "light_green": "#81c784",  # verde claro
    "purple": "#6a1b9a",      # para THC (psicoactivo)
    "teal": "#00838f",        # para CBD
    "orange": "#ef6c00",      # acento / alertas
    "gray": "#616161",        # texto secundario
}

# Colores fijos por tipo de cepa, para que Indica/Sativa/Híbrido siempre tengan el mismo color.
TYPE_COLORS = {
    "Indica": "#6a1b9a",
    "Sativa": "#ef6c00",
    "Híbrido": "#2e7d32",
    "Desconocido": "#9e9e9e",
}


def set_style():
    """Configura el estilo global de los gráficos. Llamar una vez al inicio del notebook."""
    sns.set_theme(style="whitegrid")          # fondo blanco con rejilla suave
    plt.rcParams["figure.figsize"] = (10, 6)   # tamaño por defecto de las figuras
    plt.rcParams["axes.titlesize"] = 15        # tamaño del título
    plt.rcParams["axes.titleweight"] = "bold"
    plt.rcParams["axes.labelsize"] = 12        # tamaño de las etiquetas de los ejes
    plt.rcParams["font.size"] = 11


def save_fig(name, dpi=200):
    """Guarda la figura actual en la carpeta images/ con buen tamaño.

    Ejemplo: save_fig("01_distribucion_thc")  ->  images/01_distribucion_thc.png
    """
    IMAGES_DIR.mkdir(exist_ok=True)
    output_path = IMAGES_DIR / f"{name}.png"
    plt.savefig(output_path, dpi=dpi, bbox_inches="tight")
    print(f"Gráfico guardado en {output_path}")
