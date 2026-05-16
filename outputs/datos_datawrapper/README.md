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

## 4️⃣ `4_efecto_anfitrion_OR.csv` — Forest plot del efecto anfitrión

**Tipo de gráfico:** **Dot plot con barras de error**.

**Configuración:**
- Datawrapper tiene un tipo llamado **"Range plot"** o **"Dot plot"** — ideal para forest plots.
- Eje Y: "Evento"
- Punto central: "Odds Ratio"
- Barras: "IC 95% inferior" y "IC 95% superior"
- **Escala logarítmica** en eje X (importante para Odds Ratios).
- Línea de referencia en `OR = 1` con etiqueta: *"sin efecto"*.
- Título: *"¿Cuánto vale ser anfitrión del Mundial?"*
- Subtítulo: *"Odds Ratio controlando por ELO · Mundiales 1986–2022"*.

**Uso:** Slide 7 del carrusel.

**Alternativa más simple** si "Range plot" no convence:
- **Bar chart simple** con solo "Odds Ratio" en eje X.
- Anotar el IC 95% como texto debajo de cada barra.

---

## 5️⃣ `5_grupo_A.csv` — Equipos del Grupo A de México

**Tipo de gráfico:** **Grouped bar chart** (barras agrupadas).

**Configuración:**
- Eje Y: "Selección"
- Dos series: "P(pasa grupos) %" y "P(cuartos) %"
- "Color by column" → series con colores distintos (verde para grupos, rojo para cuartos).
- Título: *"Grupo A del Mundial 2026"*.
- Subtítulo: *"Probabilidades según el modelo · ELO entre paréntesis"*.

**Uso:** Slide adicional opcional (entre 4 y 5 del carrusel actual), o reemplaza el slide 5 si quieres meter más datos.

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
