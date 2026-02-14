   return b_[u];
    }

    template <class mp_real> inline
    mp_real MomentBasedGaussianPolynomial<mp_real>::beta_(Size u) const {
        if (u == 0)
            return mp_real(1.0);

        if (c_.size() <= u)
            c_.resize(u+1, std::numeric_limits<mp_real>::quiet_NaN());

        if (std::isnan(c_[u])) {
            const Integer iu(u);
            const mp_real tmp = z(iu, iu) / z(iu-1, iu-1);
            c_[u] = tmp;
        }
        return c_[u];
    }

    template <> inline
    Real MomentBasedGaussianPolynomial<Real>::alpha(Size u) const {
        return alpha_(u);
    }

    template <class mp_real> inline
    Real MomentBasedGaussianPolynomial<mp_real>::alpha(Size u) const {
        return alpha_(u).template convert_to<Real>();
    }

    template <> inline
    Real MomentBasedGaussianPolynomial<Real>::beta(Size u) const {
        return beta_(u);
    }

    template <class mp_real> inline
    Real MomentBasedGaussianPolynomial<mp_real>::beta(Size u) const {
        mp_real b = beta_(u);
        return b.template convert_to<Real>();
    }

    template <> inline
    Real MomentBasedGaussianPolynomial<Real>::mu_0() const {
        const Real m0 = moment(0);
        QL_REQUIRE(close_enough(m0, 1.0), "zero moment must by one.");

        return moment(0);
    }

    template <class mp_real> inline
    Real MomentBasedGaussianPolynomial<mp_real>::mu_0() const {
        return moment(0).template convert_to<Real>();
    }
}

#endif
