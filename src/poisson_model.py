"""
Modelo Poisson para predicción de goles en fútbol internacional.

Modelo:
    log(λ) = α + β · elo_diff + γ · is_home

donde:
- λ = goles esperados que el equipo anota
- elo_diff = elo_self − elo_opponent (positivo si soy mejor)
- is_home = 1 si juego en casa (no neutral), 0 en cancha de visita o neutral

Se ajusta con statsmodels.GLM(family=Poisson()).

Decisiones de diseño:
- Long format: cada partido genera 2 filas (una por cada equipo) para que el
  modelo aprenda simétricamente.
- ELO previo al partido: se obtiene con merge_asof — para cada partido del
  equipo X en fecha t, tomamos el último rating registrado antes de t.
- Filtrado a partidos oficiales modernos (1990+, tier 1-3) para evitar
  amistosos ruidosos y formato antiguo.
"""

from __future__ import annotations

import pandas as pd
import numpy as np
import statsmodels.api as sm


def attach_elo(matches: pd.DataFrame, timeline: pd.DataFrame) -> pd.DataFrame:
    """Para cada partido, añade columnas elo_home_pre y elo_away_pre con el
    rating ELO previo al partido. Usa merge_asof por team y date.
    """
    matches = matches.sort_values('date').reset_index(drop=True).copy()
    tl = timeline.sort_values('date').reset_index(drop=True).copy()

    # ELO del local justo antes del partido
    home_merged = pd.merge_asof(
        matches[['date', 'home_team']].rename(columns={'home_team': 'team'}),
        tl.rename(columns={'rating': 'elo_pre'}),
        on='date', by='team', direction='backward', allow_exact_matches=False,
    )
    away_merged = pd.merge_asof(
        matches[['date', 'away_team']].rename(columns={'away_team': 'team'}),
        tl.rename(columns={'rating': 'elo_pre'}),
        on='date', by='team', direction='backward', allow_exact_matches=False,
    )

    out = matches.copy()
    out['elo_home_pre'] = home_merged['elo_pre'].values
    out['elo_away_pre'] = away_merged['elo_pre'].values
    return out


def to_long(matches_with_elo: pd.DataFrame) -> pd.DataFrame:
    """Convierte el dataset wide (una fila por partido) a long (dos filas).
    Cada fila representa la perspectiva de un equipo.
    """
    home_view = pd.DataFrame({
        'date': matches_with_elo['date'],
        'team': matches_with_elo['home_team'],
        'opponent': matches_with_elo['away_team'],
        'elo_self': matches_with_elo['elo_home_pre'],
        'elo_opp': matches_with_elo['elo_away_pre'],
        'goals_for': matches_with_elo['home_score'],
        'goals_against': matches_with_elo['away_score'],
        'is_home': (~matches_with_elo['neutral']).astype(int),
        'tier': matches_with_elo['tournament_tier'],
    })
    away_view = pd.DataFrame({
        'date': matches_with_elo['date'],
        'team': matches_with_elo['away_team'],
        'opponent': matches_with_elo['home_team'],
        'elo_self': matches_with_elo['elo_away_pre'],
        'elo_opp': matches_with_elo['elo_home_pre'],
        'goals_for': matches_with_elo['away_score'],
        'goals_against': matches_with_elo['home_score'],
        'is_home': 0,  # el visitante nunca es local
        'tier': matches_with_elo['tournament_tier'],
    })
    long = pd.concat([home_view, away_view], ignore_index=True)
    long['elo_diff'] = long['elo_self'] - long['elo_opp']
    return long


def fit_poisson(long_df: pd.DataFrame) -> sm.GLMResults:
    """Ajusta el modelo Poisson con statsmodels.

    Predictores: elo_diff (continuo), is_home (binario).
    Respuesta: goals_for.
    Link: log.
    """
    data = long_df.dropna(subset=['elo_diff', 'goals_for']).copy()
    data['goals_for'] = data['goals_for'].astype(int)
    X = sm.add_constant(data[['elo_diff', 'is_home']])
    y = data['goals_for']
    model = sm.GLM(y, X, family=sm.families.Poisson()).fit()
    return model


def predict_lambda(model: sm.GLMResults, elo_self: float, elo_opp: float, is_home: int = 0) -> float:
    """Predice goles esperados (λ) para un equipo dado el contexto."""
    X = np.array([[1, elo_self - elo_opp, is_home]])
    return float(model.predict(X)[0])


def match_probabilities(model: sm.GLMResults,
                        elo_home: float, elo_away: float,
                        neutral: bool = False,
                        max_goals: int = 8) -> dict:
    """Calcula probabilidades de victoria local/empate/visita y goles esperados.

    Asume goles del local y visitante como Poissons independientes.
    """
    from scipy.stats import poisson
    is_home_flag = 0 if neutral else 1

    lam_home = predict_lambda(model, elo_home, elo_away, is_home=is_home_flag)
    lam_away = predict_lambda(model, elo_away, elo_home, is_home=0)

    # Matriz de probabilidades [home_goals, away_goals]
    h = poisson.pmf(np.arange(max_goals + 1), lam_home)
    a = poisson.pmf(np.arange(max_goals + 1), lam_away)
    matrix = np.outer(h, a)

    p_home = np.tril(matrix, -1).sum()
    p_draw = np.trace(matrix)
    p_away = np.triu(matrix, 1).sum()

    return {
        'lambda_home': lam_home,
        'lambda_away': lam_away,
        'p_home_win': p_home,
        'p_draw': p_draw,
        'p_away_win': p_away,
    }
