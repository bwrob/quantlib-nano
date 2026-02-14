(
              ext::shared_ptr<StochasticProcess1D>(new OrnsteinUhlenbeckProcess(a, sigma))),
          fitting_(std::move(fitting)) {}

        Real variable(Time t, Rate r) const override { return r - fitting_(t); }
        Real shortRate(Time t, Real x) const override { return x + fitting_(t); }

      private:
        Parameter fitting_;
    };

    //! Analytical term-structure fitting parameter \f$ \varphi(t) \f$.
    /*! \f$ \varphi(t) \f$ is analytically defined by
        \f[
            \varphi(t) = f(t) + \frac{1}{2}[\frac{\sigma(1-e^{-at})}{a}]^2,
        \f]
        where \f$ f(t) \f$ is the instantaneous forward rate at \f$ t \f$.
    */
    class HullWhite::FittingParameter
        : public TermStructureFittingParameter {
      private:
        class Impl final : public Parameter::Impl {
          public:
            Impl(Handle<YieldTermStructure> termStructure, Real a, Real sigma)
            : termStructure_(std::move(termStructure)), a_(a), sigma_(sigma) {}

            Real value(const Array&, Time t) const override {
                Rate forwardRate =
                    termStructure_->forwardRate(t, t, Continuous, NoFrequency);
                Real temp = a_ < std::sqrt(QL_EPSILON) ?
                            Real(sigma_*t) :
                            Real(sigma_*(1.0 - std::exp(-a_*t))/a_);
                return (forwardRate + 0.5*temp*temp);
            }

          private:
            Handle<YieldTermStructure> termStructure_;
            Real a_, sigma_;
        };
      public:
        FittingParameter(const Handle<YieldTermStructure>& termStructure,
                         Real a, Real sigma)
        : TermStructureFittingParameter(ext::shared_ptr<Parameter::Impl>(
                      new FittingParameter::Impl(termStructure, a, sigma))) {}
    };


    // inline definitions

    inline ext::shared_ptr<OneFactorModel::ShortRateDynamics>
    HullWhite::dynamics() const {
        return ext::shared_ptr<ShortRateDynamics>(
                                            new Dynamics(phi_, a(), sigma()));
    }

}


#endif