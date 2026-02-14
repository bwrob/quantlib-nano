>value() >= -1
                       && correlation_->value() <= 1,
                       "correlation out of range [-1, +1]");
            registerWith(correlation_);
        }

        //! Density function of M.
        /*! Derived classes must override this method and ensure zero
            mean and unit variance.
        */
        virtual Real density(Real m) const = 0;
        //! Cumulative distribution of Z.
        /*! Derived classes must override this method and ensure zero
            mean and unit variance.
        */
        virtual Real cumulativeZ(Real z) const = 0;
        //! Cumulative distribution of Y.
        /*! This is the default implementation based on tabulated
            data. The table needs to be filled by derived classes. If
            analytic calculation is feasible, this method can also be
            overridden.
        */
        virtual Real cumulativeY(Real y) const;
        //! Inverse cumulative distribution of Y.
        /*! This is the default implementation based on tabulated
            data. The table needs to be filled by derived classes. If
            analytic calculation is feasible, this method can also be
            overridden.
        */
        virtual Real inverseCumulativeY(Real p) const;

        //! Single correlation parameter
        Real correlation() const;

        //! Conditional probability
        /*! \f[
            \hat p(m) = F_Z \left( \frac{F_Y^{-1}(p)-a\,m}{\sqrt{1-a^2}}\right)
            \f]
        */
        Real conditionalProbability(Real prob,
                                    Real m) const;

        //! Vector of conditional probabilities
        /*! \f[
            \hat p_i(m) = F_Z \left( \frac{F_Y^{-1}(p_i)-a\,m}{\sqrt{1-a^2}}
            \right)
            \f]
        */
        std::vector<Real> conditionalProbability(const std::vector<Real>& prob,
                                                 Real m) const;

        /*! Integral over the density \f$ \rho(m) \f$ of M and the conditional
            probability related to p:

            \f[
            \int_{-\infty}^\infty\,dm\,\rho(m)\,
            F_Z \left( \frac{F_Y^{-1}(p)-a\,m}{\sqrt{1-a^2}}\right)
            \f]
        */
        Real integral(Real p) const {
            QL_REQUIRE(p >= 0 && p <= 1, "probability p=" << p
                       << " out of range [0,1]");
            calculate();

            Real avg = 0;
            for (Size k = 0; k < steps(); k++) {
                Real pp = conditionalProbability(p, m(k));
                avg += pp * densitydm(k);
            }
            return avg;
        }

        /*! Integral over the density \f$ \rho(m) \f$ of M and a
            one-dimensional function \f$ f \f$ of conditional
            probabilities related to the input vector of probabilities p:

            \f[
            \int_{-\infty}^\infty\,dm\,\rho(m)\, f (\hat p_1, \hat p_2, \dots,
            \hat p_N), \qquad
            \hat p_i (m) = F_Z \left( \frac{F_Y^{-1}(p_i)-a\,m}{\sqrt{1-a^2}}
            \right)
            \f]
        */
        template <class F>
        Real integral(const F& f, std::vector<Real>& probabilities) const {
            calculate();

            Real avg = 0.0;
            for (Size i = 0; i < steps_; i++) {
                std::vector<Real> conditional
                    = conditionalProbability(probabilities, m(i));
                Real prob = f(conditional);
                avg += prob * densitydm(i);
            }
            return avg;
        }

        /*! Integral over the density \f$ \rho(m) \f$ of M and a
            multi-dimensional function \f$ f \f$ of conditional
            probabilities related to the input vector of probabilities p:

            \f[
            \int_{-\infty}^\infty\,dm\,\rho(m)\, f (\hat p_1, \hat p_2, \dots,
            \hat p_N), \qquad
            \hat p_i = F_Z \left( \frac{F_Y^{-1}(p_i)-a\,m}{\sqrt{1-a^2}}\right)
            \f]
        */
        template <class F>
        Dist
