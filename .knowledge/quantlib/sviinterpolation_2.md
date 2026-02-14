     return *dynamic_cast<detail::XABRCoeffHolder<detail::SviSpecs>*>(impl_.get());
    }
};

//! %Svi interpolation factory and traits
class Svi {
  public:
    Svi(Time t,
        Real forward,
        Real a,
        Real b,
        Real sigma,
        Real rho,
        Real m,
        bool aIsFixed,
        bool bIsFixed,
        bool sigmaIsFixed,
        bool rhoIsFixed,
        bool mIsFixed,
        bool vegaWeighted = false,
        ext::shared_ptr<EndCriteria> endCriteria = ext::shared_ptr<EndCriteria>(),
        ext::shared_ptr<OptimizationMethod> optMethod = ext::shared_ptr<OptimizationMethod>(),
        const Real errorAccept = 0.0020,
        const bool useMaxError = false,
        const Size maxGuesses = 50)
    : t_(t), forward_(forward), a_(a), b_(b), sigma_(sigma), rho_(rho), m_(m), aIsFixed_(aIsFixed),
      bIsFixed_(bIsFixed), sigmaIsFixed_(sigmaIsFixed), rhoIsFixed_(rhoIsFixed),
      mIsFixed_(mIsFixed), vegaWeighted_(vegaWeighted), endCriteria_(std::move(endCriteria)),
      optMethod_(std::move(optMethod)), errorAccept_(errorAccept), useMaxError_(useMaxError),
      maxGuesses_(maxGuesses) {}
    template <class I1, class I2>
    Interpolation interpolate(const I1 &xBegin, const I1 &xEnd,
                              const I2 &yBegin) const {
        return SviInterpolation(xBegin, xEnd, yBegin, t_, forward_, a_, b_,
                                 sigma_, rho_, m_, aIsFixed_, bIsFixed_,
                                 sigmaIsFixed_, rhoIsFixed_, mIsFixed_,
                                 vegaWeighted_, endCriteria_, optMethod_,
                                 errorAccept_, useMaxError_, maxGuesses_);
    }
    static const bool global = true;

  private:
    Time t_;
    Real forward_;
    Real a_, b_, sigma_, rho_, m_;
    bool aIsFixed_, bIsFixed_, sigmaIsFixed_, rhoIsFixed_, mIsFixed_;
    bool vegaWeighted_;
    const ext::shared_ptr<EndCriteria> endCriteria_;
    const ext::shared_ptr<OptimizationMethod> optMethod_;
    const Real errorAccept_;
    const bool useMaxError_;
    const Size maxGuesses_;
};
}

#endif