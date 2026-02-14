e Real GaussianQuadMultidimIntegrator::integrate<Real>(
        const std::function<Real (const std::vector<Real>& v1)>& f) const 
    {
        // integration variables
        // call vector quadrature integration with the function and start 
        // values, kicks in recursion over the dimensions of the integration
        // variable.
        return integral_([&](Real x){ return integrationEntries_[dimension_-1](std::cref(f), x); });
    }

    // Vector integrand version
    template<>
    inline std::vector<Real> GaussianQuadMultidimIntegrator::integrate<std::vector<Real>>(
        const std::function<std::vector<Real> (const std::vector<Real>& v1)>& f) const
    {
        return integralV_([&](Real x){ return integrationEntriesVR_[dimension_-1](std::cref(f), x); });
    } 

    //! Terminal integrand; scalar function version
    template<> 
    inline Real GaussianQuadMultidimIntegrator::scalarIntegrator<1>(
        const std::function<Real (const std::vector<Real>& arg1)>& f,
        const Real mFctr) const
    {
        varBuffer_[0] = mFctr;
        return f(varBuffer_);
    }

    //! Terminal integrand; vector function version
    template<>
    inline std::vector<Real>
        GaussianQuadMultidimIntegrator::vectorIntegratorVR<1>(
        const std::function<std::vector<Real> (const std::vector<Real>& arg1)>& f,
        const Real mFctr) const 
    {
        varBuffer_[0] = mFctr;
        return f(varBuffer_);
    }

    //! Terminal level:
    template<>
    inline void GaussianQuadMultidimIntegrator::spawnFcts<1>() const {
        integrationEntries_[0] = [&](const std::function<Real(const std::vector<Real>&)>& f,
                                     Real x) { return scalarIntegrator<1>(f, x); };
        integrationEntriesVR_[0] =
            [&](const std::function<std::vector<Real>(const std::vector<Real>&)>& f, Real x) {
                return vectorIntegratorVR<1>(f, x);
            };
    }

}

#endif

#endif