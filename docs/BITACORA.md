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

## [2026-07-09] Loop 3 — EDA narrado, Parte 1 (perfil químico) + hallazgo de calidad de datos
**Contexto:** Primeros gráficos (histogramas THC/CBD, boxplot por tipo, scatter THC-CBD). Al *mirar* los
gráficos (no solo ejecutarlos) detectamos anomalías graves.
**Hallazgos de calidad de datos (críticos):**
- **THC:** 69% (6.151) vale exactamente 20,0% → valor por defecto del scraper. Hay THC = −20% (imposible).
  15% son texto (`High`, `Very High`) → NaN. Solo ~16% (1.415) tiene THC numérico creíble.
- **CBD:** 84% dice la palabra `Low`; solo ~10% (878) tiene valor numérico. Los numéricos confirman: CBD bajo,
  sesgo positivo (media 1,81 > mediana 1,00). Etiqueta y número coinciden.
- **THC real por tipo:** Indica 21,7 > Híbrido 21,0 > Sativa 19,4 (tendencia leve, cajas se solapan).
- **THC vs CBD:** r = −0,69 (moderada, negativa), estable al quitar el default; n = 701 pares numéricos.
**Decisiones:**
- Analizar THC solo sobre el subconjunto real (`thc_pct != 20` y en 0–100%).
- Dejar el histograma THC "feo" a propósito: es el disparador didáctico de la investigación.
- Paleta de `TYPE_COLORS` revalidada para daltonismo (morado Indica → #9c4dcc para pasar la banda de luminosidad).
**Lección destacada en el notebook:** detectar datos imputados/por-defecto ANTES de sacar promedios.
Correlación ≠ causalidad.
**Corrección honesta:** las primeras interpretaciones (escritas antes de ver los datos) decían "cepa típica
~20% THC, distribución simétrica" y "correlación débil" — ambas FALSAS. Se reescribieron tras investigar.

## [2026-07-09] Loop 4 — EDA narrado, Parte 2 (efectos y usos medicinales)
**Contexto:** Analizar `effect` y `medical_strains` (multi-etiqueta). Confirmamos el sospechoso `Relaxing`.
**Hallazgos:**
- `effect` == 'Relaxing' en 76% (default, igual que THC=20). Tras excluirlo, efectos reales variados:
  energizantes (Euphoric, Creative, Energetic, Focused) vs. sedantes (Sleepy, Relaxed, Calming).
- `medical_strains` == 'Relaxing' en 52% (default). Condiciones clínicas reales top: General Pain (810),
  Stress Relief (686), Insomnia (621), Anxiety (521), Depression (391). Coherente con la evidencia.
- **Meta-hallazgo transversal:** el valor por defecto afecta al 52–87% de cada columna clave
  (flavor='Citrus' 87%, CBD='Low' 84%, effect='Relaxing' 76%, THC=20% 69%, medical='Relaxing' 52%).
  Es la firma del scraper. Gráfico 07 lo resume.
**Decisión:** para efectos/medicinal, excluir las filas que solo traen el default antes de explotar y contar.
**Gráficos nuevos:** 05_top_efectos, 06_usos_medicinales, 07_valores_por_defecto.

## [2026-07-09] Loop 5 — EDA narrado, Parte 3 (mercado) + conclusiones generales
**Contexto:** Cerrar el análisis con el ángulo comercial.
**Hallazgos:**
- Precio muy sesgado a la derecha: mediana £19, media £82, máx £999. Se usa la mediana como medida honesta.
- Descuento casi constante: 97% de las cepas al 40% → estrategia comercial permanente, no ofertas reales.
- La química **no** explica el precio: corr precio-THC(real) ≈ −0,18, precio-CBD ≈ 0,24, precio-nº efectos ≈ 0.
- El **breeder sí** manda: precio medio de £11 (Victory Seeds) a £436 (Night Owl Seeds), ~40× de diferencia.
**Conclusión global del EDA:** catálogo comercial de semillas de alta potencia y bajo CBD, con datos muy
imputados (52–87% por defecto), donde el precio responde al prestigio de la marca, no a la química declarada.
**Gráficos:** 08_distribucion_precio, 09_correlaciones_precio, 10_precio_por_breeder.
**Estado:** `03_eda_narrado` COMPLETO (Partes 1-3 + conclusiones, 10 gráficos). Pendiente: reporte GitHub Pages.

<!-- Próxima entrada: reporte final para GitHub Pages. -->
