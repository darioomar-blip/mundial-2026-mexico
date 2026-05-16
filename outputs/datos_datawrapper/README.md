# 📊 Datos listos para Datawrapper

5 archivos CSV optimizados para arrastrar y soltar directamente en [datawrapper.de](https://www.datawrapper.de). Cada uno está pensado para un gráfico específico del carrusel.

---

## 🚀 Flujo general (válido para los 5)

1. Entra a **[datawrapper.de](https://www.datawrapper.de)** → "**New chart**".
2. **Upload data** → arrastra el CSV o pega el contenido.
3. Elige el **tipo de gráfico** sugerido en cada sección abajo.
4. En "Visualize" personaliza colores, fuentes, anotaciones.
5. **Publish & Embed** → "Download PNG" (en alta resolución, 2x).

**Colores recomendados (paleta México):**

| Uso | Color |
|---|---|
| Principal | `#006847` (verde México) |
| Destacar / alerta | `#CE1126` (rojo) |
| Gris neutro | `#E8E8E8` |
| Acento dorado | `#D4AF37` |
| Texto secundario | `#444444` |

**Tipografía sugerida:** Inter, Roboto, o la default de Datawrapper (Roboto). Cualquiera de las tres funciona bien en LinkedIn.

---

## 1️⃣ `1_mexico_funnel.csv` — Funnel de México por fase

**Tipo de gráfico:** **Bar chart** (horizontal).

**Configuración:**
- Eje Y (etiquetas): columna "Fase"
- Eje X (valores): columna "Probabilidad (%)"
- Activar **"Color by column"** → usa "Resaltar" para que la fila marcada con `sí` se pinte distinto (la barra de "Cuartos / sexto partido").
- En "Annotate" agrega título: *"Probabilidad de México en cada fase del Mundial 2026"*.
- Subtítulo: *"10,000 simulaciones · ELO actual 1823 · Anfitrión"*.

**Uso:** Slide 8 del carrusel.

---

## 2️⃣ `2_top10_campeones.csv` — Top 10 favoritos al título

**Tipo de gráfico:** **Bar chart** (horizontal, ordenado descendente).

**Configuración:**
- Eje Y: "Selección"
- Eje X: "Probabilidad campeón (%)"
- "Color by column" → "Resaltar" (pinta México distinto al resto).
- La fila con `…` actúa como **separador visual** entre el top 10 y México (que es #12).
- Título: *"¿Quién levanta la copa en Nueva Jersey?"*
- Subtítulo: *"Top 10 favoritos según 10,000 simulaciones · México #12"*.

**Uso:** Slide 9 del carrusel.

**Tip:** Si Datawrapper no muestra bien la fila "…", la borras del CSV y agregas una **nota** manual ("📌 México: #12 — 1.5%") debajo del gráfico, en la sección "Annotate notes".

---

## 3️⃣ `3_mexico_historico.csv` — México histórico vs 2026

**Tipo de gráfico:** **Column chart** (vertical).

**Configuración:**
- Eje X: "Mundial"
- Eje Y: "P(llegar a cuartos) %"
- "Color by column" → "Resaltar" para pintar 2026 distinto (verde fuerte) y el resto en gris/verde claro.
- Línea horizontal opcional en `30%` con anotación: *"El 'techo' histórico"*.
- Anotaciones por barra: usar "Resultado real" como tooltip o texto encima.
- Título: *"México: el techo de cuartos no era casualidad"*.
- Subtítulo: *"P(llegar a cuartos) según el modelo en cada Mundial 1994–2026"*.

**Uso:** Slide 5 (variante) o crear un slide extra antes del 6.

---

## 4️⃣ `4_efecto_anfitrion.csv` — Antes vs después de ser anfitrión

**Tipo de gráfico recomendado:** **Grouped column chart** (barras agrupadas verticales).

> Cambio respecto a la versión anterior: el forest plot con Odds Ratios era confuso para audiencia general. Ahora se muestra la **comparación directa** de probabilidades para México (ELO 1823) en los dos escenarios: con localía vs sin localía. Mucho más intuitivo.

**Datos del CSV:**

| Evento | Sin localía | Con localía (anfitrión) | Ganancia |
|---|---|---|---|
| Pasa de grupos | 71.7% | 93.1% | +21.4 pp |
| Llega a cuartos (sexto partido) | 43.7% | 85.9% | +42.2 pp |

**Configuración en Datawrapper:**
- Eje X (categorías): "Evento"
- Series Y: "Sin localía (%)" y "Con localía — anfitrión (%)"
- Color **gris** para "Sin localía", **verde México** para "Con localía".
- Etiqueta cada barra con su porcentaje (no leyenda flotante).
- En "Annotate" agrega una nota encima del segundo par de barras: *"+42 puntos porcentuales solo por jugar en casa"*.
- Título: *"Cuánto vale ser anfitrión, en cifras concretas"*
- Subtítulo: *"México (ELO 1823) según el modelo logístico controlado por nivel"*.

**Lectura para el slide:** *"Sin localía, México tendría 44% de probabilidad de llegar a cuartos. Como anfitrión, sube a 86%. La diferencia es 42 puntos porcentuales — más que cualquier otra variable del modelo."*

**Uso:** Slide 7 del carrusel (reemplaza el "×7.8" actual con algo más concreto).

**Alternativa visual si quieres impacto extra:**
Hacer **dos bar charts horizontales separados** (uno para "pasa de grupos", otro para "llega a cuartos"), apilados verticalmente. Cada uno muestra una sola barra que se "rellena" desde la mitad hacia el extremo. Visualmente potente.

**Nota técnica:** Estas probabilidades vienen del modelo logístico del notebook 05 (efecto anfitrión histórico). Son distintas del simulador Montecarlo (notebook 06), que es más conservador (+2 pp en lugar de +42). Las dos respuestas son válidas — capturan cosas distintas. Si lo quieres documentar honestamente en el slide, anota: *"Estimación del modelo histórico. El simulador específico del bracket 2026 da un efecto más conservador (+2 pp)."* Eso te da puntos de credibilidad con perfiles técnicos.

---

## 5️⃣ `5_partidos_grupo_A.csv` — Los 3 partidos de México

**Tipo de gráfico recomendado:** **Stacked bar chart horizontal** (barras apiladas al 100%).

**Por qué este formato:** una barra por partido, dividida en 3 segmentos de colores (gana México / empate / gana rival). Es el formato clásico que usan medios deportivos para mostrar pronósticos de partidos. Inmediatamente comprensible.

**Datos del CSV:**

| Partido | Sede y fecha | P(gana MX) | P(empate) | P(gana rival) |
|---|---|---|---|---|
| México vs Sudáfrica | 11 jun · Azteca | **78.5%** | 14.2% | 7.2% |
| México vs Corea del Sur | 18 jun · Akron (Zapopan) | **57.3%** | 23.3% | 19.4% |
| México vs Rep. Checa | 24 jun · Azteca | **70.9%** | 18.0% | 11.0% |

**Configuración en Datawrapper:**
- Tipo: **"Stacked bar chart"** (no la versión "100% stacked" — los datos ya están en %).
- Eje Y (etiquetas): "Partido" (sede y fecha como subetiqueta).
- Series apiladas en este orden y color:
  - **P(gana México) %** → **verde México** (`#006847`)
  - **P(empate) %** → **gris** (`#E8E8E8`)
  - **P(gana rival) %** → **rojo** (`#CE1126`)
- Activa "Show value labels" para que aparezcan los % dentro de cada segmento.
- Título: *"Los 3 partidos de México en fase de grupos"*
- Subtítulo: *"Probabilidades según el modelo Poisson · ELO actual 1823 · Local en los 3"*.

**Lectura para el slide:**
*"México es favorito en sus 3 partidos. Sudáfrica es el rival más cómodo (78.5%); Corea del Sur el más difícil (solo 57% de probabilidad de ganar). Probabilidad de ganar los 3: 32%."*

**Uso:** Slide 5 (reemplaza el del histórico) o slide adicional entre 4 y 5.

**Bonus opcional:** abajo del gráfico puedes agregar las **expectativas de goles** (λ) como dato curioso:
- vs Sudáfrica: 2.5 – 0.6
- vs Corea: 1.8 – 0.9
- vs Rep. Checa: 2.2 – 0.7

Eso da textura sin saturar el gráfico principal.

---

## 🎨 Tips para que el carrusel se vea coherente

1. **Una sola paleta** para todos los gráficos: verde para "normal/positivo", rojo para "destacar/clave", gris para "contexto/secundario".
2. **Tipografía consistente**: elige una en Datawrapper y úsala en todos los slides.
3. **Tamaños iguales**: todos los gráficos a 1080×1350 (4:5) cuando los exportes.
4. **Anotaciones cortas**: máximo 1 frase encima del gráfico. Si necesitas explicar más, va al texto del post de LinkedIn.
5. **Sin leyendas flotantes**: pinta las anotaciones directamente sobre las barras.

---

## 📦 Una vez tengas los gráficos

1. Descarga cada PNG de Datawrapper en alta resolución.
2. Llévalos a **Canva** → crea un diseño "LinkedIn Carousel" (1080×1350).
3. Para cada slide:
   - Importa el PNG del gráfico de Datawrapper.
   - Agrega el título y texto auxiliar del carrusel actual (`outputs/carrusel/0X_*.png` te sirven de referencia).
   - Mantén el mismo número de slide y la marca "El Sexto Partido · México 2026" en pie de página.
4. Exporta como PDF (LinkedIn lo acepta como carrusel).

Listo. Carrusel con look profesional, datos sólidos, sin perder horas peleándose con matplotlib.
