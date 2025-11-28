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
    
   
    fig = plt.figure(figsize=(14, 7), dpi=100)
    fig.patch.set_facecolor('#ffffff')
    
   
    gs = fig.add_gridspec(2, 2, height_ratios=[3, 0.3], width_ratios=[1, 0.05], 
                          hspace=0.3, wspace=0.3, left=0.08, right=0.95, top=0.92, bottom=0.08)
    
    ax_main = fig.add_subplot(gs[0, 0])
    ax_main.set_facecolor('#f8f9fa')
    
    data = []
    colors_creyentes = ["#e74c3c", "#9b59b6"]  # Rojo y Púrpura para infectados
    colors_susceptibles = ["#3498db", "#f39c12"]  # Azul y Naranja para susceptibles
    
    max_i_value = 0
    picos_info = []
    
    for idx, (esc, color_crey, color_susc) in enumerate(zip(escenarios, colors_creyentes, colors_susceptibles)):
        S, I, R, t = solve_sir(N, I0, R0, b, esc["k"], t_max)
        
        
        pico_idx = np.argmax(I)
        pico_dia = t[pico_idx]
        pico_val = I[pico_idx]
        max_i_value = max(max_i_value, pico_val)
        picos_info.append((pico_dia, pico_val, color_crey, idx))
        
        
        ax_main.fill_between(t, 0, I, alpha=0.12, color=color_crey)
        
        
        ax_main.plot(t, I, color=color_crey, linewidth=3.5, 
                    label=f"Creyentes – {esc['label']}", zorder=3)
        
        
        ax_main.plot(t, S, color=color_susc, linewidth=2.2, linestyle="--", 
                    alpha=0.6, label=f"Susceptibles – {esc['label']}", zorder=2)
        
        
        ax_main.plot(pico_dia, pico_val, 'o', color=color_crey, markersize=9, zorder=4)
        
        data.append({"t": t, "I": I, "S": S, "label": esc["label"]})
    
    
    offset_y_factor = max_i_value * 0.15  
    for pico_dia, pico_val, color, idx in picos_info:
        
        if idx == 0:
            offset_x = 2.0
            offset_y = pico_val + max_i_value * 0.25
        else:
            offset_x = -2.5
            offset_y = pico_val - max_i_value * 0.22
        
        ax_main.annotate(f'Pico: {pico_val:.0f}\nDía {pico_dia:.1f}',
                        xy=(pico_dia, pico_val),
                        xytext=(pico_dia + offset_x, offset_y),
                        fontsize=11, weight='bold', color='#2c3e50',
                        bbox=dict(boxstyle='round,pad=0.7', facecolor='#ffffff', 
                                 edgecolor=color, linewidth=2.5, alpha=0.98),
                        arrowprops=dict(arrowstyle='->', color=color, lw=2.5, 
                                       connectionstyle="arc3,rad=0.3"),
                        zorder=5)
    
    
    ax_main.set_title("Propagación del Rumor: Comparación de Escenarios", 
                     fontsize=17, weight="bold", pad=15, color='#2c3e50')
    ax_main.set_xlabel("Tiempo (días)", fontsize=13, weight="bold", color='#2c3e50', labelpad=10)
    ax_main.set_ylabel("Número de Personas", fontsize=13, weight="bold", color='#2c3e50', labelpad=10)
    ax_main.grid(True, alpha=0.25, linestyle='--', linewidth=0.8, color='#95a5a6')
    ax_main.set_axisbelow(True)
    ax_main.spines['top'].set_visible(False)
    ax_main.spines['right'].set_visible(False)
    ax_main.spines['left'].set_color('#7f8c8d')
    ax_main.spines['bottom'].set_color('#7f8c8d')
    ax_main.spines['left'].set_linewidth(1.5)
    ax_main.spines['bottom'].set_linewidth(1.5)
    
    
    legend = ax_main.legend(loc="upper left", fontsize=11, frameon=True, 
                           shadow=True, fancybox=True, framealpha=0.97, 
                           edgecolor='#bdc3c7', title="Escenarios", title_fontsize=12)
    legend.get_frame().set_linewidth(1.5)
    
    ax_main.set_ylim(bottom=0, top=max_i_value * 1.25)
    ax_main.set_xlim(left=0, right=t_max)
    ax_main.tick_params(axis='both', which='major', labelsize=11, colors='#2c3e50')
    ax_legend = fig.add_subplot(gs[1, 0])
    ax_legend.axis('off')
    
    return fig, data