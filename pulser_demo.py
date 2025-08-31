from pulser import Pulse, Sequence, Register
from pulser.devices import MockDevice
from pulser.waveforms import ConstantWaveform
from pulser_simulation import QutipEmulator  # 👈 API nueva

# 1) Registro con 2 qubits
reg = Register.from_coordinates([(0.0, 0.0), (5.0, 0.0)], prefix="q")

# 2) Secuencia sobre dispositivo simulado
seq = Sequence(reg, MockDevice)
seq.declare_channel("ch", "rydberg_global")

# 3) Pulso constante (duración en ns)
duration = 1000  # 1000 ns = 1 µs
amp_wf = ConstantWaveform(duration, 1.0)   # amplitud
det_wf = ConstantWaveform(duration, 0.0)   # detuning
pulse = Pulse(amp_wf, det_wf, 0.0)
seq.add(pulse, "ch")

print("Duración de la secuencia (ns):", seq.get_duration())

# 4) Simulación (amostrado automático)
emu = QutipEmulator.from_sequence(seq, sampling_rate=0.05)
res = emu.run()  # corre la emulación

# 5) Muestras de estado final (si están disponibles)
try:
    print("Muestras de estado final:", res.sample_final_state(N_samples=10))
except Exception as e:
    print("Nota:", e)
