import numpy as np
from scipy.integrate import solve_ivp

# ---------- MODELO SIR CLÁSICO ----------
def solve_sir(N, I0, R0, beta, k, t_max):
    S0 = N - I0 - R0
    def deriv(t, y):
        S, I, R = y
        dSdt = -beta * S * I
        dIdt = beta * S * I - k * I
        dRdt = k * I
        return [dSdt, dIdt, dRdt]
    sol = solve_ivp(deriv, [0, t_max], [S0, I0, R0], t_eval=np.linspace(0, t_max, 1000))
    return sol.y[0], sol.y[1], sol.y[2], sol.t

# ---------- MODELO SIR EXTENDIDO----------
def solve_sir_extended(N, I0, R0, beta, gamma, alpha, t_max):
    S0 = N - I0 - R0
    def deriv(t, y):
        S, I, R = y
        dSdt = -beta * S * I - alpha * S
        dIdt = beta * S * I - gamma * I
        dRdt = gamma * I + alpha * S
        return [dSdt, dIdt, dRdt]
    sol = solve_ivp(deriv, [0, t_max], [S0, I0, R0], t_eval=np.linspace(0, t_max, 1000))
    return sol.y[0], sol.y[1], sol.y[2], sol.t