# 🗂️ Bitácora de decisiones

Registro de **por qué** hicimos cada cosa. Un reclutador (y tu yo del futuro) valoran ver el razonamiento,
no solo el resultado. Una entrada por decisión importante.

Formato:
```
## [AAAA-MM-DD] Título de la decisión
**Contexto:** qué observamos.
**Decisión:** qué elegimos hacer.
**Por qué:** la justificación.
**Alternativas descartadas:** qué más consideramos y por qué no.
```

---

## [2026-07-09] Fundación del proyecto y andamiaje
**Contexto:** El proyecto estaba abandonado tras 1 commit: README vacío, notebook con typo (`caraga`),
carpetas vacías, `.venv` como ruido. La guía PDF original asumía un dataset distinto (columnas
`Type/Effects/Flavor/THC/CBD`) que **no coincide** con el dataset real (38 columnas de tienda de semillas).
**Decisión:** Rehacer el andamiaje: `CLAUDE.md`, `docs/`, `src/`, memoria agéntica, `requirements.txt`,
diccionario de datos real, y trabajar en loops medianos. EDA en español, código en inglés.
**Por qué:** El plan viejo habría fallado al primer `df['Type']`. Mejor construir sobre la realidad del
dataset, que además es más rico (permite análisis de mercado + medicinal, no solo química básica).
**Alternativas descartadas:** Seguir el PDF al pie de la letra (rompe); un solo notebook gigante (menos
mantenible que la secuencia 00→03).

## [2026-07-09] Cargar desde CSV local, no desde `datasets`
**Contexto:** `from datasets import load_dataset` **falla en Python 3.13** (`ModuleNotFoundError: cgi`).
**Decisión:** Materializar el dataset en `data/cannabis_raw.csv` y cargar con `pandas`.
**Por qué:** Reproducible, estable y no depende de una librería rota. El CSV se ignora en git (pesa 11 MB).
**Alternativas descartadas:** Forzar `datasets` (rota); fijar Python 3.11 solo para cargar (fricción innecesaria).

<!-- Próximas entradas: decisiones de limpieza (parseo THC, consolidación de tipos), elección de gráficos, etc. -->
