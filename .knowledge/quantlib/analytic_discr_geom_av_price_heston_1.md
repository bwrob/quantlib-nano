 signatures, we
        // make them mutable class properties instead.
        mutable Real tr_t_;
        mutable Real Tr_T_;
        mutable std::vector<Real> tkr_tk_;

        // Equation (11)
        std::complex<Real> F(const std::complex<Real>& z1,
                             const std::complex<Real>& z2,
                             Time tau) const;

        std::complex<Real> F_tilde(const std::complex<Real>& z1,
                                   const std::complex<Real>& z2,
                                   Time tau) const;

        // Equation (14)
        std::complex<Real> z(const std::complex<Real>& s,
                             const std::complex<Real>& w,
                             Size k, Size n) const;

        // Equation (15)
        std::complex<Real> omega(const std::complex<Real>& s,
                                 const std::complex<Real>& w,
                                 Size k, Size kStar, Size n) const;

        // Equation (16)
        std::complex<Real> a(const std::complex<Real>& s,
                             const std::complex<Real>& w,
                             Time t, Time T, Size kStar,
                             const std::vector<Time>& t_n) const;

        // Equation (19)
        std::complex<Real> omega_tilde(const std::complex<Real>& s,
                                       const std::complex<Real>& w,
                                       Size k, Size kStar, Size n,
                                       const std::vector<Time>& tauK) const;
    };
}


#endif
