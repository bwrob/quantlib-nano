beta() const { return coeffs().params_[1]; }
    Real nu() const { return coeffs().params_[2]; }
    Real rho() const { return coeffs().params_[3]; }
    Real rmsError() const { return coeffs().error_; }
    Real maxError() const { return coeffs().maxError_; }
    const std::vector<Real> &interpolationWeights() const {
        return coeffs().weights_;
    }
    EndCriteria::Type endCriteria() { return coeffs().XABREndCriteria_; }

  private:
    const detail::XABRCoeffHolder<detail::SABRSpecs>& coeffs() const {
        return *dynamic_cast<detail::XABRCoeffHolder<detail::SABRSpecs>*>(impl_.get());
    }
};

//! %SABR interpolation factory and traits
/*! \ingroup interpolations */
class SABR {
  public:
    SABR(Time t,
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
         const Size maxGuesses = 50,
         const Real shift = 0.0)
    : t_(t), forward_(forward), alpha_(alpha), beta_(beta), nu_(nu), rho_(rho),
      alphaIsFixed_(alphaIsFixed), betaIsFixed_(betaIsFixed), nuIsFixed_(nuIsFixed),
      rhoIsFixed_(rhoIsFixed), vegaWeighted_(vegaWeighted), endCriteria_(std::move(endCriteria)),
      optMethod_(std::move(optMethod)), errorAccept_(errorAccept), useMaxError_(useMaxError),
      maxGuesses_(maxGuesses), shift_(shift) {}
    template <class I1, class I2>
    Interpolation interpolate(const I1 &xBegin, const I1 &xEnd,
                              const I2 &yBegin) const {
        return SABRInterpolation(xBegin, xEnd, yBegin, t_, forward_, alpha_,
                                 beta_, nu_, rho_, alphaIsFixed_, betaIsFixed_,
                                 nuIsFixed_, rhoIsFixed_, vegaWeighted_,
                                 endCriteria_, optMethod_, errorAccept_,
                                 useMaxError_, maxGuesses_, shift_);
    }
    static const bool global = true;

  private:
    Time t_;
    Real forward_;
    Real alpha_, beta_, nu_, rho_;
    bool alphaIsFixed_, betaIsFixed_, nuIsFixed_, rhoIsFixed_;
    bool vegaWeighted_;
    const ext::shared_ptr<EndCriteria> endCriteria_;
    const ext::shared_ptr<OptimizationMethod> optMethod_;
    const Real errorAccept_;
    const bool useMaxError_;
    const Size maxGuesses_;
    const Real shift_;
};
}

#endif