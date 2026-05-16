"""
Sistema ELO para selecciones nacionales de fútbol.

Implementación basada en el sistema clásico de Arpad Elo (1960s) adaptado
a fútbol internacional, con K-factor variable por importancia del torneo
y bonus por jugar de local.

Referencias:
- Sistema FIFA Elo Ratings: https://www.eloratings.net/about
- Hyndman & Athanasopoulos para K-factor en deportes.

Decisiones de diseño:
- Rating inicial: 1500 para todas las selecciones (estándar Elo).
- Burn-in: los primeros 10 años de datos sirven para estabilizar; no usar
  esos ratings en producción.
- Home advantage: +100 puntos al equipo local en el cálculo del expected
  (no se modifica el rating, solo la expectativa del partido).
- Empate: cuenta como 0.5 para ambos.
- Margen de victoria: el ELO clásico ignora el marcador; solo importa el
  resultado (W/D/L). Existen variantes con multiplier por diferencia de
  goles; aquí mantenemos la versión clásica para fidelidad y simplicidad.
"""

from __future__ import annotations

import pandas as pd
from collections import defaultdict
from typing import Iterable


# K-factor por tier de torneo (ver tournament_tier en data limpia)
K_FACTOR_POR_TIER: dict[int, int] = {
    1: 50,   # Copa del Mundo, Confederations
    2: 30,   # Continentales (Eurocopa, Copa América, etc.)
    3: 20,   # Eliminatorias y Nations League
    4: 10,   # Amistosos y resto
}

# Bonus para el equipo local (en puntos de rating, no se transfiere)
HOME_ADVANTAGE = 100

# Rating de partida
DEFAULT_RATING = 1500


def expected_score(rating_a: float, rating_b: float, home_advantage: float = 0) -> float:
    """Probabilidad esperada (0 a 1) de que A gane sobre B.

    Si A juega en casa, pasar home_advantage > 0 para inflar la expectativa.

    Ejemplo:
        >>> round(expected_score(1500, 1500), 3)
        0.5
        >>> round(expected_score(1700, 1500), 3)
        0.76
    """
    diff = (rating_b - rating_a) - home_advantage
    return 1.0 / (1.0 + 10 ** (diff / 400))


def actual_score(home_goals: int, away_goals: int) -> tuple[float, float]:
    """Convierte un marcador en (score_home, score_away).

    1 = victoria, 0.5 = empate, 0 = derrota.
    """
    if home_goals > away_goals:
        return 1.0, 0.0
    if home_goals < away_goals:
        return 0.0, 1.0
    return 0.5, 0.5


def update_pair(
    rating_home: float,
    rating_away: float,
    home_goals: int,
    away_goals: int,
    k_factor: float,
    is_neutral: bool = False,
) -> tuple[float, float]:
    """Calcula los nuevos ratings tras un partido entre home y away."""
    bonus = 0 if is_neutral else HOME_ADVANTAGE
    exp_home = expected_score(rating_home, rating_away, home_advantage=bonus)
    exp_away = 1.0 - exp_home

    act_home, act_away = actual_score(home_goals, away_goals)

    new_home = rating_home + k_factor * (act_home - exp_home)
    new_away = rating_away + k_factor * (act_away - exp_away)
    return new_home, new_away


def run_history(matches: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    """Procesa cronológicamente todos los partidos y devuelve:

    - timeline: DataFrame con (date, team, rating_after) — un registro por
      equipo por partido jugado.
    - final_ratings: dict {team: rating} con el rating final de cada selección.

    Espera columnas: date, home_team, away_team, home_score, away_score,
    tournament_tier, neutral.
    """
    required = {'date', 'home_team', 'away_team', 'home_score', 'away_score',
                'tournament_tier', 'neutral'}
    missing = required - set(matches.columns)
    if missing:
        raise ValueError(f'Faltan columnas: {missing}')

    df = matches.dropna(subset=['home_score', 'away_score']).copy()
    df = df.sort_values('date').reset_index(drop=True)

    ratings: dict[str, float] = defaultdict(lambda: DEFAULT_RATING)

    timeline_rows: list[dict] = []

    for row in df.itertuples(index=False):
        k = K_FACTOR_POR_TIER.get(int(row.tournament_tier), 10)
        r_home = ratings[row.home_team]
        r_away = ratings[row.away_team]
        new_home, new_away = update_pair(
            r_home, r_away,
            int(row.home_score), int(row.away_score),
            k_factor=k, is_neutral=bool(row.neutral),
        )
        ratings[row.home_team] = new_home
        ratings[row.away_team] = new_away

        timeline_rows.append({'date': row.date, 'team': row.home_team, 'rating': new_home})
        timeline_rows.append({'date': row.date, 'team': row.away_team, 'rating': new_away})

    timeline = pd.DataFrame(timeline_rows)
    return timeline, dict(ratings)


def latest_ratings_table(timeline: pd.DataFrame, min_matches: int = 30) -> pd.DataFrame:
    """Tabla de ELOs más recientes por equipo, filtrada a equipos con
    al menos `min_matches` partidos (para evitar selecciones de exhibición)."""
    counts = timeline.groupby('team').size().rename('n_matches')
    latest = (timeline.sort_values('date')
                       .groupby('team').last()
                       .rename(columns={'rating': 'elo_actual'}))
    out = latest.join(counts).reset_index()
    out = out[out['n_matches'] >= min_matches]
    return out.sort_values('elo_actual', ascending=False).reset_index(drop=True)
