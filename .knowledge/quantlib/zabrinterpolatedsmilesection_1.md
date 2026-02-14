Quote> atmVolatility_;
    std::vector<Handle<Quote> > volHandles_;
    mutable std::vector<Rate> strikes_;
    //! Only strikes corresponding to valid market data
    mutable std::vector<Rate> actualStrikes_;
    bool hasFloatingStrikes_;

    mutable Real forwardValue_;
    mutable std::vector<Volatility> vols_;
    //! Sabr parameters
    Real alpha_, beta_, nu_, rho_, gamma_;
    //! Sabr interpolation settings
    bool isAlphaFixed_, isBetaFixed_, isNuFixed_, isRhoFixed_, isGammaFixed_;
    bool vegaWeighted_;
    const ext::shared_ptr<EndCriteria> endCriteria_;
    const ext::shared_ptr<OptimizationMethod> method_;
};

template <typename Evaluation>
inline void ZabrInterpolatedSmileSection<Evaluation>::update() {
    LazyObject::update();
    SmileSection::update();
}

template <typename Evaluation>
inline Real
ZabrInterpolatedSmileSection<Evaluation>::volatilityImpl(Rate strike) const {
    calculate();
    return (*zabrInterpolation_)(strike, true);
}

template <typename Evaluation>
inline Real ZabrInterpolatedSmileSection<Evaluation>::alpha() const {
    calculate();
    return zabrInterpolation_->alpha();
}

template <typename Evaluation>
inline Real ZabrInterpolatedSmileSection<Evaluation>::beta() const {
    calculate();
    return zabrInterpolation_->beta();
}

template <typename Evaluation>
inline Real ZabrInterpolatedSmileSection<Evaluation>::nu() const {
    calculate();
    return zabrInterpolation_->nu();
}

template <typename Evaluation>
inline Real ZabrInterpolatedSmileSection<Evaluation>::rho() const {
    calculate();
    return zabrInterpolation_->rho();
}

template <typename Evaluation>
inline Real ZabrInterpolatedSmileSection<Evaluation>::gamma() const {
    calculate();
    return zabrInterpolation_->gamma();
}

template <typename Evaluation>
inline Real ZabrInterpolatedSmileSection<Evaluation>::rmsError() const {
    calculate();
    return zabrInterpolation_->rmsError();
}

template <typename Evaluation>
inline Real ZabrInterpolatedSmileSection<Evaluation>::maxError() const {
    calculate();
    return zabrInterpolation_->maxError();
}

template <typename Evaluation>
inline EndCriteria::Type
ZabrInterpolatedSmileSection<Evaluation>::endCriteria() const {
    calculate();
    return zabrInterpolation_->endCriteria();
}

template <typename Evaluation>
inline Real ZabrInterpolatedSmileSection<Evaluation>::minStrike() const {
    calculate();
    return actualStrikes_.front();
}

template <typename Evaluation>
inline Real ZabrInterpolatedSmileSection<Evaluation>::maxStrike() const {
    calculate();
    return actualStrikes_.back();
}

template <typename Evaluation>
inline Real ZabrInterpolatedSmileSection<Evaluation>::atmLevel() const {
    calculate();
    return forwardValue_;
}

template <typename Evaluation>
ZabrInterpolatedSmileSection<Evaluation>::ZabrInterpolatedSmileSection(
    const Date& optionDate,
    Handle<Quote> forward,
    const std::vector<Rate>& strikes,
    bool hasFloatingStrikes,
    Handle<Quote> atmVolatility,
    const std::vector<Handle<Quote> >& volHandles,
    Real alpha,
    Real beta,
    Real nu,
    Real rho,
    Real gamma,
    bool isAlphaFixed,
    bool isBetaFixed,
    bool isNuFixed,
    bool isRhoFixed,
    bool isGammaFixed,
    bool vegaWeighted,
    ext::shared_ptr<EndCriteria> endCriteria,
    ext::shared_ptr<OptimizationMethod> method,
    const DayCounter& dc)
: SmileSection(optionDate, dc), forward_(std::move(forward)),
  atmVolatility_(std::move(atmVolatility)), volHandles_(volHandles), strikes_(strikes),
  actualStrikes_(strikes), hasFloatingStrikes_(hasFloatingStrikes), vols_(volHandles.size()),
  alpha_(alpha), beta_(beta), nu_(nu), rho_(rho), gamma_(gamma), isAlphaFixed_(isAlphaFixed),
  isBetaFixed_(isBetaFixed), isNuFixed_(isNuFixed), isRhoFixed_(isRhoFixed),
  isGammaFixed_(isGammaFixed), vegaWeighted_(vegaWeighted), endCriteria_(std::move(endCriteria)),
  method_(std::move(method)) {

    LazyObject::registerWith(forward_);
    LazyObject::registe
