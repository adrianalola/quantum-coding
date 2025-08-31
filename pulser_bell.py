from pulser import Pulse, Sequence, Register
from pulser.devices import MockDevice
from pulser.waveforms import ConstantWaveform
from pulser_simulation import QutipEmulator
import numpy as np
import matplotlib.pyplot as plt

# --- Registro de 2 qubits ---
reg = Register.from_coordinates([(0.0, 0.0), (5.0, 0.0)], prefix="q")

# --- Secuencia en dispositivo virtual ---
seq = Sequence(reg, MockDevice)
seq.declare_channel("g", "rydberg_global")  # global
seq.declare_channel("l", "rydberg_local")   # local

def pulse_const(duration_ns, area):
    """Pulso con área (integral de la amplitud) = 'area' radianes."""
    amp = area / duration_ns
    return Pulse(ConstantWaveform(duration_ns, amp),
                 ConstantWaveform(duration_ns, 0.0),
                 phase=0.0)

# Parámetros
t = 1000   # ns (1 μs)
pi = np.pi

# Estado de Bell |Φ+> ≈ (|00> + |11>)/√2:
# 1) H ⊗ H aproximadas con π/2 global
seq.add(pulse_const(t, pi/2), "g")

# 2) "CZ" aproximada: dar 2π local a q1 (fase sobre |11>)
seq.target("q1", "l")
seq.add(pulse_const(t, 2*pi), "l")
# (No llamamos seq.target(None, "l"): no es necesario y puede fallar)

# 3) Otra π/2 global
seq.add(pulse_const(t, pi/2), "g")

# --- Emulación ---
emu = QutipEmulator.from_sequence(seq, sampling_rate=0.05)
res = emu.run()

# --- Muestreo / conteos ---
shots = 4000
counts = res.sample_final_state(N_samples=shots)  # Counter({...})
print("Cuentas:", counts)

# --- Gráfica de cuentas ---
labels = sorted(counts.keys())
vals = [counts.get(k, 0) for k in labels]
plt.figure(figsize=(6,4))
plt.bar(labels, vals)
plt.xlabel("Bitstring")
plt.ylabel("Cuentas")
plt.title(f"Estado de Bell |Φ+> – Cuentas (N={shots})")
plt.tight_layout()
plt.savefig("bell_counts.png")
plt.close()

# --- Probabilidades y gráfica ---
probs = {k: v/shots for k, v in counts.items()}
print("Probabilidades ordenadas:")
for k in labels:
    print(f"  {k}: {probs.get(k,0):.3f}")

plt.figure(figsize=(6,4))
plt.bar(labels, [probs.get(k,0) for k in labels])
plt.xlabel("Bitstring")
plt.ylabel("Probabilidad")
plt.title("Estado de Bell |Φ+> – Probabilidades")
plt.tight_layout()
plt.savefig("bell_probs.png")
plt.close()

print("Imágenes guardadas: bell_counts.png, bell_probs.png")
