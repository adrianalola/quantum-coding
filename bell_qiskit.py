from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

# Circuito Bell |Φ+> = (|00> + |11>)/√2
qc = QuantumCircuit(2, 2)
qc.h(0)         # Hadamard en q0
qc.cx(0, 1)     # CNOT de q0 a q1
qc.measure([0,1], [0,1])

# Simulador y ejecución
shots = 4000
sim = AerSimulator()
tcirc = transpile(qc, sim)
result = sim.run(tcirc, shots=shots).result()
counts = result.get_counts()

print("Cuentas:", counts)

# Histograma simple con matplotlib
labels = sorted(counts.keys())  # típicamente ['00','11']
values = [counts[k] for k in labels]

plt.figure(figsize=(6,4))
plt.bar(labels, values)
plt.title(f"Estado de Bell |Φ+> – Cuentas (N={shots})")
plt.xlabel("Bitstring")
plt.ylabel("Cuentas")
plt.tight_layout()
plt.show()

# Probabilidades por consola
print("Probabilidades:")
for k in labels:
    print(f"  {k}: {counts[k]/shots:.3f}")
