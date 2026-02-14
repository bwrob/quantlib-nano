s[2] *
                                  std::sqrt(1.0 - values[3] * values[3]));
    }
    Array inverse(const Array &y, const std::vector<bool> &,
                  const std::vector<Real> &, const Real) {
        Array x(5);
        x[2] = std::sqrt(y[2] - eps1());
        x[3] = std::asin(y[3] / eps2());
        x[4] = y[4];
        x[1] = std::tan(y[1] / 4.0 * (1.0 + std::fabs(y[3])) / eps2() * M_PI -
                        M_PI / 2.0);
        x[0] = std::sqrt(y[0] - eps1() +
                         y[1] * y[2] * std::sqrt(1.0 - y[3] * y[3]));
        return x;
    }
    Real eps1() { return 0.000001; }
    Real eps2() { return 0.999999; }
    Array direct(const Array &x, const std::vector<bool> &paramIsFixed,
                 const std::vector<Real> &params, const Real forward) {
        Array y(5);
        y[2] = x[2] * x[2] + eps1();
        y[3] = std::sin(x[3]) * eps2();
        y[4] = x[4];
        if (paramIsFixed[1])
            y[1] = params[1];
        else
            y[1] = (std::atan(x[1]) + M_PI / 2.0) / M_PI * eps2() * 4.0 /
                   (1.0 + std::fabs(y[3]));
        if (paramIsFixed[0])
            y[0] = params[0];
        else
            y[0] = eps1() + x[0] * x[0] -
                   y[1] * y[2] * std::sqrt(1.0 - y[3] * y[3]);
        return y;
    }
    Real weight(const Real strike, const Real forward, const Real stdDev,
                const std::vector<Real> &addParams) {
        return blackFormulaStdDevDerivative(strike, forward, stdDev, 1.0);
    }
    typedef SviWrapper type;
    ext::shared_ptr<type> instance(const Time t, const Real &forward,
                                     const std::vector<Real> &params,
                                     const std::vector<Real> &addParams) {
        return ext::make_shared<type>(t, forward, params);
    }
};
}

//! %Svi smile interpolation between discrete volatility points.
class SviInterpolation : public Interpolation {
  public:
    template <class I1, class I2>
    SviInterpolation(const I1 &xBegin, // x = strikes
                     const I1 &xEnd,
                     const I2 &yBegin, // y = volatilities
                     Time t,           // option expiry
                     const Real &forward, Real a, Real b, Real sigma, Real rho,
                     Real m, bool aIsFixed, bool bIsFixed, bool sigmaIsFixed,
                     bool rhoIsFixed, bool mIsFixed, bool vegaWeighted = true,
                     const ext::shared_ptr<EndCriteria> &endCriteria =
                         ext::shared_ptr<EndCriteria>(),
                     const ext::shared_ptr<OptimizationMethod> &optMethod =
                         ext::shared_ptr<OptimizationMethod>(),
                     const Real errorAccept = 0.0020,
                     const bool useMaxError = false,
                     const Size maxGuesses = 50) {

        impl_ = ext::shared_ptr<Interpolation::Impl>(
            new detail::XABRInterpolationImpl<I1, I2, detail::SviSpecs>(
                xBegin, xEnd, yBegin, t, forward,
                {a, b, sigma, rho, m},
                {aIsFixed, bIsFixed, sigmaIsFixed, rhoIsFixed, mIsFixed},
                vegaWeighted, endCriteria, optMethod, errorAccept, useMaxError,
                maxGuesses));
    }
    Real expiry() const { return coeffs().t_; }
    Real forward() const { return coeffs().forward_; }
    Real a() const { return coeffs().params_[0]; }
    Real b() const { return coeffs().params_[1]; }
    Real sigma() const { return coeffs().params_[2]; }
    Real rho() const { return coeffs().params_[3]; }
    Real m() const { return coeffs().params_[4]; }
    Real rmsError() const { return coeffs().error_; }
    Real maxError() const { return coeffs().maxError_; }
    const std::vector<Real> &interpolationWeights() const {
        return coeffs().weights_;
    }
    EndCriteria::Type endCriteria() { return coeffs().XABREndCriteria_; }

  private:
    const detail::XABRCoeffHolder<detail::SviSpecs>& coeffs() const {

