# 📁 Carpeta data/

Los archivos CSV **no se versionan** en git (pesan varios MB y se pueden regenerar). Por eso esta carpeta
solo guarda este README en el repo.

## Archivos

| Archivo | Qué es | Cómo se genera |
|---|---|---|
| `cannabis_raw.csv` | Dataset original sin tocar (8.910 × 38) | Copiado del caché de Hugging Face |
| `cannabis_clean.csv` | Dataset limpio y enriquecido | Lo genera el notebook `02_limpieza_features.ipynb` |

## Cómo obtener `cannabis_raw.csv`

El dataset original es [`JonusNattapong/cannabis-strains`](https://huggingface.co/datasets/JonusNattapong/cannabis-strains).

⚠️ La librería `datasets` de Hugging Face **está rota en Python 3.13**. Opciones:

1. **Más fácil:** descargar el CSV manualmente desde la página del dataset en Hugging Face y guardarlo aquí
   como `cannabis_raw.csv`.
2. Si tienes Python 3.11/3.12:
   ```python
   from datasets import load_dataset
   import pandas as pd
   ds = load_dataset("JonusNattapong/cannabis-strains")
   pd.DataFrame(ds["train"]).to_csv("data/cannabis_raw.csv", index=False)
   ```

La descripción de cada columna está en [`../docs/DICCIONARIO_DATOS.md`](../docs/DICCIONARIO_DATOS.md).
