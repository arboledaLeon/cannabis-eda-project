# CLAUDE.md — Guía del proyecto para el agente

Este archivo le da contexto a Claude Code cada vez que trabajamos aquí. Léelo antes de actuar.

## 🎯 Qué es este proyecto

Análisis Exploratorio de Datos (EDA) del dataset **Cannabis Strains** (`JonusNattapong/cannabis-strains`,
Hugging Face): 8.910 cepas de cannabis scrapeadas de una tienda de semillas (seed-city.com), 38 columnas.

Es una **pieza de portafolio** de León (estudiante de Ingeniería Biomédica, 6º semestre) para freelancing
en ciencia de datos. Objetivo doble: que quede **profesional y vendible**, y que **León aprenda** haciendo.

**Hilo narrativo:** enfoque mixto **químico-medicinal + mercado/precios**. Las tres dimensiones del dataset
(química/efectos · comercial/precios · botánica/cultivo) se tocan, pero la historia la lideran lo medicinal
(gancho, conecta con su carrera) y lo comercial (cierre, conecta con el objetivo freelance).

## 🗣️ Regla de idioma (IMPORTANTE)

- **Prosa, títulos, interpretaciones, comentarios, etiquetas de gráficos, docs → ESPAÑOL.**
- **Código: nombres de variables, funciones, columnas del DataFrame → INGLÉS** (estándar profesional).
- El dataset viene en inglés; sus *valores* (ej. `"Relaxed"`, `"Citrus"`) se mantienen en inglés, pero
  **siempre se traducen/explican en la prosa** que los rodea.

## 📚 Nivel y tono

- Teoría **intermedia pero clara**: cada concepto estadístico se explica al usarlo (IQR, sesgo, correlación,
  media vs mediana…), asumiendo bases de una carrera de ingeniería, pero que **cualquiera lo entienda**.
- Tono cercano y directo, en español. León aprende haciendo; no le des solo resultados, dale el porqué.

## 🔁 Cómo trabajamos: loops medianos (tamaño B)

El ciclo completo está en `docs/WORKFLOW.md`. Resumen operativo:

1. **Un loop = un bloque temático** (3-4 preguntas relacionadas resueltas de corrido, sin frenar a pedir OK).
2. En cada loop Claude: escribe teoría + análisis modelo (código + gráfico + interpretación en español) en
   el notebook, de forma que el notebook quede **completo y presentable**.
3. Al cerrar el bloque, Claude entrega una sección **"🎯 Tu turno en VSCode"**: 2-4 tareas concretas para que
   León extienda ese análisis por su cuenta en el notebook en que estemos.
4. Claude prepara el commit del bloque y **avisa**. León da luz verde para `git push`.

## ⚠️ Reglas de Git

- **Nunca hacer `git push` ni `commit` sin que León lo pida o lo confirme.** Es su repo público
  (`github.com/arboledaLeon/cannabis-eda-project`).
- Commits pequeños, en español, uno por bloque/loop. Historial legible = mejor portafolio.
- Entregable final del reporte visual → **GitHub Pages** (link público de León). Ver `docs/WORKFLOW.md`.

## 🧱 Estructura

```
CLAUDE.md              # este archivo
README.md              # portada del portafolio
requirements.txt       # dependencias fijadas
data/                  # CSVs (ignorados por git; ver data/README.md)
  cannabis_raw.csv     # dataset original materializado
docs/
  WORKFLOW.md          # el Ciclo EDA en loops + método de trabajo
  DICCIONARIO_DATOS.md # las 38 columnas explicadas en español
  BITACORA.md          # log de decisiones analíticas (por qué hicimos cada cosa)
src/
  data_loading.py      # carga + parseo (%THC→float, explode de efectos, etc.)
  viz.py               # estilo y paleta consistente de gráficos
notebooks/             # 00_carga → 01_exploracion → 02_limpieza → 03_eda_narrado
images/                # gráficos exportados (sí se versionan; son el portafolio)
memory/                # memoria agéntica sobre León y el proyecto
```

## 🩺 Realidades técnicas del dataset (no las olvides)

- **`datasets` de HF está rota en Python 3.13** (`ModuleNotFoundError: cgi`). NO la uses.
  Carga siempre desde `data/cannabis_raw.csv` con `pandas` (o usa `src/data_loading.py`).
- El intérprete con las librerías instaladas es el **Python del sistema**
  (`C:/Users/león/AppData/Local/Programs/Python/Python313/python.exe`), NO el `.venv` del repo
  (ese solo tiene pip). pandas/numpy/matplotlib/seaborn/wordcloud están en el del sistema.
- **"0% de nulos" es engañoso.** Hay basura escondida:
  - Columnas constantes (1 solo valor) → inútiles: `sale_item`, `most_popular_seeds`.
  - Columnas plantilladas (texto casi idéntico): `experience`, `growth_and_harvest`.
  - Casi-constantes: `stock_availability` (2 valores).
- Columnas que necesitan parseo a número: `thc`/`cbd` (`"21.8%"`), `yield_indoor`/`yield_outdoor`
  (`"406.0g/m²"`, `"523.0g/plant"`), `height_indoor`/`height_outdoor` (`"166.0cm"`), `flowering_time` (`"64 days"`).
- Columnas multi-etiqueta separadas por comas (usar explode): `effect`, `flavor`, `smell_taste`, `medical_strains`.
- `indica_sativa` está sucio (15 variantes, algunas mezcladas tipo `"Indica Dominant , 50%..."`) → consolidar.
- `type_ratio` (`"30% Indica / 70% Sativa"`) → parsear a `indica_pct` / `sativa_pct` numéricos.
- Todos los precios están en **GBP (£)**.

## ✅ Antes de dar por cerrado un loop

- ¿La prosa está en español y el código en inglés?
- ¿Cada gráfico tiene título, ejes etiquetados y una interpretación escrita debajo?
- ¿Actualizaste `docs/BITACORA.md` con las decisiones tomadas?
- ¿Dejaste la sección "🎯 Tu turno en VSCode"?
- ¿Avisaste a León para el commit (sin pushear por tu cuenta)?
