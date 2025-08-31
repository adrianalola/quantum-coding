from pulser import Pulse, Sequence, Register
from pulser.devices import MockDevice
from pulser.waveforms import ConstantWaveform
from pulser_simulation import QutipEmulator
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def pulse_const(duration_ns, area):
    amp = area / duration_ns
    return Pulse(ConstantWaveform(duration_ns, amp),
                 ConstantWaveform(duration_ns, 0.0),
                 phase=0.0)

reg = Register.from_coordinates([(0.0, 0.0), (5.0, 0.0)], prefix="q")
seq = Sequence(reg, MockDevice)
seq.declare_channel("g", "rydberg_global")
seq.declare_channel("l", "rydberg_local")

t = 1000
pi = np.pi

seq.add(pulse_const(t, pi/2), "g")
seq.target("q1", "l")
seq.add(pulse_const(t, 2*pi), "l")
seq.add(pulse_const(t, pi/2), "g")

emu = QutipEmulator.from_sequence(seq, sampling_rate=0.05)
res = emu.run()

shots = 4000
counts = res.sample_final_state(N_samples=shots)
labels = sorted(counts.keys())
vals = [counts.get(k, 0) for k in labels]

plt.figure()
plt.bar(labels, vals)
plt.title(f"Bell state (aprox) – Cuentas (N={shots})")
plt.xlabel("Bitstring")
plt.ylabel("Cuentas")
plt.tight_layout()
plt.show()
