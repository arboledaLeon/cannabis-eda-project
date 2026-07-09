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

## [2026-07-09] Loop 1 — Notebooks de carga y exploración
**Contexto:** Necesitábamos entender los datos antes de limpiarlos.
**Decisión:** Crear `00_carga_inicial` (carga + primer vistazo) y `01_exploracion` (radiografía). Ejecutados
con outputs incrustados para que GitHub los muestre completos.
**Por qué:** Documentamos el hallazgo clave: el "0% de nulos" es engañoso — la basura está escondida en
columnas constantes (`sale_item`, `most_popular_seeds`), plantilladas (`experience`), números como texto
(`thc`='21.8%') y multi-etiqueta (`effect`='Relaxed, Energetic'). Esto le da un plan concreto a la limpieza.
**Alternativas descartadas:** Saltar directo a limpiar (limpieza a ciegas, sin justificación).

## [2026-07-09] Loop 2 — Limpieza y features
**Contexto:** La exploración dejó un plan claro de 5 problemas a resolver.
**Decisiones:**
- THC/CBD/rendimientos/alturas/floración: texto → número (`pct_to_float`, `extract_number`), con sufijos
  `_pct`/`_num`/`_days` para distinguir las columnas numéricas de las originales.
- `indica_sativa` (15 variantes) → `type_simple` con 3 categorías (Indica 5507, Sativa 2100, Híbrido 1303).
  Regla: si menciona ambas o "50%" → Híbrido (salvo que un "dominant" desempate).
- `type_ratio` → `indica_pct` / `sativa_pct` numéricos.
- Features nuevas: `num_effects`, `num_flavors`, `num_medical`, `savings_gbp`.
- Eliminadas columnas basura (`NOISE_COLS`).
- Resultado guardado en `data/cannabis_clean.csv`.
**Por qué:** Separar "preparar datos" de "analizar". A partir del 03 se carga `clean(load_raw())` en una línea.
**Hallazgo a vigilar:** el efecto `Relaxing` domina de forma sospechosa (~7000/8910) → posible valor por
defecto del scraper. Investigar en el 03 antes de sacar conclusiones sobre efectos.

<!-- Próximas entradas: elección de gráficos del EDA narrado, análisis de precio, etc. -->
