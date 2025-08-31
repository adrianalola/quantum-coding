import qsharp
qsharp.init(target_profile=qsharp.TargetProfile.Base)

from qsharp import compile as qcompile

# Compilar Q# inline SIN 'namespace' y con nombres completos
RandomNBits = qcompile("""
operation RandomNBits(n : Int) : Result[] {
    mutable results = [];
    for _ in 1..n {
        use q = Qubit();
        Microsoft.Quantum.Intrinsic.H(q);
        let r = Microsoft.Quantum.Measurement.M(q);
        Microsoft.Quantum.Intrinsic.Reset(q);
        set results += [r];
    }
    return results;
}
""")

print("Random bits:", RandomNBits.simulate(n=8))
