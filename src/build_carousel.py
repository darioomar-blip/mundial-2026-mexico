"""
Generador del carrusel de LinkedIn — 10 slides 1080×1350 (formato 4:5).

Sin emojis (matplotlib no los soporta en mac). Usa elementos gráficos puros.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'outputs' / 'carrusel'
OUT.mkdir(parents=True, exist_ok=True)

# Paleta
VERDE_MX = '#006847'
ROJO_MX = '#CE1126'
GRIS_CLARO = '#E8E8E8'
GRIS_TEXTO = '#444444'
NEGRO = '#1a1a1a'
DORADO = '#D4AF37'

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Helvetica Neue', 'Arial', 'DejaVu Sans']

FIG_W = 9
FIG_H = 11.25
DPI = 120


def base_slide(slide_n, total=10):
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12.5)
    ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.text(9.7, 0.3, f'{slide_n}/{total}', fontsize=11, color=GRIS_TEXTO,
            ha='right', va='bottom', alpha=0.6)
    ax.text(0.3, 0.3, 'El Sexto Partido  ·  México 2026',
            fontsize=10, color=GRIS_TEXTO, ha='left', va='bottom', alpha=0.7)
    return fig, ax


def bandera_mexico(ax, x, y, w=2.4, h=1.5):
    """Dibuja una mini-bandera de México (verde-blanco-rojo)."""
    tercio = w / 3
    ax.add_patch(Rectangle((x, y), tercio, h, facecolor=VERDE_MX, edgecolor='none'))
    ax.add_patch(Rectangle((x + tercio, y), tercio, h, facecolor='white',
                            edgecolor='#cccccc', linewidth=0.5))
    ax.add_patch(Rectangle((x + 2 * tercio, y), tercio, h, facecolor=ROJO_MX,
                            edgecolor='none'))


def save(fig, name):
    out = OUT / f'{name}.png'
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor='white', pad_inches=0.3)
    plt.close(fig)
    print(f'  OK  {out.name}')


# ============================================================
# SLIDE 1 — Hook
# ============================================================
def slide_1():
    fig, ax = base_slide(1)
    bandera_mexico(ax, 3.8, 9.8, w=2.4, h=1.5)

    ax.text(5, 8.2, '¿Por qué México', fontsize=46, ha='center',
            color=NEGRO, fontweight='bold')
    ax.text(5, 7.2, 'siempre cae en', fontsize=46, ha='center',
            color=NEGRO, fontweight='bold')
    ax.text(5, 6.2, 'octavos?', fontsize=46, ha='center',
            color=ROJO_MX, fontweight='bold')

    ax.text(5, 4.4, 'Analicé 49,329 partidos', fontsize=22, ha='center',
            color=GRIS_TEXTO)
    ax.text(5, 3.7, 'internacionales para', fontsize=22, ha='center',
            color=GRIS_TEXTO)
    ax.text(5, 3.0, 'responderlo con datos.', fontsize=22, ha='center',
            color=GRIS_TEXTO)

    ax.text(5, 1.4, 'Spoiler: no es maldición.',
            fontsize=24, ha='center', color=VERDE_MX, style='italic',
            fontweight='bold')

    save(fig, '01_hook')


# ============================================================
# SLIDE 2 — La hipótesis
# ============================================================
def slide_2():
    fig, ax = base_slide(2)
    ax.text(5, 11.3, 'La hipótesis', fontsize=36, ha='center',
            color=VERDE_MX, fontweight='bold')

    ax.text(5, 9.5, 'Si México siempre cae en octavos…', fontsize=22,
            ha='center', color=GRIS_TEXTO)

    box = FancyBboxPatch((0.6, 7), 8.8, 1.6, boxstyle='round,pad=0.1',
                          facecolor=GRIS_CLARO, edgecolor='none')
    ax.add_patch(box)
    ax.text(5, 7.8, '¿Es maldición o es exactamente',
            fontsize=22, ha='center', color=NEGRO, fontweight='bold')
    ax.text(5, 7.25, 'lo que la estadística predice?',
            fontsize=22, ha='center', color=NEGRO, fontweight='bold')

    ax.text(5, 5.5, 'Para responder necesitábamos:', fontsize=20,
            ha='center', color=GRIS_TEXTO)

    bullets = [
        'Saber el nivel real de México en cada año',
        'Predecir cuántos goles mete y recibe',
        'Aislar cuánto vale ser local',
        'Simular el torneo 10,000 veces',
    ]
    for i, b in enumerate(bullets):
        y = 4.5 - i * 0.7
        # Cuadrito verde como bullet
        ax.add_patch(Rectangle((1.2, y - 0.12), 0.3, 0.3,
                                facecolor=VERDE_MX, edgecolor='none'))
        ax.text(1.8, y + 0.03, b, fontsize=18, color=NEGRO, va='center')

    save(fig, '02_hipotesis')


# ============================================================
# SLIDE 3 — Los datos
# ============================================================
def slide_3():
    fig, ax = base_slide(3)
    ax.text(5, 11.3, 'Los datos', fontsize=36, ha='center',
            color=VERDE_MX, fontweight='bold')

    def num_box(x, num, label):
        ax.text(x, 8.0, num, fontsize=58, ha='center', color=ROJO_MX,
                fontweight='bold')
        ax.text(x, 6.6, label, fontsize=15, ha='center', color=GRIS_TEXTO)

    num_box(2.5, '49,257', 'Partidos\ninternacionales')
    num_box(5.0, '154', 'Años\n(1872 — 2026)')
    num_box(7.5, '964', 'Partidos\nde Mundial')

    ax.text(5, 4.8, 'Dataset abierto:', fontsize=18, ha='center',
            color=GRIS_TEXTO)
    ax.text(5, 4.2, 'github.com/martj42/international_results',
            fontsize=14, ha='center', color=VERDE_MX,
            family='monospace')

    ax.text(5, 2.5, '23 ediciones del Mundial', fontsize=20,
            ha='center', color=NEGRO, fontweight='bold')
    ax.text(5, 1.8, '230 selecciones con historial', fontsize=18,
            ha='center', color=GRIS_TEXTO)

    save(fig, '03_datos')


# ============================================================
# SLIDE 4 — El método
# ============================================================
def slide_4():
    fig, ax = base_slide(4)
    ax.text(5, 11.3, 'El método', fontsize=36, ha='center',
            color=VERDE_MX, fontweight='bold')

    pasos = [
        ('1', 'Sistema ELO dinámico', 'Rating recalculado tras cada partido,\n150 años de historia.', 9.2),
        ('2', 'GLM Poisson', 'Modelo de goles esperados según\nELO + ventaja de local.', 7.1),
        ('3', 'Regresión logística', 'Aislar el efecto puro de ser\nanfitrión controlando por nivel.', 5.0),
        ('4', 'Simulación Montecarlo', '10,000 mundiales simulados\ncon el calendario real 2026.', 2.9),
    ]
    for num, titulo, desc, y in pasos:
        circle = patches.Circle((1.0, y), 0.55, facecolor=VERDE_MX, edgecolor='none')
        ax.add_patch(circle)
        ax.text(1.0, y, num, fontsize=28, ha='center', va='center',
                color='white', fontweight='bold')
        ax.text(2.1, y + 0.3, titulo, fontsize=20, color=NEGRO,
                fontweight='bold', va='center')
        ax.text(2.1, y - 0.45, desc, fontsize=14, color=GRIS_TEXTO,
                va='center')

    save(fig, '04_metodo')


# ============================================================
# SLIDE 5 — México histórico
# ============================================================
def slide_5():
    fig, ax = base_slide(5)
    ax.text(5, 11.3, 'El "techo" no era casualidad', fontsize=29,
            ha='center', color=VERDE_MX, fontweight='bold')
    ax.text(5, 10.4, 'Probabilidad apriori de que México cayera',
            fontsize=15, ha='center', color=GRIS_TEXTO)
    ax.text(5, 10.0, 'exactamente en octavos según el modelo',
            fontsize=15, ha='center', color=GRIS_TEXTO)

    ax2 = fig.add_axes([0.13, 0.22, 0.74, 0.43])
    ediciones = ['1994', '1998', '2002', '2006', '2010', '2014', '2018']
    probs = [30.3, 30.7, 30.3, 30.7, 30.4, 30.8, 29.7]
    bars = ax2.bar(ediciones, probs, color=VERDE_MX, edgecolor='none', width=0.7)
    ax2.axhline(np.mean(probs), color=ROJO_MX, linestyle='--', linewidth=2)
    ax2.text(6.4, np.mean(probs) + 1.5, f'Promedio: {np.mean(probs):.0f}%',
             color=ROJO_MX, fontsize=14, fontweight='bold', ha='right')
    for bar, p in zip(bars, probs):
        ax2.text(bar.get_x() + bar.get_width() / 2, p + 0.5, f'{p:.0f}%',
                 ha='center', fontsize=12, color=NEGRO)
    ax2.set_ylim(0, 45)
    ax2.set_ylabel('P(eliminarse en octavos)', fontsize=12)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.tick_params(labelsize=11)

    ax.text(5, 1.4, 'Cada vez, eliminarse en octavos era',
            fontsize=17, ha='center', color=NEGRO)
    ax.text(5, 0.85, 'el resultado individual MÁS probable.',
            fontsize=17, ha='center', color=ROJO_MX, fontweight='bold')

    save(fig, '05_historico')


# ============================================================
# SLIDE 6 — El patrón: local vs neutral
# ============================================================
def slide_6():
    fig, ax = base_slide(6)
    ax.text(5, 11.4, 'El patrón que nadie se atreve a decir',
            fontsize=27, ha='center', color=VERDE_MX, fontweight='bold')

    # ---------- BLOQUE LOCAL (verde) ----------
    box_local = FancyBboxPatch((0.4, 7.3), 9.2, 2.7,
                                boxstyle='round,pad=0.1',
                                facecolor='#E8F3EE', edgecolor=VERDE_MX,
                                linewidth=1.5)
    ax.add_patch(box_local)
    ax.text(0.8, 9.55, '2 veces local', fontsize=22, color=VERDE_MX,
            fontweight='bold')
    locales = [('1970', 'CUARTOS'), ('1986', 'CUARTOS')]
    for i, (ed, res) in enumerate(locales):
        y = 8.8 - i * 0.7
        ax.text(1.2, y, ed, fontsize=18, color=NEGRO, fontweight='bold')
        ax.text(2.4, y, '→', fontsize=18, color=GRIS_TEXTO)
        ax.text(3.0, y, res, fontsize=18, color=VERDE_MX, fontweight='bold')
        ax.add_patch(Rectangle((7.5, y - 0.18), 1.7, 0.45,
                                facecolor=VERDE_MX, edgecolor='none'))
        ax.text(8.35, y + 0.05, 'PASA', fontsize=13, ha='center',
                color='white', va='center', fontweight='bold')

    # ---------- BLOQUE NEUTRAL (rojo) ----------
    box_neutro = FancyBboxPatch((0.4, 1.8), 9.2, 5.1,
                                 boxstyle='round,pad=0.1',
                                 facecolor='#FDECEC', edgecolor=ROJO_MX,
                                 linewidth=1.5)
    ax.add_patch(box_neutro)
    ax.text(0.8, 6.45, '7 veces NO local', fontsize=22, color=ROJO_MX,
            fontweight='bold')
    neutros = ['1994', '1998', '2002', '2006', '2010', '2014', '2018']
    for i, ed in enumerate(neutros):
        y = 5.7 - i * 0.55
        ax.text(1.2, y, ed, fontsize=16, color=NEGRO, fontweight='bold')
        ax.text(2.4, y, '→', fontsize=16, color=GRIS_TEXTO)
        ax.text(3.0, y, 'octavos', fontsize=16, color=GRIS_TEXTO)
        ax.add_patch(Rectangle((7.5, y - 0.16), 1.7, 0.4,
                                facecolor=ROJO_MX, edgecolor='none'))
        ax.text(8.35, y + 0.04, 'OUT', fontsize=12, ha='center',
                color='white', va='center', fontweight='bold')

    ax.text(5, 1.0, '2026: vuelve a ser local. ¿Coincidencia o patrón?',
            fontsize=17, ha='center', color=NEGRO, style='italic',
            fontweight='bold')

    save(fig, '06_patron_local')


# ============================================================
# SLIDE 7 — Efecto anfitrión
# ============================================================
def slide_7():
    fig, ax = base_slide(7)
    ax.text(5, 11.3, '¿Cuánto vale ser anfitrión?',
            fontsize=30, ha='center', color=VERDE_MX, fontweight='bold')
    ax.text(5, 10.4, 'Regresión logística controlando por ELO',
            fontsize=15, ha='center', color=GRIS_TEXTO)
    ax.text(5, 10.0, 'sobre los mundiales 1986–2022',
            fontsize=15, ha='center', color=GRIS_TEXTO)

    ax.text(5, 7.5, '×7.8', fontsize=110, ha='center',
            color=ROJO_MX, fontweight='bold')
    ax.text(5, 5.5, 'multiplica las probabilidades de', fontsize=18,
            ha='center', color=NEGRO)
    ax.text(5, 4.9, 'llegar a CUARTOS de final', fontsize=20,
            ha='center', color=NEGRO, fontweight='bold')

    ax.text(5, 3.5, 'Odds Ratio = 7.82', fontsize=16, ha='center',
            color=GRIS_TEXTO, family='monospace')
    ax.text(5, 3.0, 'IC 95% [2.0 — 31.1]   ·   p = 0.0035', fontsize=14,
            ha='center', color=GRIS_TEXTO, family='monospace')

    ax.text(5, 1.5, 'Incluso el extremo más conservador del intervalo',
            fontsize=14, ha='center', color=GRIS_TEXTO, style='italic')
    ax.text(5, 1.0, 'sigue duplicando las probabilidades.',
            fontsize=14, ha='center', color=GRIS_TEXTO, style='italic')

    save(fig, '07_efecto_anfitrion')


# ============================================================
# SLIDE 8 — México 2026 funnel
# ============================================================
def slide_8():
    fig, ax = base_slide(8)
    ax.text(5, 11.3, 'México en el Mundial 2026', fontsize=30,
            ha='center', color=VERDE_MX, fontweight='bold')
    ax.text(5, 10.4, '10,000 simulaciones del torneo completo',
            fontsize=15, ha='center', color=GRIS_TEXTO)

    fases = [
        ('Pasa de grupos\n(entra a 16avos)', 97.0, VERDE_MX),
        ('Gana 16avos\n(entra a octavos)', 63.7, VERDE_MX),
        ('SEXTO PARTIDO\n(cuartos de final)', 30.4, ROJO_MX),
        ('Semifinales', 12.5, '#888888'),
        ('Final', 4.5, '#888888'),
        ('Campeón', 1.5, '#888888'),
    ]
    max_p = 100
    for i, (label, p, color) in enumerate(fases):
        y = 9.0 - i * 1.25
        bar_width = (p / max_p) * 6.5
        rect = patches.FancyBboxPatch((2.4, y - 0.32), bar_width, 0.64,
                                       boxstyle='round,pad=0.02',
                                       facecolor=color, edgecolor='none')
        ax.add_patch(rect)
        ax.text(2.3, y, label, fontsize=13, color=NEGRO, ha='right',
                va='center', fontweight='bold')
        ax.text(2.4 + bar_width + 0.2, y, f'{p:.1f}%',
                fontsize=17, color=color, va='center', fontweight='bold')

    ax.text(5, 0.95, 'Por primera vez en la historia, la probabilidad',
            fontsize=14, ha='center', color=GRIS_TEXTO)
    ax.text(5, 0.4, 'del sexto partido > 28%.',
            fontsize=15, ha='center', color=ROJO_MX, fontweight='bold')

    save(fig, '08_mexico_2026')


# ============================================================
# SLIDE 9 — Quién levanta la copa
# ============================================================
def slide_9():
    fig, ax = base_slide(9)
    ax.text(5, 11.3, '¿Quién levanta la copa?', fontsize=30,
            ha='center', color=VERDE_MX, fontweight='bold')
    ax.text(5, 10.4, 'Top 10 favoritos al título según el modelo',
            fontsize=15, ha='center', color=GRIS_TEXTO)

    favoritos = [
        ('Argentina', 24.9),
        ('España', 22.4),
        ('Francia', 16.1),
        ('Brasil', 7.4),
        ('Inglaterra', 4.8),
        ('Portugal', 4.0),
        ('Países Bajos', 3.8),
        ('Colombia', 3.3),
        ('Alemania', 2.2),
        ('Uruguay', 1.6),
    ]
    for i, (nombre, p) in enumerate(favoritos):
        y = 9.2 - i * 0.75
        color = DORADO if i == 0 else GRIS_TEXTO
        # Bullet circular numerado
        circle = patches.Circle((1.2, y), 0.27,
                                 facecolor=color if i == 0 else VERDE_MX,
                                 edgecolor='none')
        ax.add_patch(circle)
        ax.text(1.2, y, str(i + 1), fontsize=13, ha='center', va='center',
                color='white', fontweight='bold')
        ax.text(2.0, y, nombre, fontsize=18, color=NEGRO, va='center')
        ax.text(8.6, y, f'{p:.1f}%', fontsize=18,
                color=color if i == 0 else NEGRO,
                ha='right', va='center', fontweight='bold')

    # México highlight
    box_mx = FancyBboxPatch((1.0, 0.85), 8.0, 0.9,
                             boxstyle='round,pad=0.08',
                             facecolor=VERDE_MX, edgecolor='none')
    ax.add_patch(box_mx)
    ax.text(5, 1.3, 'México: posición 12 con 1.5%',
            fontsize=16, ha='center', color='white', fontweight='bold')

    ax.text(5, 0.25, 'Ser anfitrión ayuda a avanzar fases, no a ganar el título.',
            fontsize=12, ha='center', color=GRIS_TEXTO, style='italic')

    save(fig, '09_campeones')


# ============================================================
# SLIDE 10 — Cierre + CTA
# ============================================================
def slide_10():
    fig, ax = base_slide(10)

    ax.text(5, 11.3, 'La lección', fontsize=36, ha='center',
            color=VERDE_MX, fontweight='bold')

    ax.text(5, 9.7, 'México no tenía maldición.',
            fontsize=24, ha='center', color=NEGRO, fontweight='bold')
    ax.text(5, 9.05, 'Tenía ELO 1750.',
            fontsize=24, ha='center', color=ROJO_MX, fontweight='bold')

    ax.text(5, 7.7, 'La diferencia entre', fontsize=16, ha='center',
            color=GRIS_TEXTO)
    ax.text(5, 7.15, '"los datos contradicen el sentido común"', fontsize=15,
            ha='center', color=NEGRO, style='italic')
    ax.text(5, 6.6, 'y', fontsize=15, ha='center', color=GRIS_TEXTO)
    ax.text(5, 6.05, '"los datos explican el sentido común"', fontsize=15,
            ha='center', color=NEGRO, style='italic')
    ax.text(5, 5.4, 'está en la pregunta que haces.', fontsize=16,
            ha='center', color=VERDE_MX, fontweight='bold')

    cta = FancyBboxPatch((1.0, 1.7), 8.0, 2.5, boxstyle='round,pad=0.15',
                          facecolor=VERDE_MX, edgecolor='none')
    ax.add_patch(cta)
    ax.text(5, 3.6, '¿Qué le preguntarías al modelo',
            fontsize=18, ha='center', color='white', fontweight='bold')
    ax.text(5, 3.0, 'que yo no le pregunté?',
            fontsize=18, ha='center', color='white', fontweight='bold')
    ax.text(5, 2.2, 'Repo + notebooks → primer comentario',
            fontsize=14, ha='center', color='white', style='italic')

    save(fig, '10_cierre')


def main():
    print('Generando carrusel de LinkedIn (10 slides 1080x1350)...')
    for slide in (slide_1, slide_2, slide_3, slide_4, slide_5,
                  slide_6, slide_7, slide_8, slide_9, slide_10):
        slide()
    print(f'\nListo. Archivos en: {OUT}')


if __name__ == '__main__':
    main()
