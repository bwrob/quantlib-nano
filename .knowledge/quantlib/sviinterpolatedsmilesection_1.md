 hasFloatingStrikes_;

    mutable Real forwardValue_;
    mutable std::vector<Volatility> vols_;
    //! Svi parameters
    Real a_, b_, sigma_, rho_, m_;
    //! Svi interpolation settings
    bool isAFixed_, isBFixed_, isSigmaFixed_, isRhoFixed_, isMFixed_;
    bool vegaWeighted_;
    const ext::shared_ptr<EndCriteria> endCriteria_;
    const ext::shared_ptr<OptimizationMethod> method_;
};

inline void SviInterpolatedSmileSection::update() {
    LazyObject::update();
    SmileSection::update();
}

inline Real SviInterpolatedSmileSection::volatilityImpl(Rate strike) const {
    calculate();
    return (*sviInterpolation_)(strike, true);
}

inline Real SviInterpolatedSmileSection::a() const {
    calculate();
    return sviInterpolation_->a();
}

inline Real SviInterpolatedSmileSection::b() const {
    calculate();
    return sviInterpolation_->b();
}

inline Real SviInterpolatedSmileSection::sigma() const {
    calculate();
    return sviInterpolation_->sigma();
}

inline Real SviInterpolatedSmileSection::rho() const {
    calculate();
    return sviInterpolation_->rho();
}

inline Real SviInterpolatedSmileSection::m() const {
    calculate();
    return sviInterpolation_->m();
}

inline Real SviInterpolatedSmileSection::rmsError() const {
    calculate();
    return sviInterpolation_->rmsError();
}

inline Real SviInterpolatedSmileSection::maxError() const {
    calculate();
    return sviInterpolation_->maxError();
}

inline EndCriteria::Type SviInterpolatedSmileSection::endCriteria() const {
    calculate();
    return sviInterpolation_->endCriteria();
}

inline Real SviInterpolatedSmileSection::minStrike() const {
    calculate();
    return actualStrikes_.front();
}

inline Real SviInterpolatedSmileSection::maxStrike() const {
    calculate();
    return actualStrikes_.back();
}

inline Real SviInterpolatedSmileSection::atmLevel() const {
    calculate();
    return forwardValue_;
}
}

#endif