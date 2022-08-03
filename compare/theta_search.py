"""
Uses a simple search to find the best theta that maximises TTR and minimises FTR

TODO: Figure out other ways that balance TTR & FTR based on precision/recall requirements
"""

import numpy as np
from utils import load_json
from score import true_target_rate, false_target_rate

SCOREBOARD_PATH = "temp_save/scoreboard.json"
CUTOFF_VALUE = 0.1
SCORING_TYPE = "minus"

def calculate_ttr_ftr_using_theta(theta, scoreboard):
    # Nt: number of probe tracks from target people
    # Nt2t: number of correctly verified probe tracks of target people
    Nt = len(scoreboard['Same'])
    Nt2t = len([i for i in scoreboard['Same'] if i <= theta])
    ttr = true_target_rate(Nt2t, Nt)

    # Nnt: number of probe tracks from non-target people
    # Nnt2t: number of probe tracks of non-targets but verified as targets
    Nnt = len(scoreboard['Different'])
    Nnt2t = len([i for i in scoreboard['Different'] if i <= theta])
    ftr = false_target_rate(Nnt2t, Nnt)

    return ttr, ftr

def calculate_scores(prev_best_theta, prev_score, thetas, scoreboard, scoring_type, cutoff):
    scores = []
    for t_theta in thetas:
        ttr, ftr = calculate_ttr_ftr_using_theta(
            t_theta,
            scoreboard)
        if scoring_type == "minus":
            scores.append(ttr - ftr)
        elif scoring_type == "penalise_ftr":
            scores.append(ttr - ftr*2)
    best_score = max(scores)
    bs_index = scores.index(best_score)
    best_theta = thetas[bs_index]
    if best_score == 1.0:
        return best_score, best_theta
    elif prev_score > best_score:
        return prev_score, prev_best_theta
    elif prev_score - cutoff < best_score < prev_score + cutoff:
        return best_score, best_theta
    if bs_index != 0 and bs_index != len(scores):
        new_thetas = np.linspace(thetas[bs_index - 1], thetas[bs_index + 1], 8).tolist()
        return calculate_scores(
            best_theta,
            best_score,
            new_thetas,
            scoreboard,
            scoring_type,
            cutoff)
    else:
        return best_score, best_theta

def theta_split(
    scoreboard_path,
    scoring_type = "minus",
    cutoff = 0.1
    ):
    scoreboard = load_json(scoreboard_path)

    theta_lower_bound = min(min(scoreboard['Same']),
                            min(scoreboard['Different']))
    theta_upper_bound = max(max(scoreboard['Same']),
                            max(scoreboard['Different']))

    test_thetas = np.linspace(
        theta_lower_bound,
        theta_upper_bound,
        8).tolist()

    best_score, best_theta = calculate_scores(
        0,
        0,
        test_thetas,
        scoreboard,
        scoring_type,
        cutoff)

    ttr, ftr = calculate_ttr_ftr_using_theta(best_theta, scoreboard)

    return best_theta, best_score, ttr, ftr

if __name__ == "__main__":
    ## To run separately from main.py

    best_theta, best_score, ttr, ftr = theta_split(
        SCOREBOARD_PATH,
        SCORING_TYPE,
        CUTOFF_VALUE)

    print("Best theta: ", best_theta)
    print("Best score: ", best_score)
    print("TTR: ", ttr)
    print("FTR: ", ftr)
