       Period& lag,
        Natural fixingDays,
        const ext::shared_ptr<YoYInflationIndex>& anIndex,
        const ext::shared_ptr<YoYCapFloorTermPriceSurface>& surf,
        ext::shared_ptr<YoYInflationCapFloorEngine> p,
        Real priceToMatch)
    : slope_(slope), K_(K), frequency_(anIndex->frequency()),
      indexIsInterpolated_(anIndex->interpolated()), tvec_(std::vector<Time>(2)),
      dvec_(std::vector<Date>(2)), vvec_(std::vector<Volatility>(2)), priceToMatch_(priceToMatch),
      surf_(surf), p_(std::move(p)) {

        lag_ = surf_->observationLag();
        capfloor_ =
            MakeYoYInflationCapFloor(type, anIndex,
                                     (Size)std::floor(0.5+surf->timeFromReference(surf->minMaturity())),
                                     surf->calendar(), lag, CPI::AsIndex)
            .withNominal(10000.0)
            .withStrike(K);

        // shortest time available from price surface
        dvec_[0] = surf_->baseDate();
        dvec_[1] = surf_->minMaturity() +
                   Period(7, Days);
        tvec_[0] = surf_->dayCounter().yearFraction(surf_->referenceDate(),
                                                    dvec_[0] );
        tvec_[1] = surf_->dayCounter().yearFraction(surf_->referenceDate(),
                                                    dvec_[1]);

        Size n = (Size)std::floor(0.5 + surf->timeFromReference(surf_->minMaturity()));
        QL_REQUIRE( n > 0,
                    "first maturity in price surface not > 0: "
                    << n);

        capfloor_->setPricingEngine(p_);
        // pricer already setup just need to do the volatility surface each time
    }


    template <class Interpolator1D>
    Real InterpolatedYoYOptionletStripper<Interpolator1D>::
    ObjectiveFunction::operator()(Volatility guess) const {

        vvec_[1] = guess;
        vvec_[0] = guess - slope_ * (tvec_[1] - tvec_[0]) * guess;
        // could have Interpolator1D instead of Linear
        ext::shared_ptr<InterpolatedYoYOptionletVolatilityCurve<Linear> >
        vCurve(
            new InterpolatedYoYOptionletVolatilityCurve<Linear>(
                                               0, TARGET(), ModifiedFollowing,
                                               Actual365Fixed(), lag_,
                                               frequency_, indexIsInterpolated_,
                                               dvec_, vvec_,
                                               -1.0, 3.0) ); // strike limits
        Handle<YoYOptionletVolatilitySurface> hCurve(vCurve);
        p_->setVolatility(hCurve);
        // hopefully this gets to the pricer ... then
        return priceToMatch_ - capfloor_->NPV();
    }


    template <class Interpolator1D>
    void InterpolatedYoYOptionletStripper<Interpolator1D>::
    initialize(const ext::shared_ptr<YoYCapFloorTermPriceSurface> &s,
               const ext::shared_ptr<YoYInflationCapFloorEngine> &p,
               const Real slope) const {
        YoYCapFloorTermPriceSurface_ = s;
        p_ = p;
        lag_ = YoYCapFloorTermPriceSurface_->observationLag();
        frequency_ = YoYCapFloorTermPriceSurface_->frequency();
        indexIsInterpolated_ = YoYCapFloorTermPriceSurface_->indexIsInterpolated();
        Natural fixingDays_ = YoYCapFloorTermPriceSurface_->fixingDays();
        Natural settlementDays = 0; // always
        Calendar cal = YoYCapFloorTermPriceSurface_->calendar();
        BusinessDayConvention bdc =
            YoYCapFloorTermPriceSurface_->businessDayConvention();
        DayCounter dc = YoYCapFloorTermPriceSurface_->dayCounter();

        // switch from caps to floors when out of floors
        Rate maxFloor = YoYCapFloorTermPriceSurface_->floorStrikes().back();
        YoYInflationCapFloor::Type useType = YoYInflationCapFloor::Floor;
        Period TPmin = YoYCapFloorTermPriceSurface_->maturities().front();
        // create a "fake index" based on Generic, this should work
        // provided that the la
