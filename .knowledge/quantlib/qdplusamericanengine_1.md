Real K, Rate r, Rate q, Volatility vol, Time T) const override;

      private:
        template <class Solver>
        Real buildInSolver(
            const QdPlusBoundaryEvaluator& eval,
            Solver solver, Real S, Real strike, Size maxIter,
            Real guess = Null<Real>()) const;

        const Size interpolationPoints_;
        const SolverType solverType_;
        const Real eps_;
        const Size maxIter_;
    };
}

#endif