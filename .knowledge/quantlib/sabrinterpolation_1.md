01; }
    Real eps2() { return .9999; }
    Real dilationFactor() { return 0.001; }
    Array inverse(const Array &y, const std::vector<bool> &,
                  const std::vector<Real> &, const Real) {
        Array x(4);
        x[0] = y[0] < 25.0 + eps1() ? Real(std::sqrt(y[0] - eps1()))
                                    : Real((y[0] - eps1() + 25.0) / 10.0);
        // y_[1] = std::tan(M_PI*(x[1] - 0.5))/dilationFactor();
        x[1] = std::sqrt(-std::log(y[1]));
        x[2] = y[2] < 25.0 + eps1() ? Real(std::sqrt(y[2] - eps1()))
                                    : Real((y[2] - eps1() + 25.0) / 10.0);
        x[3] = std::asin(y[3] / eps2());
        return x;
    }
    Array direct(const Array &x, const std::vector<bool> &,
                 const std::vector<Real> &, const Real) {
        Array y(4);
        y[0] = std::fabs(x[0]) < 5.0 ? Real(x[0] * x[0] + eps1())
                                     : Real((10.0 * std::fabs(x[0]) - 25.0) + eps1());
        // y_[1] = std::atan(dilationFactor_*x[1])/M_PI + 0.5;
        y[1] = std::fabs(x[1]) < std::sqrt(-std::log(eps1()))
                   ? std::exp(-(x[1] * x[1]))
                   : eps1();
        y[2] = std::fabs(x[2]) < 5.0 ? Real(x[2] * x[2] + eps1())
                                     : Real((10.0 * std::fabs(x[2]) - 25.0) + eps1());
        y[3] = std::fabs(x[3]) < 2.5 * M_PI
                   ? Real(eps2() * std::sin(x[3]))
                   : Real(eps2() * (x[3] > 0.0 ? 1.0 : (-1.0)));
        return y;
    }
    Real weight(const Real strike, const Real forward, const Real stdDev,
                const std::vector<Real> &addParams) {
        return blackFormulaStdDevDerivative(strike, forward, stdDev, 1.0,
                                            addParams[0]);
    }
    typedef SABRWrapper type;
    ext::shared_ptr<type> instance(const Time t, const Real &forward,
                                     const std::vector<Real> &params,
                                     const std::vector<Real> &addParams) {
        return ext::make_shared<type>(t, forward, params, addParams);
    }
};
}

//! %SABR smile interpolation between discrete volatility points.
/*! \ingroup interpolations
    \warning See the Interpolation class for information about the
             required lifetime of the underlying data.
*/
class SABRInterpolation : public Interpolation {
  public:
    template <class I1, class I2>
    SABRInterpolation(const I1 &xBegin, // x = strikes
                      const I1 &xEnd,
                      const I2 &yBegin, // y = volatilities
                      Time t,           // option expiry
                      const Real &forward, Real alpha, Real beta, Real nu,
                      Real rho, bool alphaIsFixed, bool betaIsFixed,
                      bool nuIsFixed, bool rhoIsFixed, bool vegaWeighted = true,
                      const ext::shared_ptr<EndCriteria> &endCriteria =
                          ext::shared_ptr<EndCriteria>(),
                      const ext::shared_ptr<OptimizationMethod> &optMethod =
                          ext::shared_ptr<OptimizationMethod>(),
                      const Real errorAccept = 0.0020,
                      const bool useMaxError = false,
                      const Size maxGuesses = 50, const Real shift = 0.0,
                      const VolatilityType volatilityType = VolatilityType::ShiftedLognormal) {

        impl_ = ext::shared_ptr<Interpolation::Impl>(
            new detail::XABRInterpolationImpl<I1, I2, detail::SABRSpecs>(
                xBegin, xEnd, yBegin, t, forward,
                {alpha, beta, nu, rho},
                {alphaIsFixed, betaIsFixed, nuIsFixed, rhoIsFixed},
                vegaWeighted, endCriteria, optMethod, errorAccept, useMaxError,
                maxGuesses, {shift}, volatilityType));
    }
    Real expiry() const { return coeffs().t_; }
    Real forward() const { return coeffs().forward_; }
    Real alpha() const { return coeffs().params_[0]; }
    Real 