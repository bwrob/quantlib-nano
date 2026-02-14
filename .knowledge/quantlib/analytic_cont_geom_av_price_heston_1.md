   // Equations (13)
        std::complex<Real> z1_f(const std::complex<Real>& s, const std::complex<Real>& w, Real T) const;
        std::complex<Real> z2_f(const std::complex<Real>& s, const std::complex<Real>& w, Real T) const;
        std::complex<Real> z3_f(const std::complex<Real>& s, const std::complex<Real>& w, Real T) const;
        std::complex<Real> z4_f(const std::complex<Real>& s, const std::complex<Real>& w) const;

        // Equations (19), (20)
        std::pair<std::complex<Real>, std::complex<Real> > F_F_tilde(
                                        const std::complex<Real>& z1,
                                        const std::complex<Real>& z2,
                                        const std::complex<Real>& z3,
                                        const std::complex<Real>& z4,
                                        Real tau,
                                        Size cutoff = 50) const;

        // Equation (21)
        std::complex<Real> f(const std::complex<Real>& z1,
                             const std::complex<Real>& z2,
                             const std::complex<Real>& z3,
                             const std::complex<Real>& z4,
                             int n,
                             Real tau) const;
    };
}


#endif
