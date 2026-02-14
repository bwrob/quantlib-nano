const override {

                 using std::sqrt;

                 const Real sigmaShift_vega = 0.001;
                 const Real sigmaShift_volga = 0.0001;
                 const Real spotShift_delta = 0.0001 * spotFX_->value();
                 const Real sigmaShift_vanna = 0.0001;

                 QL_REQUIRE(arguments_.barrierType == DoubleBarrier::KnockIn ||
                                arguments_.barrierType == DoubleBarrier::KnockOut,
                            "Only same type barrier supported");

                 Handle<Quote> x0Quote( // used for shift
                     ext::make_shared<SimpleQuote>(spotFX_->value()));
                 Handle<Quote> atmVolQuote( // used for shift
                     ext::make_shared<SimpleQuote>(atmVol_->value()));

                 ext::shared_ptr<BlackVolTermStructure> blackVolTS =
                     ext::make_shared<BlackConstantVol>(Settings::instance().evaluationDate(),
                                                        NullCalendar(), atmVolQuote,
                                                        Actual365Fixed());
                 ext::shared_ptr<BlackScholesMertonProcess> stochProcess =
                     ext::make_shared<BlackScholesMertonProcess>(
                         x0Quote, foreignTS_, domesticTS_,
                         Handle<BlackVolTermStructure>(blackVolTS));

                 ext::shared_ptr<PricingEngine> engineBS =
                     ext::make_shared<DoubleBarrierEngine>(stochProcess, series_);

                 BlackDeltaCalculator blackDeltaCalculatorAtm(
                     Option::Call, atmVol_->deltaType(), x0Quote->value(),
                     domesticTS_->discount(T_), foreignTS_->discount(T_),
                     atmVol_->value() * sqrt(T_));
                 Real atmStrike = blackDeltaCalculatorAtm.atmStrike(atmVol_->atmType());

                 Real call25Vol = vol25Call_->value();
                 Real put25Vol = vol25Put_->value();
                 BlackDeltaCalculator blackDeltaCalculatorPut25(
                     Option::Put, vol25Put_->deltaType(), x0Quote->value(),
                     domesticTS_->discount(T_), foreignTS_->discount(T_), put25Vol * sqrt(T_));
                 Real put25Strike = blackDeltaCalculatorPut25.strikeFromDelta(-0.25);
                 BlackDeltaCalculator blackDeltaCalculatorCall25(
                     Option::Call, vol25Call_->deltaType(), x0Quote->value(),
                     domesticTS_->discount(T_), foreignTS_->discount(T_), call25Vol * sqrt(T_));
                 Real call25Strike = blackDeltaCalculatorCall25.strikeFromDelta(0.25);

                 // here use vanna volga interpolated smile to price vanilla
                 std::vector<Real> strikes;
                 std::vector<Real> vols;
                 strikes.push_back(put25Strike);
                 vols.push_back(put25Vol);
                 strikes.push_back(atmStrike);
                 vols.push_back(atmVol_->value());
                 strikes.push_back(call25Strike);
                 vols.push_back(call25Vol);
                 VannaVolga vannaVolga(x0Quote->value(), foreignTS_->discount(T_),
                                       foreignTS_->discount(T_), T_);
                 Interpolation interpolation =
                     vannaVolga.interpolate(strikes.begin(), strikes.end(), vols.begin());
                 interpolation.enableExtrapolation();
                 const ext::shared_ptr<StrikedTypePayoff> payoff =
                     ext::dynamic_pointer_cast<StrikedTypePayoff>(arguments_.payoff);
                 Real strikeVol = interpolation(payoff->strike());
                 // vanilla option price
                 Real vanillaOption = blackFormula(payoff->optionType(), payoff->strike(),
                                                   x0Quote->value() * foreignTS_->discount(T_) /
                                                       domesticTS_->discount(T_),
                                              