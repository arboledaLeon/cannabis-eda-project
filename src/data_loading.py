"""Carga y limpieza del dataset Cannabis Strains.

La idea de este archivo: guardar aquí las funciones de limpieza para que los notebooks
queden cortos y fáciles de leer. Cada función hace UNA cosa y está explicada paso a paso.

Regla del proyecto: los nombres (funciones, variables, columnas) van en INGLÉS;
los comentarios y explicaciones van en ESPAÑOL.

Cómo usarlo en un notebook:
    import sys
    sys.path.append("..")            # para que Python vea la carpeta src/
    from src.data_loading import load_raw, clean
    df = clean(load_raw())
"""

import re
from pathlib import Path

import pandas as pd

# --- Rutas del proyecto ---
# __file__ es este archivo. .parents[1] sube una carpeta (de src/ a la raíz del repo).
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_ROOT / "data" / "cannabis_raw.csv"
CLEAN_PATH = PROJECT_ROOT / "data" / "cannabis_clean.csv"

# Columnas que no aportan nada (un solo valor o texto plantillado).
# Las quitamos al limpiar. El detalle del porqué está en docs/DICCIONARIO_DATOS.md
NOISE_COLS = [
    "sale_item",
    "most_popular_seeds",
    "experience",
    "growth_and_harvest",
    "stock_availability",
]


def load_raw(path=RAW_PATH):
    """Lee el CSV crudo y devuelve un DataFrame.

    Cargamos desde el archivo local (no desde la librería `datasets`, que está rota
    en Python 3.13). Si el archivo no está, avisamos con un mensaje claro.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"No encontré {path}. Copia cannabis_raw.csv en la carpeta data/."
        )
    return pd.read_csv(path, encoding="utf-8")


def pct_to_float(series):
    """Convierte texto de porcentaje a número. Ejemplo: '21.8%' -> 21.8

    Paso a paso:
      1. Nos aseguramos de que sea texto (astype str).
      2. Quitamos el símbolo '%'.
      3. Convertimos a número; lo que no se pueda convertir queda como NaN.
    """
    text = series.astype(str)
    text = text.str.replace("%", "", regex=False)
    return pd.to_numeric(text, errors="coerce")


def extract_number(series):
    """Saca el primer número de un texto que trae unidades.

    Ejemplos: '406.0g/m²' -> 406.0   |   '64 days' -> 64.0   |   '166.0cm' -> 166.0

    Usamos una expresión regular sencilla: r"(\\d+\\.?\\d*)"
      \\d+   = uno o más dígitos
      \\.?   = un punto decimal opcional
      \\d*   = cero o más dígitos después del punto
    str.extract nos devuelve ese primer número como texto, y lo pasamos a número.
    """
    number_as_text = series.astype(str).str.extract(r"(\d+\.?\d*)", expand=False)
    return pd.to_numeric(number_as_text, errors="coerce")


def simplify_type(series):
    """Convierte la columna sucia `indica_sativa` en 3 categorías limpias:
    'Indica', 'Sativa' o 'Híbrido'.

    La columna original tiene 15 variantes (ej. 'Indica Dominant', '50% Indica/50% Sativa',
    e incluso mezclas raras). Aquí definimos una regla clara y la aplicamos fila por fila.
    """
    def classify(value):
        text = str(value).lower()
        has_indica = "indica" in text
        has_sativa = "sativa" in text

        # Si dice 50% o menciona ambas, es una mezcla -> Híbrido...
        if "50%" in text or (has_indica and has_sativa):
            # ...salvo que quede claro cuál domina.
            if "indica dominant" in text and "sativa dominant" not in text:
                return "Indica"
            if "sativa dominant" in text and "indica dominant" not in text:
                return "Sativa"
            return "Híbrido"
        if has_indica:
            return "Indica"
        if has_sativa:
            return "Sativa"
        return "Desconocido"

    # .map aplica la función a cada valor de la columna.
    return series.map(classify)


def parse_type_ratio(series):
    """Separa '30% Indica / 70% Sativa' en dos números: 30 y 70.

    Devuelve un DataFrame con dos columnas: indica_pct y sativa_pct.
    Buscamos el número que va justo antes de la palabra 'Indica' y el de 'Sativa'.
    """
    text = series.astype(str)
    # (\\d+) captura los dígitos que están justo antes de la palabra buscada.
    indica_text = text.str.extract(r"(\d+)%\s*Indica", expand=False)
    sativa_text = text.str.extract(r"(\d+)%\s*Sativa", expand=False)

    result = pd.DataFrame(index=series.index)
    result["indica_pct"] = pd.to_numeric(indica_text, errors="coerce")
    result["sativa_pct"] = pd.to_numeric(sativa_text, errors="coerce")
    return result


def explode_multi(df, column):
    """Separa una columna con varias etiquetas por coma en una lista larga.

    Ejemplo: la fila 'Relaxed, Energetic' se convierte en dos filas: 'Relaxed' y 'Energetic'.
    Sirve para contar frecuencias:  explode_multi(df, 'effect').value_counts()

    Paso a paso:
      1. split(',')  -> cada celda pasa a ser una lista: ['Relaxed', ' Energetic']
      2. explode()   -> cada elemento de la lista pasa a su propia fila
      3. str.strip() -> quitamos espacios sobrantes (' Energetic' -> 'Energetic')
    """
    labels = df[column].dropna().astype(str)
    labels = labels.str.split(",").explode()
    labels = labels.str.strip()
    return labels[labels != ""]


def count_labels(text_value):
    """Cuenta cuántas etiquetas hay en un texto separado por comas.

    Ejemplo: 'Sweet, Citrus, Pine' -> 3
    """
    return len(str(text_value).split(","))


def clean(df):
    """Devuelve una copia limpia y enriquecida del DataFrame crudo.

    Qué hace, en orden:
      1. Convierte a número las columnas que venían como texto (THC, CBD, rendimientos, alturas, floración).
      2. Crea un tipo simple (Indica/Sativa/Híbrido) y separa el ratio en números.
      3. Agrega columnas nuevas (cuántos efectos/sabores tiene, cuánto ahorras).
      4. Elimina las columnas basura.
    """
    out = df.copy()

    # 1. Texto -> número
    out["thc_pct"] = pct_to_float(out["thc"])
    out["cbd_pct"] = pct_to_float(out["cbd"])
    out["yield_indoor_num"] = extract_number(out["yield_indoor"])
    out["yield_outdoor_num"] = extract_number(out["yield_outdoor"])
    out["height_indoor_num"] = extract_number(out["height_indoor"])
    out["height_outdoor_num"] = extract_number(out["height_outdoor"])
    out["flowering_days"] = extract_number(out["flowering_time"])

    # 2. Tipo limpio + ratio numérico
    out["type_simple"] = simplify_type(out["indica_sativa"])
    ratio = parse_type_ratio(out["type_ratio"])
    out["indica_pct"] = ratio["indica_pct"]
    out["sativa_pct"] = ratio["sativa_pct"]

    # 3. Columnas nuevas (features)
    out["num_effects"] = out["effect"].apply(count_labels)
    out["num_flavors"] = out["flavor"].apply(count_labels)
    out["num_medical"] = out["medical_strains"].apply(count_labels)
    out["savings_gbp"] = (out["original_price_gbp"] - out["current_price_gbp"]).round(2)

    # 4. Quitar ruido
    cols_to_drop = [c for c in NOISE_COLS if c in out.columns]
    out = out.drop(columns=cols_to_drop)
    return out


# Este bloque solo corre si ejecutas el archivo directamente (python src/data_loading.py).
# Sirve como prueba rápida de que todo funciona.
if __name__ == "__main__":
    raw = load_raw()
    clean_df = clean(raw)
    print("Crudo:", raw.shape, "-> Limpio:", clean_df.shape)
    print("THC promedio: %.1f%%" % clean_df["thc_pct"].mean())
    print("CBD promedio: %.2f%%" % clean_df["cbd_pct"].mean())
    print("Tipos:", clean_df["type_simple"].value_counts().to_dict())
    top_effects = explode_multi(clean_df, "effect").value_counts().head()
    print("Top 5 efectos:", top_effects.to_dict())
