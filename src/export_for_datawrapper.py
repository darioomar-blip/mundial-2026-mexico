"""
Exporta 4 CSVs limpios y listos para arrastrar a Datawrapper.

Datawrapper acepta CSV/TSV directamente:
1. Entras a datawrapper.de
2. "Create new chart"
3. "Upload data" → arrastras el CSV
4. Eliges tipo de gráfico
5. Personalizas y exportas
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / 'data' / 'processed'
OUT = ROOT / 'outputs' / 'datos_datawrapper'
OUT.mkdir(parents=True, exist_ok=True)

# Datos base
df = pd.read_csv(PROCESSED / 'mc_probs_acumuladas.csv', index_col=0)
mx = df.loc['Mexico']
mexico_wc = pd.read_csv(PROCESSED / 'mexico_wc_with_elo.csv')


# ============================================================
# 1. FUNNEL DE MÉXICO 2026 — Barra horizontal
# ============================================================
funnel = pd.DataFrame({
    'Fase': [
        'Pasa de grupos (entra a 16avos)',
        'Gana 16avos (entra a octavos)',
        'Cuartos (sexto partido)',
        'Semifinales',
        'Final',
        'Campeón',
    ],
    'Probabilidad (%)': [
        round(mx['Round of 32'] * 100, 1),
        round(mx['Round of 16'] * 100, 1),
        round(mx['Quarter-final'] * 100, 1),
        round(mx['Semi-final'] * 100, 1),
        round(mx['Final'] * 100, 1),
        round(mx['Champion'] * 100, 1),
    ],
    'Resaltar': ['', '', 'sí', '', '', ''],
})
funnel.to_csv(OUT / '1_mexico_funnel.csv', index=False)


# ============================================================
# 2. TOP 10 FAVORITOS AL TÍTULO — Barra horizontal
# ============================================================
campeones = df['Champion'].sort_values(ascending=False).head(10) * 100
# Agregar México como referencia (#12)
mexico_pct = round(df.loc['Mexico', 'Champion'] * 100, 2)
top10 = pd.DataFrame({
    'Selección': list(campeones.index),
    'Probabilidad campeón (%)': campeones.round(2).tolist(),
    'Resaltar': [''] * 10,
})
# Añadir fila separada para México como contexto
top10_con_mexico = pd.concat([
    top10,
    pd.DataFrame({
        'Selección': ['…'],
        'Probabilidad campeón (%)': [None],
        'Resaltar': [''],
    }),
    pd.DataFrame({
        'Selección': ['#12  México'],
        'Probabilidad campeón (%)': [mexico_pct],
        'Resaltar': ['sí'],
    }),
], ignore_index=True)
top10_con_mexico.to_csv(OUT / '2_top10_campeones.csv', index=False)


# ============================================================
# 3. MÉXICO HISTÓRICO — P(cuartos) vs realidad
# ============================================================
# Usamos las probabilidades del notebook 05 (modelo simple)
# para los 7 mundiales históricos + el actual
import pickle, numpy as np
with open(ROOT / 'src' / 'trained_models' / 'logit_host.pkl', 'rb') as f:
    logit = pickle.load(f)
lc = logit['logit_cuartos']

los_8 = mexico_wc[mexico_wc['edition'].isin(
    [1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022]
)].copy()
los_8['p_cuartos'] = los_8['elo_pre'].apply(
    lambda e: lc.predict(np.array([[1, e - 1750, 0]]))[0] * 100)

# 2026 viene del simulador Montecarlo
fila_2026 = pd.DataFrame({
    'edition': [2026],
    'p_cuartos': [round(mx['Quarter-final'] * 100, 1)],
    'ultima_fase': ['(por jugar)'],
})
historico = pd.concat([
    los_8[['edition', 'p_cuartos', 'ultima_fase']].rename(
        columns={'edition': 'Mundial',
                 'p_cuartos': 'P(llegar a cuartos) %',
                 'ultima_fase': 'Resultado real'}),
    fila_2026.rename(columns={'edition': 'Mundial',
                              'p_cuartos': 'P(llegar a cuartos) %',
                              'ultima_fase': 'Resultado real'}),
], ignore_index=True)
historico['P(llegar a cuartos) %'] = historico['P(llegar a cuartos) %'].round(1)
historico['Resaltar'] = historico['Mundial'].apply(
    lambda x: 'sí' if x == 2026 else '')
historico.to_csv(OUT / '3_mexico_historico.csv', index=False)


# ============================================================
# 4. EFECTO ANFITRIÓN — Comparación directa Anfitrión vs No anfitrión
#    (más interpretable que el forest plot)
# ============================================================
lg = logit['logit_grupos']
lc_logit = logit['logit_cuartos']
elo_mx = 1823

# ELO centrado a 1750 (como está entrenado el modelo)
x_anf = np.array([[1, elo_mx - 1750, 1]])
x_no = np.array([[1, elo_mx - 1750, 0]])

p_g_anf = round(lg.predict(x_anf)[0] * 100, 1)
p_g_no = round(lg.predict(x_no)[0] * 100, 1)
p_c_anf = round(lc_logit.predict(x_anf)[0] * 100, 1)
p_c_no = round(lc_logit.predict(x_no)[0] * 100, 1)

# Formato grouped bar chart: una fila por evento, columnas por escenario
efecto = pd.DataFrame({
    'Evento': [
        'Pasa de grupos',
        'Llega a CUARTOS (sexto partido)',
    ],
    'Sin localía (%)': [p_g_no, p_c_no],
    'Con localía — anfitrión (%)': [p_g_anf, p_c_anf],
    'Ganancia (pp)': [
        round(p_g_anf - p_g_no, 1),
        round(p_c_anf - p_c_no, 1),
    ],
})
efecto.to_csv(OUT / '4_efecto_anfitrion.csv', index=False)

# Borrar el CSV viejo de forest plot si existe
viejo = OUT / '4_efecto_anfitrion_OR.csv'
if viejo.exists():
    viejo.unlink()


# ============================================================
# 5. GRUPO A — Probabilidades de los 4 equipos
# ============================================================
grupo_a = pd.DataFrame({
    'Selección': ['México', 'Corea del Sur', 'Rep. Checa', 'Sudáfrica'],
    'P(pasa grupos) %': [
        round(df.loc['Mexico', 'Round of 32'] * 100, 1),
        round(df.loc['South Korea', 'Round of 32'] * 100, 1),
        round(df.loc['Czech Republic', 'Round of 32'] * 100, 1),
        round(df.loc['South Africa', 'Round of 32'] * 100, 1),
    ],
    'P(cuartos) %': [
        round(df.loc['Mexico', 'Quarter-final'] * 100, 1),
        round(df.loc['South Korea', 'Quarter-final'] * 100, 1),
        round(df.loc['Czech Republic', 'Quarter-final'] * 100, 1),
        round(df.loc['South Africa', 'Quarter-final'] * 100, 1),
    ],
    'ELO actual': [1823, 1759, 1670, 1613],
})
grupo_a.to_csv(OUT / '5_grupo_A.csv', index=False)


# ============================================================
# Listado
# ============================================================
print('CSVs exportados a:', OUT)
print()
for p in sorted(OUT.glob('*.csv')):
    df_show = pd.read_csv(p)
    print(f'{p.name}  →  {len(df_show)} filas')
