"""
Regenera el gráfico mc_01_mexico_funnel.png con la nomenclatura corregida.

Antes: dos filas redundantes ('Pasa de grupos' y '16avos' eran 97% ambas).
Ahora: una sola fila combinada que aclara la equivalencia.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as patches

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / 'data' / 'processed'
OUT = ROOT / 'outputs'

VERDE_MX = '#006847'
ROJO = '#CE1126'
GRIS = '#999999'

sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6.5)
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

df = pd.read_csv(PROCESSED / 'mc_probs_acumuladas.csv', index_col=0)
mx = df.loc['Mexico']

# Funnel corregido: sin duplicar la fila "pasa grupos" / "16avos"
# Cada barra representa "llegar a esta ronda eliminatoria"
fases_es = [
    'Pasa de grupos\n(entra a 16avos)',
    'Octavos\n(gana 16avos)',
    'Cuartos\n("sexto partido")',
    'Semifinales',
    'Final',
    'Campeón',
]
valores = [
    mx['Round of 32'] * 100,       # 97.0% — pasar de grupos = entrar a 16avos
    mx['Round of 16'] * 100,       # 63.7% — ganar 16avos = entrar a octavos
    mx['Quarter-final'] * 100,     # 30.4% — ganar octavos = sexto partido
    mx['Semi-final'] * 100,
    mx['Final'] * 100,
    mx['Champion'] * 100,
]

colors = [VERDE_MX, VERDE_MX, ROJO, GRIS, GRIS, GRIS]

fig, ax = plt.subplots(figsize=(12, 6.5))
bars = ax.bar(fases_es, valores, color=colors, edgecolor='black')

for bar, v in zip(bars, valores):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 1.8,
            f'{v:.1f}%', ha='center', fontsize=14, fontweight='bold')

# Marcar el sexto partido con línea destacada
ax.axvline(2, color=ROJO, linestyle=':', alpha=0.5, linewidth=1)

ax.set_ylabel('Probabilidad acumulada', fontsize=12)
ax.set_ylim(0, max(valores) + 15)
ax.set_title('Probabilidad de México en cada fase del Mundial 2026\n'
             '10,000 simulaciones Montecarlo · ELO actual 1823 · Anfitrión',
             loc='left', fontsize=13, pad=15)

plt.xticks(fontsize=11)
plt.tight_layout()
plt.savefig(OUT / 'mc_01_mexico_funnel.png', dpi=120, bbox_inches='tight')
plt.close()
print('OK regenerado: outputs/mc_01_mexico_funnel.png')
