rWith(atmVolatility_);
    for (auto& volHandle : volHandles_)
        LazyObject::registerWith(volHandle);
}

template <typename Evaluation>
ZabrInterpolatedSmileSection<Evaluation>::ZabrInterpolatedSmileSection(
    const Date& optionDate,
    const Rate& forward,
    const std::vector<Rate>& strikes,
    bool hasFloatingStrikes,
    const Volatility& atmVolatility,
    const std::vector<Volatility>& volHandles,
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
: SmileSection(optionDate, dc),
  forward_(Handle<Quote>(ext::shared_ptr<Quote>(new SimpleQuote(forward)))),
  atmVolatility_(Handle<Quote>(ext::shared_ptr<Quote>(new SimpleQuote(atmVolatility)))),
  volHandles_(volHandles.size()), strikes_(strikes), actualStrikes_(strikes),
  hasFloatingStrikes_(hasFloatingStrikes), vols_(volHandles.size()), alpha_(alpha), beta_(beta),
  nu_(nu), rho_(rho), gamma_(gamma), isAlphaFixed_(isAlphaFixed), isBetaFixed_(isBetaFixed),
  isNuFixed_(isNuFixed), isRhoFixed_(isRhoFixed), isGammaFixed_(isGammaFixed),
  vegaWeighted_(vegaWeighted), endCriteria_(std::move(endCriteria)), method_(std::move(method)) {

    for (Size i = 0; i < volHandles_.size(); ++i)
        volHandles_[i] = Handle<Quote>(
            ext::shared_ptr<Quote>(new SimpleQuote(volHandles[i])));
}

template <typename Evaluation>
void ZabrInterpolatedSmileSection<Evaluation>::createInterpolation() const {
    ext::shared_ptr<ZabrInterpolation<Evaluation> > tmp(
        new ZabrInterpolation<Evaluation>(
            actualStrikes_.begin(), actualStrikes_.end(), vols_.begin(),
            exerciseTime(), forwardValue_, alpha_, beta_, nu_, rho_, gamma_,
            isAlphaFixed_, isBetaFixed_, isNuFixed_, isRhoFixed_, isGammaFixed_,
            vegaWeighted_, endCriteria_, method_));
    swap(tmp, zabrInterpolation_);
}

template <typename Evaluation>
void ZabrInterpolatedSmileSection<Evaluation>::performCalculations() const {
    forwardValue_ = forward_->value();
    vols_.clear();
    actualStrikes_.clear();
    // we populate the volatilities, skipping the invalid ones
    for (Size i = 0; i < volHandles_.size(); ++i) {
        if (volHandles_[i]->isValid()) {
            if (hasFloatingStrikes_) {
                actualStrikes_.push_back(forwardValue_ + strikes_[i]);
                vols_.push_back(atmVolatility_->value() +
                                volHandles_[i]->value());
            } else {
                actualStrikes_.push_back(strikes_[i]);
                vols_.push_back(volHandles_[i]->value());
            }
        }
    }
    // we are recreating the sabrinterpolation object unconditionnaly to
    // avoid iterator invalidation
    createInterpolation();
    zabrInterpolation_->update();
}

template <typename Evaluation>
Real ZabrInterpolatedSmileSection<Evaluation>::varianceImpl(Real strike) const {
    calculate();
    Real v = (*zabrInterpolation_)(strike, true);
    return v * v * exerciseTime();
}
}

#endif