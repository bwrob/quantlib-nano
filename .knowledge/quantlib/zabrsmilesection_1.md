MaturityNormal) const;
    Volatility volatilityImpl(Rate strike, ZabrLocalVolatility) const;
    Volatility volatilityImpl(Rate strike, ZabrFullFd) const;
    ext::shared_ptr<ZabrModel> model_;
    Evaluation evaluation_;
    Rate forward_;
    std::vector<Real> params_;
    const Size fdRefinement_;
    std::vector<Real> strikes_, callPrices_;
    ext::shared_ptr<Interpolation> callPriceFct_;
    Real a_, b_;
};

template <typename Evaluation>
ZabrSmileSection<Evaluation>::ZabrSmileSection(Time timeToExpiry,
                                               Rate forward,
                                               std::vector<Real> zabrParams,
                                               const std::vector<Real>& moneyness,
                                               const Size fdRefinement)
: SmileSection(timeToExpiry, DayCounter()), forward_(forward), params_(std::move(zabrParams)),
  fdRefinement_(fdRefinement) {
    init(moneyness);
}

template <typename Evaluation>
ZabrSmileSection<Evaluation>::ZabrSmileSection(const Date& d,
                                               Rate forward,
                                               std::vector<Real> zabrParams,
                                               const DayCounter& dc,
                                               const std::vector<Real>& moneyness,
                                               const Size fdRefinement)
: SmileSection(d, dc, Date()), forward_(forward), params_(std::move(zabrParams)),
  fdRefinement_(fdRefinement) {
    init(moneyness);
}

template <typename Evaluation>
void ZabrSmileSection<Evaluation>::init(const std::vector<Real> &,
                                        ZabrShortMaturityLognormal) {

    model_ = ext::make_shared<ZabrModel>(
        exerciseTime(), forward_, params_[0], params_[1],
                      params_[2], params_[3], params_[4]);
}

template <typename Evaluation>
void ZabrSmileSection<Evaluation>::init(const std::vector<Real> &a,
                                        ZabrShortMaturityNormal) {
    init(a, ZabrShortMaturityLognormal());
}

template <typename Evaluation>
void ZabrSmileSection<Evaluation>::init(const std::vector<Real> &moneyness,
                                        ZabrLocalVolatility) {

    QL_REQUIRE(params_.size() >= 5,
               "zabr expects 5 parameters (alpha,beta,nu,rho,gamma) but ("
                   << params_.size() << ") given");

    model_ = ext::make_shared<ZabrModel>(
        exerciseTime(), forward_, params_[0], params_[1],
                      params_[2], params_[3], params_[4]);

    // set up strike grid for local vol or full fd flavour of this section
    // this is shared with SmileSectionUtils - unify later ?
    static const Real defaultMoney[] = {
        0.0, 0.01, 0.05, 0.10, 0.25, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90,
        1.0, 1.25, 1.5,  1.75, 2.0,  5.0,  7.5,  10.0, 15.0, 20.0};
    std::vector<Real> tmp;
    if (moneyness.empty())
        tmp = std::vector<Real>(defaultMoney, defaultMoney + 21);
    else
        tmp = std::vector<Real>(moneyness);

    strikes_.clear(); // should not be necessary, anyway
    Real lastF = 0.0;
    bool firstStrike = true;
    for (Real i : tmp) {
        Real f = i * forward_;
        if (f > 0.0) {
            if (!firstStrike) {
                for (Size j = 1; j <= fdRefinement_; ++j) {
                    strikes_.push_back(lastF +
                                       ((double)j) * (f - lastF) /
                                           (fdRefinement_ + 1));
                }
            }
            firstStrike = false;
            lastF = f;
            strikes_.push_back(f);
        }
    }
}

template <typename Evaluation>
void ZabrSmileSection<Evaluation>::init(const std::vector<Real> &moneyness,
                                        ZabrFullFd) {
    init(moneyness, ZabrLocalVolatility());
}

template <typename Evaluation>
void ZabrSmileSection<Evaluation>::init2(ZabrShortMaturityLognormal) {}

templ
