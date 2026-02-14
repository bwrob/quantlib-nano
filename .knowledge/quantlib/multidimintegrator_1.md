f the 
         template argument restriction to be constant known at compilation.
        */
        mutable std::vector<std::function<Real (//<- members: integrate<N>
            // integrable function:
            const std::function<Real (const std::vector<Real>&)>&, 
            const std::vector<Real>&, //<- a
            const std::vector<Real>&) //<- b
            > > 
            integrationLevelEntries_;

        /* One can avoid the passing around of the ct refs to a and b but the 
        price is to keep a copy of them (they are unknown at construction time)
         On the other hand the vector integration variable has to be created.*/
        mutable std::vector<Real> varBuffer_;

    };

    // spez last call/dimension
    template<>
    Real inline MultidimIntegral::vectorBinder<0> (
        const std::function<Real (const std::vector<Real>&)>& f, 
        Real z,
        const std::vector<Real>& a,
        const std::vector<Real>& b) const
    {
        varBuffer_[0] = z;
        return f(varBuffer_);
    }

    template<>
    void inline MultidimIntegral::spawnFcts<1>() const {
        integrationLevelEntries_[0] = [this](const auto& f, const auto& a, const auto& b) {
            return this->integrate<0>(f, a, b);
        };
    }

    template<int nT>
    inline Real MultidimIntegral::integrate(
        const std::function<Real (const std::vector<Real>&)>& f,
        const std::vector<Real>& a,
        const std::vector<Real>& b) const 
    {
        return 
            (*integrators_[nT])([this, &f, &a, &b](auto z) {
                return this->vectorBinder<nT>(f, z, a, b);
            }, a[nT], b[nT]);
    }

    template<int T_N> 
    inline Real MultidimIntegral::vectorBinder (
        const std::function<Real (const std::vector<Real>&)>& f,
        Real z,
        const std::vector<Real>& a,
        const std::vector<Real>& b) const 
    {
        varBuffer_[T_N] = z;
        return integrate<T_N-1>(f, a, b);
    }

    template<Size depth>
    void MultidimIntegral::spawnFcts() const {
        integrationLevelEntries_[depth-1] = [this](const auto& f, const auto& a, const auto& b) {
            return this->integrate<depth-1>(f, a, b);
        };
        spawnFcts<depth-1>();
    }

}

#endif