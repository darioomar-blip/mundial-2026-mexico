"""
Simulador Montecarlo del Mundial 2026 (versión vectorizada).

Formato 2026: 48 equipos / 12 grupos de 4. Avanzan 2 primeros + 8 mejores
terceros = 32 a eliminación directa.

Diseño de rendimiento:
- Pre-computamos λ_home y λ_away para los 72 partidos de grupos
  (no cambian entre simulaciones).
- Cada simulación genera 144 goles (72 partidos × 2 equipos) en un solo
  np.random.poisson() vectorizado.
- Standings se computan con operaciones vectorizadas sobre matrices.
- Solo la fase de eliminación es loop Python (31 partidos), aceptable.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


HOST_COUNTRIES = {'United States', 'Mexico', 'Canada'}


def get_groups_from_fixture(fixture_2026: pd.DataFrame) -> dict[str, list[str]]:
    """Inferir los grupos: cada equipo juega contra los otros 3 de su grupo."""
    teams = set(fixture_2026['home_team']) | set(fixture_2026['away_team'])
    adj = {t: set() for t in teams}
    for _, row in fixture_2026.iterrows():
        adj[row['home_team']].add(row['away_team'])
        adj[row['away_team']].add(row['home_team'])

    groups = []
    used = set()
    for t in sorted(teams):
        if t in used:
            continue
        grupo = sorted(adj[t] | {t})
        if len(grupo) == 4:
            used.update(grupo)
            groups.append(grupo)
    return {chr(ord('A') + i): g for i, g in enumerate(groups)}


def _lambda(coef_const, coef_elo, coef_home, elo_self, elo_opp, is_home):
    return np.exp(coef_const + coef_elo * (elo_self - elo_opp) + coef_home * is_home)


def precompute_group_lambdas(fixture: pd.DataFrame, elos: dict, model):
    """Devuelve arrays (lam_h, lam_a, team_h_idx, team_a_idx) listos para
    simular vectorialmente."""
    coef_const = float(model.params['const'])
    coef_elo = float(model.params['elo_diff'])
    coef_home = float(model.params['is_home'])

    teams = sorted(set(fixture['home_team']) | set(fixture['away_team']))
    team_to_idx = {t: i for i, t in enumerate(teams)}
    n_teams = len(teams)

    elo_arr = np.array([elos.get(t, 1500) for t in teams])

    h_idx = fixture['home_team'].map(team_to_idx).values
    a_idx = fixture['away_team'].map(team_to_idx).values

    e_h = elo_arr[h_idx]
    e_a = elo_arr[a_idx]

    # is_home solo si el local pertenece a algún host AND el partido se juega en su país
    is_home_h = np.array([
        1 if (h in HOST_COUNTRIES and c == h) else 0
        for h, c in zip(fixture['home_team'], fixture['country'])
    ])
    is_home_a = np.array([
        1 if (a in HOST_COUNTRIES and c == a) else 0
        for a, c in zip(fixture['away_team'], fixture['country'])
    ])

    lam_h = _lambda(coef_const, coef_elo, coef_home, e_h, e_a, is_home_h)
    lam_a = _lambda(coef_const, coef_elo, coef_home, e_a, e_h, is_home_a)

    return {
        'teams': teams, 'team_to_idx': team_to_idx, 'elo_arr': elo_arr,
        'h_idx': h_idx, 'a_idx': a_idx,
        'lam_h': lam_h, 'lam_a': lam_a, 'n_teams': n_teams,
        'coef_const': coef_const, 'coef_elo': coef_elo, 'coef_home': coef_home,
    }


def simulate_group_phase_vectorized(pre: dict, rng: np.random.Generator):
    """Simula los 72 partidos de grupos en operaciones vectorizadas.

    Devuelve: matriz (n_teams, 4) con [played, points, gf, ga].
    """
    n_teams = pre['n_teams']
    goals_h = rng.poisson(pre['lam_h'])
    goals_a = rng.poisson(pre['lam_a'])

    points = np.zeros(n_teams, dtype=np.int32)
    gf = np.zeros(n_teams, dtype=np.int32)
    ga = np.zeros(n_teams, dtype=np.int32)
    played = np.zeros(n_teams, dtype=np.int32)

    h_idx = pre['h_idx']
    a_idx = pre['a_idx']

    np.add.at(played, h_idx, 1)
    np.add.at(played, a_idx, 1)
    np.add.at(gf, h_idx, goals_h)
    np.add.at(gf, a_idx, goals_a)
    np.add.at(ga, h_idx, goals_a)
    np.add.at(ga, a_idx, goals_h)

    home_wins = (goals_h > goals_a).astype(np.int32)
    away_wins = (goals_h < goals_a).astype(np.int32)
    draws = (goals_h == goals_a).astype(np.int32)

    np.add.at(points, h_idx, 3 * home_wins + draws)
    np.add.at(points, a_idx, 3 * away_wins + draws)

    return points, gf, ga, played


def rank_within_groups(points, gf, ga, groups, team_to_idx):
    """Devuelve rank_in_group para cada team (1-4) y points/gd/gf como tabla."""
    gd = gf - ga
    n_teams = len(points)
    rank = np.zeros(n_teams, dtype=np.int32)

    for letra, equipos in groups.items():
        idxs = np.array([team_to_idx[t] for t in equipos])
        # Ordenar por (-points, -gd, -gf)
        key = list(zip(-points[idxs], -gd[idxs], -gf[idxs]))
        order = sorted(range(len(idxs)), key=lambda i: key[i])
        for rk, slot in enumerate(order, start=1):
            rank[idxs[slot]] = rk

    return rank, gd


def select_top32_vec(points, gf, ga, rank, team_to_idx):
    """Top 32: 2 primeros de cada grupo + 8 mejores terceros."""
    n_teams = len(points)
    is_top2 = (rank <= 2)
    is_third = (rank == 3)

    # Idx de los terceros, ordenados por mejor performance
    third_idxs = np.where(is_third)[0]
    gd = gf - ga
    key = list(zip(-points[third_idxs], -gd[third_idxs], -gf[third_idxs]))
    order = sorted(range(len(third_idxs)), key=lambda i: key[i])
    best8_thirds = third_idxs[order[:8]]

    selected = np.concatenate([np.where(is_top2)[0], best8_thirds])
    return selected


def simulate_knockout_fast(top32_idxs, pre, rng):
    """Bracket #1 vs #32 sembrado por ELO. Todos los partidos neutrales.
    Devuelve dict idx → mejor fase alcanzada (índice en el array de fases)."""
    elo_arr = pre['elo_arr']
    coef_const = pre['coef_const']
    coef_elo = pre['coef_elo']
    coef_home = pre['coef_home']

    fases = ['Round of 16', 'Quarter-final', 'Semi-final', 'Final', 'Champion']

    # Sembrar por ELO descendente
    seeded = top32_idxs[np.argsort(-elo_arr[top32_idxs])]
    current = list(seeded)

    fase_alcanzada = {idx: 'Round of 32' for idx in current}
    fase_idx = 0

    while len(current) > 1:
        winners = []
        for i in range(len(current) // 2):
            a = current[i]
            b = current[-(i + 1)]
            ea, eb = elo_arr[a], elo_arr[b]
            lam_a = float(_lambda(coef_const, coef_elo, coef_home, ea, eb, 0))
            lam_b = float(_lambda(coef_const, coef_elo, coef_home, eb, ea, 0))
            ga = rng.poisson(lam_a)
            gb = rng.poisson(lam_b)
            if ga == gb:
                # Tiempo extra y penales: probabilidad por ELO
                ea_p = 1 / (1 + 10 ** ((eb - ea) / 400))
                winner = a if rng.random() < ea_p else b
            elif ga > gb:
                winner = a
            else:
                winner = b
            winners.append(winner)
            if fase_idx < len(fases):
                fase_alcanzada[winner] = fases[fase_idx]
        current = winners
        fase_idx += 1

    return fase_alcanzada


def run_tournament_fast(pre, groups, rng):
    """Una simulación completa. Devuelve dict idx → fase."""
    points, gf, ga, played = simulate_group_phase_vectorized(pre, rng)
    rank, _ = rank_within_groups(points, gf, ga, groups, pre['team_to_idx'])
    top32 = select_top32_vec(points, gf, ga, rank, pre['team_to_idx'])
    fase = simulate_knockout_fast(top32, pre, rng)
    # Equipos no en top32 → eliminados en grupos
    n = pre['n_teams']
    for idx in range(n):
        if idx not in fase:
            fase[idx] = 'Group'
    return fase


# Compatibilidad con código viejo
def run_tournament(fixture, groups, elos, model, rng):
    pre = precompute_group_lambdas(fixture, elos, model)
    fase_by_idx = run_tournament_fast(pre, groups, rng)
    idx_to_team = {i: t for t, i in pre['team_to_idx'].items()}
    return {idx_to_team[i]: f for i, f in fase_by_idx.items()}
