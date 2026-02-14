ward rate at \f$ t \f$
        and \f$ h = \sqrt{k^2 + 2\sigma^2} \f$.
    */
    class ExtendedCoxIngersollRoss::FittingParameter
        : public TermStructureFittingParameter {
      private:
        class Impl final : public Parameter::Impl {
          public:
            Impl(Handle<YieldTermStructure> termStructure, Real theta, Real k, Real sigma, Real x0)
            : termStructure_(std::move(termStructure)), theta_(theta), k_(k), sigma_(sigma),
              x0_(x0) {}

            Real value(const Array&, Time t) const override {
                Rate forwardRate =
                    termStructure_->forwardRate(t, t, Continuous, NoFrequency);
                Real h = std::sqrt(k_*k_ + 2.0*sigma_*sigma_);
                Real expth = std::exp(t*h);
                Real temp = 2.0*h + (k_+h)*(expth-1.0);
                Real phi = forwardRate -
                    2.0*k_*theta_*(expth - 1.0)/temp -
                    x0_*4.0*h*h*expth/(temp*temp);
                return phi;
            }

          private:
            Handle<YieldTermStructure> termStructure_;
            Real theta_, k_, sigma_, x0_;
        };
      public:
        FittingParameter(const Handle<YieldTermStructure>& termStructure,
                         Real theta, Real k, Real sigma, Real x0)
        : TermStructureFittingParameter(ext::shared_ptr<Parameter::Impl>(
                 new FittingParameter::Impl(
                                     termStructure, theta, k, sigma, x0))) {}
    };

    // inline definitions

    inline ext::shared_ptr<OneFactorModel::ShortRateDynamics>
    ExtendedCoxIngersollRoss::dynamics() const {
        return ext::shared_ptr<ShortRateDynamics>(
                            new Dynamics(phi_, theta(), k() , sigma(), x0()));
    }

    inline void ExtendedCoxIngersollRoss::generateArguments() {
        phi_ = FittingParameter(termStructure(), theta(), k(), sigma(), x0());
    }

}


#endif
