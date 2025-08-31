namespace Demo {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Measurement;

    operation Random() : Result {
        use q = Qubit();
        H(q);
        let r = M(q);
        Reset(q);
        return r;
    }

    @EntryPoint()
    operation RandomNBits(n : Int) : Result[] {
        mutable results = [];
        for _ in 1..n {
            set results += [Random()];
        }
        return results;
    }
}
