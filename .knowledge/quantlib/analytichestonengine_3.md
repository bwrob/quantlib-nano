;
        Real alphaMin(Real strike) const;
        Real alphaMax(Real strike) const;

      private:
        std::pair<Real, Real> findMinima(Real lower, Real upper, Real strike) const;

        const Real t_, fwd_, kappa_, theta_, sigma_, rho_;

        const Real eps_;

        const AnalyticHestonEngine* const enginePtr_;
        Real km_, kp_;
        mutable Size evaluations_ = 0;
    };


    inline std::complex<Real> AnalyticHestonEngine::addOnTerm(
        Real, Time, Size) const {
        return std::complex<Real>(0,0);
    }
}

#endif