import matplotlib.pyplot as plt
import numpy as np

plt.style.use("seaborn-v0_8-pastel")

def plot_sir(S, I, R, t, title="Dinámica SIR"):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(t, S, label="Susceptibles", color="blue")
    ax.plot(t, I, label="Infectados", color="red")
    ax.plot(t, R, label="Recuperados", color="green")
    ax.set_title(title, fontsize=14, weight="bold")
    ax.set_xlabel("Tiempo (días)", fontsize=12)
    ax.set_ylabel("Personas", fontsize=12)
    ax.legend()
    ax.grid(alpha=0.3)
    return fig


def plot_sir_profesional(S, I, R, t, title="Dinámica SIR Extendida"):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.fill_between(t, 0, S, alpha=0.3, color="#4c72b0", label="Susceptibles")
    ax.fill_between(t, 0, I, alpha=0.3, color="#c44e52", label="Infectados")
    ax.fill_between(t, 0, R, alpha=0.3, color="#55a868", label="Inmunes")
    ax.plot(t, S, color="#4c72b0", linewidth=2.2)
    ax.plot(t, I, color="#c44e52", linewidth=2.5)
    ax.plot(t, R, color="#55a868", linewidth=2.2)

    pico_dia = t[np.argmax(I)]
    pico_val = max(I)
    ax.annotate(f"Pico: {pico_val:.0f}", xy=(pico_dia, pico_val),
                xytext=(pico_dia + 1, pico_val + 50),
                arrowprops=dict(arrowstyle="->", color="black"),
                fontsize=10, weight="bold", color="darkred")

    ax.set_title(title, fontsize=14, weight="bold")
    ax.set_xlabel("Tiempo (días)", fontsize=12)
    ax.set_ylabel("Personas", fontsize=12)
    ax.legend(loc="best", frameon=True, shadow=True)
    ax.grid(alpha=0.25)
    for spine in ax.spines.values():
        spine.set_visible(False)
    return fig


def plot_sir_comparison(N, I0, R0, b, escenarios, t_max):
    from models.sir_model import solve_sir
    fig, ax = plt.subplots(figsize=(7, 4))
    data = []
    colors = ["#ff7f0e", "#2ca02c"]
    for esc, color in zip(escenarios, colors):
        S, I, R, t = solve_sir(N, I0, R0, b, esc["k"], t_max)
        ax.fill_between(t, 0, I, alpha=0.25, color=color)
        ax.plot(t, I, color=color, linewidth=2.5, label=f"I(t) – {esc['label']}")
        ax.plot(t, S, color=color, linestyle="--", linewidth=2, alpha=0.8)
        data.append({"t": t, "I": I, "S": S, "label": esc["label"]})

    ax.set_title("Propagación del rumor: comparación de escenarios", fontsize=14, weight="bold")
    ax.set_xlabel("Tiempo (días)", fontsize=12)
    ax.set_ylabel("Personas", fontsize=12)
    ax.legend(loc="best", frameon=True, shadow=True)
    ax.grid(alpha=0.25)
    for spine in ax.spines.values():
        spine.set_visible(False)
    return fig, data