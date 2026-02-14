return y;
    }
    Real weight(const Real strike, const Real forward, const Real stdDev,
                const std::vector<Real> &addParams) {
        return blackFormulaStdDevDerivative(strike, forward, stdDev, 1.0);
    }
    typedef NoArbSabrWrapper type;
    ext::shared_ptr<type> instance(const Time t, const Real &forward,
                                     const std::vector<Real> &params,
                                     const std::vector<Real> &) {
        return ext::make_shared<type>(t, forward, params);
    }
};
}

//! no arbitrage sabr smile interpolation between discrete volatility points.
class NoArbSabrInterpolation : public Interpolation {
  public:
    template <class I1, class I2>
    NoArbSabrInterpolation(
        const I1 &xBegin, // x = strikes
        const I1 &xEnd,
        const I2 &yBegin, // y = volatilities
        Time t,           // option expiry
        const Real &forward, Real alpha, Real beta, Real nu, Real rho,
        bool alphaIsFixed, bool betaIsFixed, bool nuIsFixed, bool rhoIsFixed,
        bool vegaWeighted = true,
        const ext::shared_ptr<EndCriteria> &endCriteria =
            ext::shared_ptr<EndCriteria>(),
        const ext::shared_ptr<OptimizationMethod> &optMethod =
            ext::shared_ptr<OptimizationMethod>(),
        const Real errorAccept = 0.0020, const bool useMaxError = false,
        const Size maxGuesses = 50, const Real shift = 0.0) {

        QL_REQUIRE(shift==0.0,"NoArbSabrInterpolation for non zero shift not implemented");
        impl_ = ext::shared_ptr<Interpolation::Impl>(
            new detail::XABRInterpolationImpl<I1, I2, detail::NoArbSabrSpecs>(
                xBegin, xEnd, yBegin, t, forward,
                {alpha, beta, nu, rho},
                {alphaIsFixed, betaIsFixed, nuIsFixed, rhoIsFixed},
                vegaWeighted, endCriteria, optMethod, errorAccept, useMaxError,
                maxGuesses));
    }
    Real expiry() const { return coeffs().t_; }
    Real forward() const { return coeffs().forward_; }
    Real alpha() const { return coeffs().params_[0]; }
    Real beta() const { return coeffs().params_[1]; }
    Real nu() const { return coeffs().params_[2]; }
    Real rho() const { return coeffs().params_[3]; }
    Real rmsError() const { return coeffs().error_; }
    Real maxError() const { return coeffs().maxError_; }
    const std::vector<Real> &interpolationWeights() const {
        return coeffs().weights_;
    }
    EndCriteria::Type endCriteria() { return coeffs().XABREndCriteria_; }

  private:
    const detail::XABRCoeffHolder<detail::NoArbSabrSpecs>& coeffs() const {
        return *dynamic_cast<detail::XABRCoeffHolder<detail::NoArbSabrSpecs>*>(impl_.get());
    }
};

//! no arbtrage sabr interpolation factory and traits
class NoArbSabr {
  public:
    NoArbSabr(Time t,
              Real forward,
              Real alpha,
              Real beta,
              Real nu,
              Real rho,
              bool alphaIsFixed,
              bool betaIsFixed,
              bool nuIsFixed,
              bool rhoIsFixed,
              bool vegaWeighted = false,
              ext::shared_ptr<EndCriteria> endCriteria = ext::shared_ptr<EndCriteria>(),
              ext::shared_ptr<OptimizationMethod> optMethod = ext::shared_ptr<OptimizationMethod>(),
              const Real errorAccept = 0.0020,
              const bool useMaxError = false,
              const Size maxGuesses = 50)
    : t_(t), forward_(forward), alpha_(alpha), beta_(beta), nu_(nu), rho_(rho),
      alphaIsFixed_(alphaIsFixed), betaIsFixed_(betaIsFixed), nuIsFixed_(nuIsFixed),
      rhoIsFixed_(rhoIsFixed), vegaWeighted_(vegaWeighted), endCriteria_(std::move(endCriteria)),
      optMethod_(std::move(optMethod)), errorAccept_(errorAccept), useMaxError_(useMaxError),
      maxGuesses_(maxGuesses) {}
    template <class I1, class I2>
    Interpolation interpolate(const I1 &xBegin, const I1 &xEnd,
                              const I2 &yBegin) const {
        retu