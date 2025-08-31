namespace Demo {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;

    operation RandomNBits(n : Int) : Result[] {
        mutable results = [];
        for _ in 1..n {
            use q = Qubit();
            H(q);
            let r = M(q);
            Reset(q);
            set results += [r];
        }
        return results;
    }
}
