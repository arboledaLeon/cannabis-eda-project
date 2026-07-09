# 🔁 Flujo de trabajo — El "Ciclo EDA" en loops

Este documento define **cómo trabajamos** León + Claude en este proyecto. La idea es avanzar de forma
continua, aprender haciendo y dejar el repo siempre presentable.

## El Ciclo EDA (un loop)

Cada loop responde una **pregunta o un bloque temático**, no "hace un gráfico". El ciclo es:

```
   ┌─────────────────────────────────────────────────────────┐
   │  1. PREGUNTA   ¿Qué queremos saber? (hipótesis explícita) │
   │  2. EXPLORA    Mirar los datos crudos relevantes          │
   │  3. LIMPIA     Solo lo necesario para responder           │
   │  4. VISUALIZA  El gráfico correcto para la pregunta        │
   │  5. INTERPRETA Escribir en español qué significa           │
   │  6. CIERRA     Commit (avisar; push solo con OK de León)    │
   └─────────────────────────────────────────────────────────┘
```

> Un buen analista no se distingue por hacer gráficos, sino por **la pregunta que hace y la interpretación
> que escribe**. Por eso los pasos 1 y 5 son los más importantes.

## Tamaño de loop: MEDIANO (B)

Acordado con León. En cada loop, Claude avanza **3-4 preguntas relacionadas de corrido** (un bloque temático
completo) sin frenar a pedir aprobación en cada paso. Ejemplos de bloques:

- Bloque "Perfil químico": distribución de THC, distribución de CBD, relación THC↔CBD, potencia por tipo.
- Bloque "Efectos y sabores": top efectos, top sabores, co-ocurrencia efecto↔sabor.
- Bloque "Mercado": distribución de precios, precio por breeder, ¿qué explica el precio?, descuentos.

Cada bloque cierra con un **commit** y una tanda de tareas para León.

## Reparto de trabajo

- **Claude** escribe TODO en el notebook: la teoría del concepto, el análisis completo (código + gráfico +
  interpretación en español) y cualquier exploración adicional que valga la pena. El notebook queda
  **autocontenido y didáctico**.
- **León aprende leyendo** el notebook. Decidió (2026-07-09) **no** usar secciones de ejercicios
  "🎯 Tu turno": todos los detalles se incluyen ya resueltos y explicados dentro del EDA.

## Secuencia de notebooks

| Notebook | Objetivo |
|---|---|
| `00_carga_inicial.ipynb`   | Cargar el CSV, primer vistazo, guardar copia local |
| `01_exploracion.ipynb`     | Conocer columnas, tipos, "nulos" reales, constantes |
| `02_limpieza_features.ipynb` | Parsear números, explotar multi-etiquetas, features nuevas → `cannabis_clean.csv` |
| `03_eda_narrado.ipynb`     | ⭐ El notebook estrella: teoría + análisis + narrativa (química-medicinal + mercado) |

## Reglas de Git (recordatorio)

- Claude **prepara** el commit y **avisa**; León confirma el `push`. Nunca push automático.
- Un commit por loop. Mensajes en español, descriptivos:
  `análisis: relación THC–precio` · `limpieza: parseo de THC/CBD a numérico` · `docs: diccionario de datos`.

## Entregable visual final

1. **A (automático):** GitHub renderiza los `.ipynb` con gráficos → ya es navegable en el repo.
2. **B (intermedio):** un reporte HTML limpio (Artifact) con resumen + gráficos estrella + conclusiones.
3. **C (meta final, elegido por León):** publicar ese reporte en **GitHub Pages**
   (`arboledaleon.github.io/cannabis-eda-project`) como link público de portafolio.

## Ritmo (método de León)

León trabaja con Pomodoro 25/10 + hiperfoco flexible. Un bloque temático ≈ 2-3 Pomodoros. El "🎯 Tu turno"
está pensado para caber en 1-2 Pomodoros de práctica activa.
