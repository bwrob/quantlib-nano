ate <typename Evaluation>
void ZabrSmileSection<Evaluation>::init2(ZabrShortMaturityNormal) {}

template <typename Evaluation>
void ZabrSmileSection<Evaluation>::init2(ZabrLocalVolatility) {
    callPrices_ = model_->fdPrice(strikes_);
}

template <typename Evaluation>
void ZabrSmileSection<Evaluation>::init2(ZabrFullFd) {
    callPrices_.resize(strikes_.size());
#pragma omp parallel for
    for (long i = 0; i < (long)strikes_.size(); i++) {
        callPrices_[i] = model_->fullFdPrice(strikes_[i]);
    }
}

template <typename Evaluation>
void ZabrSmileSection<Evaluation>::init3(ZabrShortMaturityLognormal) {}

template <typename Evaluation>
void ZabrSmileSection<Evaluation>::init3(ZabrShortMaturityNormal) {}

template <typename Evaluation>
void ZabrSmileSection<Evaluation>::init3(ZabrLocalVolatility) {
    strikes_.insert(strikes_.begin(), 0.0);
    callPrices_.insert(callPrices_.begin(), forward_);

    callPriceFct_ = ext::shared_ptr<Interpolation>(new CubicInterpolation(
        strikes_.begin(), strikes_.end(), callPrices_.begin(),
        CubicInterpolation::Spline, true, CubicInterpolation::SecondDerivative,
        0.0, CubicInterpolation::SecondDerivative, 0.0));
    // callPriceFct_ =
    //     ext::shared_ptr<Interpolation>(new LinearInterpolation(
    //         strikes_.begin(), strikes_.end(), callPrices_.begin()));

    callPriceFct_->enableExtrapolation();

    // on the right side we extrapolate exponetially (because spline
    // does not make sense)
    // we precompute the necessary parameters here
    static const Real eps = 1E-5; // gap for first derivative computation

    Real c0 = (*callPriceFct_)(strikes_.back());
    Real c0p = ((*callPriceFct_)(strikes_.back() - eps) - c0) / eps;

    a_ = c0p / c0;
    b_ = std::log(c0) + a_ * strikes_.back();
}

template <typename Evaluation>
void ZabrSmileSection<Evaluation>::init3(ZabrFullFd) {
    init3(ZabrLocalVolatility());
}

template <typename Evaluation>
Real
ZabrSmileSection<Evaluation>::optionPrice(Real strike, Option::Type type,
                                          Real discount,
                                          ZabrShortMaturityLognormal) const {
    return SmileSection::optionPrice(strike, type, discount);
}

template <typename Evaluation>
Real ZabrSmileSection<Evaluation>::optionPrice(Real strike, Option::Type type,
                                               Real discount,
                                               ZabrShortMaturityNormal) const {
    return bachelierBlackFormula(
        type, strike, forward_,
        model_->normalVolatility(strike) * std::sqrt(exerciseTime()), discount);
}

template <typename Evaluation>
Real ZabrSmileSection<Evaluation>::optionPrice(Rate strike, Option::Type type,
                                               Real discount,
                                               ZabrLocalVolatility) const {
    Real call = strike <= strikes_.back() ? (*callPriceFct_)(strike)
                                          : exp(-a_ * strike + b_);
    if (type == Option::Call)
        return call * discount;
    else
        return (call - (forward_ - strike)) * discount;
}

template <typename Evaluation>
Real ZabrSmileSection<Evaluation>::optionPrice(Rate strike, Option::Type type,
                                               Real discount,
                                               ZabrFullFd) const {
    return optionPrice(strike, type, discount, ZabrLocalVolatility());
}

template <typename Evaluation>
Real
ZabrSmileSection<Evaluation>::volatilityImpl(Rate strike,
                                             ZabrShortMaturityLognormal) const {
    strike = std::max(1E-6, strike);
    return model_->lognormalVolatility(strike);
}

template <typename Evaluation>
Real
ZabrSmileSection<Evaluation>::volatilityImpl(Rate strike,
                                             ZabrShortMaturityNormal) const {
    Real impliedVol = 0.0;
    try {
        Option::Type type;
        if (strike >= model_->fo