import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Lotka–Volterra", layout="centered")

DEFAULTS = {
    "alpha": 0.6,
    "beta": 0.02,
    "delta": 0.01,
    "gamma": 0.4,
    "x0": 40.0,
    "y0": 9.0,
    "T": 60.0,
}

if "params" not in st.session_state:
    st.session_state.params = DEFAULTS.copy()

def reset():
    st.session_state.params = DEFAULTS.copy()

st.title("Lotka–Volterra: Astrophage och Taumoeba")

st.markdown("""
**Astrophage** = bytesdjur  
**Taumoeba** = rovdjur
""")

st.button("Återställ värden", on_click=reset)

p = st.session_state.params

alpha = st.slider("α – Astrophage växer", 0.0, 2.0, p["alpha"], 0.01)
beta = st.slider("β – Taumoeba äter Astrophage", 0.0, 0.10, p["beta"], 0.001)
delta = st.slider("δ – Taumoeba växer av mat", 0.0, 0.10, p["delta"], 0.001)
gamma = st.slider("γ – Taumoeba dör utan mat", 0.0, 2.0, p["gamma"], 0.01)

x0 = st.slider("Startvärde Astrophage", 1.0, 200.0, p["x0"], 1.0)
y0 = st.slider("Startvärde Taumoeba", 1.0, 100.0, p["y0"], 1.0)
T = st.slider("Tid", 10.0, 200.0, p["T"], 1.0)

dt = 0.01
n = int(T / dt)

x = x0
y = y0

xs = []
ys = []
ts = []

for i in range(n):
    t = i * dt

    dx = alpha * x - beta * x * y
    dy = delta * x * y - gamma * y

    x = x + dx * dt
    y = y + dy * dt

    x = max(x, 0)
    y = max(y, 0)

    ts.append(t)
    xs.append(x)
    ys.append(y)
# Jämvikt
if beta > 0 and delta > 0:
    jämvikt_x = gamma / delta
    jämvikt_y = alpha / beta
else:
    jämvikt_x = None
    jämvikt_y = None

st.markdown("### Jämviktsläge")
if jämvikt_x is not None:
    st.write(f"Bytesdjur: {jämvikt_x:.2f}")
    st.write(f"Rovdjur: {jämvikt_y:.2f}")
else:
    st.warning("Kan inte beräkna jämvikt (beta eller delta = 0)")
# Grafikon
fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(ts, xs, label="Astrophage")
ax.plot(ts, ys, label="Taumoeba")

# Egyensúlyi vonalak
if jämvikt_x is not None:
    ax.axhline(y=jämvikt_x, linestyle="--", label="Jämvikt Astrophage")

if jämvikt_y is not None:
    ax.axhline(y=jämvikt_y, linestyle="--", label="Jämvikt Taumoeba")

ax.set_xlabel("Tid")
ax.set_ylabel("Population")
ax.set_title("Lotka–Volterra-modell")
ax.legend()
ax.grid(True)

st.pyplot(fig)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(ts, xs, label="Astrophage")
ax.plot(ts, ys, label="Taumoeba")
ax.set_xlabel("Tid")
ax.set_ylabel("Population")
ax.set_title("Lotka–Volterra-modell")
ax.legend()
ax.grid(True)

st.pyplot(fig)

st.markdown("### Ekvationerna")

st.latex(r"""
\begin{cases}
x' = \alpha x - \beta xy \\
y' = \delta xy - \gamma y
\end{cases}
""")

st.markdown("""
### Tolkning

- Om **α ökar** växer Astrophage snabbare.
- Om **β ökar** äter Taumoeba effektivare.
- Om **δ ökar** växer Taumoeba snabbare när den får mat.
- Om **γ ökar** dör Taumoeba snabbare utan mat.
""")
