# 📖 Diccionario de datos — Cannabis Strains

Dataset: `JonusNattapong/cannabis-strains` (Hugging Face). **8.910 filas × 38 columnas.**
Origen: scrape de la tienda de semillas seed-city.com. Precios en **GBP (£)**.

> ⚠️ Ojo: el dataset reporta **0% de nulos**, pero eso es engañoso — hay columnas constantes, plantilladas y
> valores dentro de texto que hay que limpiar. Ver la columna "Notas".

## 🧪 Dimensión química / efectos (nuestro hilo medicinal)

| Columna | Qué es | Tipo | Notas de limpieza |
|---|---|---|---|
| `thc` | % de THC (psicoactivo) | texto `"21.8%"` | Parsear → `thc_pct` (float). 804 valores únicos |
| `cbd` | % de CBD (no psicoactivo, terapéutico) | texto `"1.5%"` | Parsear → `cbd_pct` (float). 226 únicos |
| `strength` | Potencia percibida | categórica | `Normal` (6176), `Super Strength` (2506), `Mild` (211) + mezclas |
| `effect` | Efectos (multi-etiqueta) | texto con comas | Explode. Ej: `"Relaxed, Energetic"`. 1116 combinaciones |
| `medical_strains` | Usos medicinales (multi-etiqueta) | texto con comas | Explode. Ej: `"Insomnia, Pain Relief"`. 1419 combinaciones |
| `flavor` | Sabores (multi-etiqueta) | texto con comas | Explode. Ej: `"Sweet, Citrus, Pine"`. 445 combinaciones |
| `smell_taste` | Aroma/sabor (multi-etiqueta, más granular) | texto con comas | Explode. 2899 combinaciones |

## 💰 Dimensión comercial / mercado (nuestro cierre freelance)

| Columna | Qué es | Tipo | Notas |
|---|---|---|---|
| `current_price_gbp` | Precio actual (£) | float | Limpio. 1776 valores |
| `original_price_gbp` | Precio original antes de descuento (£) | float | Limpio |
| `discount_percent` | % de descuento | float | Solo 5 valores (10, 20, 30, 40…) |
| `breeder` | Casa productora de semillas | categórica | 268 breeders. Clave para análisis de mercado |
| `pack_options` | Presentaciones y precios por cantidad | texto complejo | Ej: `"3 Feminised Seeds (GBP 18.54) \| 5 Feminised..."`. Se puede extraer precio mínimo/por semilla |
| `stock_availability` | Disponibilidad | casi-constante | Solo `In Stock` / (raro) — poco útil |
| `product_url` | Link al producto | texto | Identificador, no analítico |

## 🌱 Dimensión botánica / cultivo (contexto de apoyo)

| Columna | Qué es | Tipo | Notas |
|---|---|---|---|
| `indica_sativa` | Tipo dominante | categórica sucia | 15 variantes; consolidar → `type_simple` (Indica/Sativa/Híbrido) |
| `type_ratio` | Proporción indica/sativa | texto `"30% Indica / 70% Sativa"` | Parsear → `indica_pct`, `sativa_pct` |
| `strain_type_summary` | Resumen del tipo | categórica | 36 variantes; redundante con `indica_sativa` |
| `seed_type` | Tipo de semilla | categórica | `Feminized` (6772), `Regular` (1672), mezcla (466) |
| `flowering_period_type` | Fotoperiodo | categórica | `12/12 Photoperiod`, `Autoflowering` |
| `genetic_background` | Linaje/cruce genético | texto | Ej: `"Northern Lights x Haze"`. 271 únicos |
| `environment` | Dónde crece | multi-etiqueta | `Indoor, Outdoor, Greenhouse` |
| `climate` | Clima ideal | categórica | 26 valores (`Mediterranean`, `Tropical`…) |
| `yield_indoor` | Rendimiento interior | texto `"406.0g/m²"` | Parsear → número (g/m²) |
| `yield_outdoor` | Rendimiento exterior | texto `"523.0g/plant"` | Parsear → número (g/planta) |
| `height_indoor` | Altura interior | texto `"166.0cm"` | Parsear → número (cm) |
| `height_outdoor` | Altura exterior | texto `"152.0cm"` | Parsear → número (cm) |
| `indoor_height_detail` | Rango de altura interior | categórica | `"Medium (81cm - 140cm)"` |
| `indoor_flowering_time` | Rango de floración interior | categórica | `"Medium (56 to 90 days)"` |
| `flowering_time` | Tiempo de floración | texto `"64 days"` | Parsear → número (días) |
| `outdoor_harvest_time` | Época de cosecha exterior | categórica | `"The End of October"` |
| `harvest_month` | Mes de cosecha | categórica | `"Mid October"` |

## 🏷️ Identificación y texto libre

| Columna | Qué es | Notas |
|---|---|---|
| `strain_name` | Nombre de la cepa | 8080 únicos de 8910 → ~830 nombres repetidos (posibles variantes) |
| `description` | Descripción comercial | Texto libre; útil para nubes de palabras |
| `overview` | Resumen | Texto semi-plantillado |

## 🗑️ Columnas a descartar (ruido)

| Columna | Motivo |
|---|---|
| `sale_item` | Constante: 1 solo valor (`"Cannabis Seeds Currently on Sale"`) |
| `most_popular_seeds` | Constante: 1 solo valor |
| `experience` | Plantillada: 52 frases casi idénticas, sin valor analítico |
| `growth_and_harvest` | Plantillada: 7 frases genéricas |
| `stock_availability` | Casi-constante (2 valores, casi todo `In Stock`) |

---
**Glosario mínimo (para la prosa):**
- **THC**: tetrahidrocannabinol, el compuesto psicoactivo principal (el "colocón").
- **CBD**: cannabidiol, no psicoactivo, asociado a efectos terapéuticos (dolor, ansiedad, inflamación).
- **Indica / Sativa / Híbrido**: clasificación tradicional de subespecies; Indica se asocia a efecto
  relajante/corporal, Sativa a efecto energético/cerebral, Híbrido a mezclas.
- **Feminized**: semillas que producen casi siempre plantas hembra (las que dan flor útil).
- **Autoflowering**: florecen por edad, no por fotoperiodo.
