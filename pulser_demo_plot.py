from pulser import Pulse, Sequence, Register
from pulser.devices import MockDevice
from pulser.waveforms import ConstantWaveform
from pulser_simulation import QutipEmulator

import matplotlib.pyplot as plt

# --- Misma secuencia que el demo ---
reg = Register.from_coordinates([(0.0, 0.0), (5.0, 0.0)], prefix="q")
seq = Sequence(reg, MockDevice)
seq.declare_channel("ch", "rydberg_global")

duration = 1000  # ns
amp_wf = ConstantWaveform(duration, 1.0)
det_wf = ConstantWaveform(duration, 0.0)
seq.add(Pulse(amp_wf, det_wf, 0.0), "ch")

# 1) Dibuja la línea de tiempo de la secuencia (útil para ver el pulso)
print("Mostrando la línea de tiempo de la secuencia…")
seq.draw()  # abre una figura con el pulso

# 2) Corre emulación y arma histograma de bitstrings
emu = QutipEmulator.from_sequence(seq, sampling_rate=0.05)
res = emu.run()

shots = 2000
counts = res.sample_final_state(N_samples=shots)  # Counter({'00':..., '01':..., ...})

# Ordena las keys para que el eje sea estable
keys = sorted(counts.keys())
vals = [counts[k] for k in keys]

plt.figure()
plt.bar(keys, vals)
plt.title(f"Distribución de resultados (N={shots})")
plt.xlabel("Bitstring")
plt.ylabel("Cuentas")
plt.tight_layout()
plt.show()
