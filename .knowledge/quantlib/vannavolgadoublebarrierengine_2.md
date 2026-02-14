     strikeVol * sqrt(T_), domesticTS_->discount(T_));

                 // already out
                 if ((x0Quote->value() > arguments_.barrier_hi ||
                      x0Quote->value() < arguments_.barrier_lo) &&
                     arguments_.barrierType == DoubleBarrier::KnockOut) {
                     results_.value = 0.0;
                     results_.additionalResults["VanillaPrice"] =
                         adaptVanDelta_ ? bsPriceWithSmile_ : vanillaOption;
                     results_.additionalResults["BarrierInPrice"] =
                         adaptVanDelta_ ? bsPriceWithSmile_ : vanillaOption;
                     results_.additionalResults["BarrierOutPrice"] = Real(0.0);
                 }
                 // already in
                 else if ((x0Quote->value() > arguments_.barrier_hi ||
                           x0Quote->value() < arguments_.barrier_lo) &&
                          arguments_.barrierType == DoubleBarrier::KnockIn) {
                     results_.value = adaptVanDelta_ ? bsPriceWithSmile_ : vanillaOption;
                     results_.additionalResults["VanillaPrice"] =
                         adaptVanDelta_ ? bsPriceWithSmile_ : vanillaOption;
                     results_.additionalResults["BarrierInPrice"] =
                         adaptVanDelta_ ? bsPriceWithSmile_ : vanillaOption;
                     results_.additionalResults["BarrierOutPrice"] = Real(0.0);
                 } else {

                     // set up BS barrier option pricing
                     // only calculate out barrier option price
                     // in barrier price = vanilla - out barrier
                     ext::shared_ptr<StrikedTypePayoff> payoff =
                         ext::static_pointer_cast<StrikedTypePayoff>(arguments_.payoff);
                     DoubleBarrierOption doubleBarrierOption(
                         DoubleBarrier::KnockOut, arguments_.barrier_lo, arguments_.barrier_hi,
                         arguments_.rebate, payoff, arguments_.exercise);

                     doubleBarrierOption.setPricingEngine(engineBS);

                     // BS price
                     Real priceBS = doubleBarrierOption.NPV();

                     Real priceAtmCallBS = blackFormula(
                         Option::Call, atmStrike,
                         x0Quote->value() * foreignTS_->discount(T_) / domesticTS_->discount(T_),
                         atmVol_->value() * sqrt(T_), domesticTS_->discount(T_));
                     Real price25CallBS = blackFormula(
                         Option::Call, call25Strike,
                         x0Quote->value() * foreignTS_->discount(T_) / domesticTS_->discount(T_),
                         atmVol_->value() * sqrt(T_), domesticTS_->discount(T_));
                     Real price25PutBS = blackFormula(
                         Option::Put, put25Strike,
                         x0Quote->value() * foreignTS_->discount(T_) / domesticTS_->discount(T_),
                         atmVol_->value() * sqrt(T_), domesticTS_->discount(T_));

                     // market price
                     Real priceAtmCallMkt = blackFormula(
                         Option::Call, atmStrike,
                         x0Quote->value() * foreignTS_->discount(T_) / domesticTS_->discount(T_),
                         atmVol_->value() * sqrt(T_), domesticTS_->discount(T_));
                     Real price25CallMkt = blackFormula(
                         Option::Call, call25Strike,
                         x0Quote->value() * foreignTS_->discount(T_) / domesticTS_->discount(T_),
                         call25Vol * sqrt(T_), domesticTS_->discount(T_));
                     Real price25PutMkt = blackFormula(
                         Option::Put, put25Strike,
                         x0Quote->value() * foreignTS_->discount(T_) / domesticTS_->discount(T_),
                         put25Vol * sqrt(T_), domesticTS_->discount(T_));

                     // Analytical Black Schole