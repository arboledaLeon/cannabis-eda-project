# 🌿 Cannabis Strains — Análisis Exploratorio de Datos (EDA)

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Estado](https://img.shields.io/badge/Estado-En%20progreso-yellow.svg)
![Idioma](https://img.shields.io/badge/An%C3%A1lisis-Espa%C3%B1ol-green.svg)

> Análisis exploratorio de **8.910 cepas de cannabis** desde una doble perspectiva:
> **químico-medicinal** (THC, CBD, efectos, usos terapéuticos) y **de mercado** (precios, descuentos, breeders).

Proyecto de portafolio en ciencia de datos. Autor: **León** — Ingeniería Biomédica.

## 📊 El dataset

- **Fuente:** [Cannabis Strains — Hugging Face](https://huggingface.co/datasets/JonusNattapong/cannabis-strains)
- **Tamaño:** 8.910 cepas × 38 columnas (scrape de una tienda de semillas; precios en £ GBP).
- **Documentación completa de columnas:** [`docs/DICCIONARIO_DATOS.md`](docs/DICCIONARIO_DATOS.md)

## 🎯 Preguntas que responde el análisis

- ¿Cómo se distribuyen el THC y el CBD? ¿Qué tan potentes son las cepas típicas?
- ¿Qué efectos y usos medicinales son más comunes?
- ¿Se diferencian Indica, Sativa e Híbrido en su química?
- ¿Qué determina el **precio** de una cepa? ¿La potencia, el breeder, otra cosa?

## 🗂️ Estructura del proyecto

```
├── data/            # Datos (CSV, no versionados). Ver data/README.md
├── notebooks/       # 00_carga → 01_exploracion → 02_limpieza → 03_eda_narrado
├── src/             # Código reutilizable (carga, limpieza, estilo de gráficos)
├── images/          # Gráficos exportados
├── docs/            # Diccionario de datos, flujo de trabajo, bitácora de decisiones
└── CLAUDE.md        # Contexto del proyecto
```

## 🛠️ Tecnologías

Python · pandas · NumPy · Matplotlib · Seaborn · WordCloud

## 🚀 Cómo reproducirlo

```bash
pip install -r requirements.txt
# El dataset ya está en data/cannabis_raw.csv. Abre los notebooks en orden (00 → 03).
```

## 📈 Resultados

_En construcción — se irán agregando los hallazgos y gráficos al avanzar el análisis._

---
<sub>Análisis y documentación en español; código en inglés (estándar profesional).</sub>
