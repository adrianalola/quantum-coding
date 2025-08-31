import json
import numpy as np
from azure.quantum import Workspace
from pulser_pasqal import PasqalCloud
from pulser import Sequence, Register, Pulse
from pulser.waveforms import RampWaveform, BlackmanWaveform

# --- Azure Quantum Workspace ---
workspace = Workspace(
    resource_id="/subscriptions/81ff920d-3cb3-4d4e-bc42-417fbf947ba2/resourceGroups/quantum-rg/providers/Microsoft.Quantum/Workspaces/quantum-workspace-adry",
    location="northeurope"
)

# --- Selección de dispositivo PASQAL ---
devices = PasqalCloud().fetch_available_devices()
QPU = devices["FRESNEL"]  # usamos FRESNEL para validar la secuencia
layout = QPU.pre_calibrated_layouts[0]

print(f"Layout '{layout.slug}' con {layout.number_of_traps} traps totales.")
trap_coords = layout.coords[:60]  # 60 primeros traps
reg = Register.from_coordinates(trap_coords, prefix="q")
print(f"Register creado con {len(reg.qubits)} qubits.")

# --- Secuencia mínima ---
seq = Sequence(reg, QPU)
seq.declare_channel("ch0", "rydberg_global")
amp_wf = BlackmanWaveform(1000, np.pi)
det_wf = RampWaveform(1000, -5.0, 5.0)
pulse  = Pulse(amp_wf, det_wf, 0.0)
seq.add(pulse, "ch0")

# --- Convertir a JSON para Azure ---
def to_input(seq):
    return json.dumps({"sequence_builder": json.loads(seq.to_abstract_repr())})
payload = to_input(seq)

# --- Seleccionar target EMULADOR (gratis) ---
matches = workspace.get_targets(name="pasqal.sim.emu-tn")
# Puede ser lista u objeto según la versión del SDK:
if isinstance(matches, list):
    if not matches:
        raise RuntimeError("No hay target 'pasqal.sim.emu-tn' en el workspace.")
    target = matches[0]
else:
    target = matches

print(f"Usando target: {getattr(target, 'name', str(target))}")

# --- Enviar job ---
job = target.submit(
    input_data=payload,
    input_data_format="pasqal.pulser.v1",
    output_data_format="pasqal.pulser-results.v1",
    name="Pulser Rabi demo (60q)",
    shots=20
)
print("Queued job:", job.id)
job.wait_until_completed()
print("State:", job.details.status)

# --- Guardar resultados ---
res = job.get_results()
with open("pasqal_results.json", "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2)
with open("pasqal_last_job.txt", "w", encoding="utf-8") as f:
    f.write(job.id)
print("Resultados guardados en pasqal_results.json")
print("Job ID guardado en pasqal_last_job.txt")
