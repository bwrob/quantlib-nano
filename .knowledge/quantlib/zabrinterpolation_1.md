               : Real(eps2() * (x[3] > 0.0 ? 1.0 : (-1.0)));
        // limit gamma to 1.9
        y[4] = (std::atan(x[4])/M_PI + 0.5) * 1.9;
        return y;
    }
    Real weight(const Real strike, const Real forward, const Real stdDev,
                const std::vector<Real> &addParams) {
        return blackFormulaStdDevDerivative(strike, forward, stdDev, 1.0);
    }
    typedef ZabrSmileSection<Evaluation> type;
    ext::shared_ptr<type> instance(const Time t, const Real &forward,
                                     const std::vector<Real> &params,
                                     const std::vector<Real> &addParams) {
        return ext::make_shared<type>(t, forward, params);
    }
};
} // end namespace detail


//! zabr smile interpolation between discrete volatility points.
template <class Evaluation> class ZabrInterpolation : public Interpolation {
  public:
    template <class I1, class I2>
    ZabrInterpolation(
        const I1 &xBegin, // x = strikes
        const I1 &xEnd,
        const I2 &yBegin, // y = volatilities
        Time t,           // option expiry
        const Real &forward, Real alpha, Real beta, Real nu, Real rho,
        Real gamma, bool alphaIsFixed, bool betaIsFixed, bool nuIsFixed,
        bool rhoIsFixed, bool gammaIsFixed, bool vegaWeighted = true,
        const ext::shared_ptr<EndCriteria> &endCriteria =
            ext::shared_ptr<EndCriteria>(),
        const ext::shared_ptr<OptimizationMethod> &optMethod =
            ext::shared_ptr<OptimizationMethod>(),
        const Real errorAccept = 0.0020, const bool useMaxError = false,
        const Size maxGuesses = 50) {
            impl_ = ext::shared_ptr<
                Interpolation::Impl>(new detail::XABRInterpolationImpl<
                I1, I2,
                detail::ZabrSpecs<Evaluation> >(
                xBegin, xEnd, yBegin, t, forward,
                {alpha, beta, nu, rho, gamma},
                {alphaIsFixed, betaIsFixed, nuIsFixed, rhoIsFixed, gammaIsFixed},
                vegaWeighted, endCriteria, optMethod, errorAccept, useMaxError,
                maxGuesses));
    }
    Real expiry() const { return coeffs().t_; }
    Real forward() const { return coeffs().forward_; }
    Real alpha() const { return coeffs().params_[0]; }
    Real beta() const { return coeffs().params_[1]; }
    Real nu() const { return coeffs().params_[2]; }
    Real rho() const { return coeffs().params_[3]; }
    Real gamma() const { return coeffs().params_[4]; }
    Real rmsError() const { return coeffs().error_; }
    Real maxError() const { return coeffs().maxError_; }
    const std::vector<Real> &interpolationWeights() const {
        return coeffs().weights_;
    }
    EndCriteria::Type endCriteria() { return coeffs().XABREndCriteria_; }

  private:
    const detail::XABRCoeffHolder<detail::ZabrSpecs<Evaluation>>& coeffs() const {
        return *dynamic_cast<detail::XABRCoeffHolder<detail::ZabrSpecs<Evaluation>>*>(impl_.get());
    }
};

//! no arbtrage sabr interpolation factory and traits
template<class Evaluation> class Zabr {
  public:
    Zabr(Time t,
         Real forward,
         Real alpha,
         Real beta,
         Real nu,
         Real rho,
         Real gamma,
         bool alphaIsFixed,
         bool betaIsFixed,
         bool nuIsFixed,
         bool rhoIsFixed,
         bool gammaIsFixed,
         bool vegaWeighted = false,
         ext::shared_ptr<EndCriteria> endCriteria = ext::shared_ptr<EndCriteria>(),
         ext::shared_ptr<OptimizationMethod> optMethod = ext::shared_ptr<OptimizationMethod>(),
         const Real errorAccept = 0.0020,
         const bool useMaxError = false,
         const Size maxGuesses = 50)
    : t_(t), forward_(forward), alpha_(alpha), beta_(beta), nu_(nu), rho_(rho),
      alphaIsFixed_(alphaIsFixed), betaIsFixed_(betaIsFixed), nuIsFixed_(nuIsFixed),
      rhoIsFixed_(rhoIsFixed), gammaIsFixed_(gammaIsFixed), vegaWeighted_(vegaWeighted),
      endCriteria_(std::move(endCriteria)), optMethod_(st