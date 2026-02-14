s formula
                     NormalDistribution norm;
                     Real d1atm = (std::log(x0Quote->value() * foreignTS_->discount(T_) /
                                            domesticTS_->discount(T_) / atmStrike) +
                                   0.5 * std::pow(atmVolQuote->value(), 2.0) * T_) /
                                  (atmVolQuote->value() * sqrt(T_));
                     Real vegaAtm_Analytical =
                         x0Quote->value() * norm(d1atm) * sqrt(T_) * foreignTS_->discount(T_);
                     Real vannaAtm_Analytical = vegaAtm_Analytical / x0Quote->value() *
                                                (1.0 - d1atm / (atmVolQuote->value() * sqrt(T_)));
                     Real volgaAtm_Analytical = vegaAtm_Analytical * d1atm *
                                                (d1atm - atmVolQuote->value() * sqrt(T_)) /
                                                atmVolQuote->value();

                     Real d125call = (std::log(x0Quote->value() * foreignTS_->discount(T_) /
                                               domesticTS_->discount(T_) / call25Strike) +
                                      0.5 * std::pow(atmVolQuote->value(), 2.0) * T_) /
                                     (atmVolQuote->value() * sqrt(T_));
                     Real vega25Call_Analytical =
                         x0Quote->value() * norm(d125call) * sqrt(T_) * foreignTS_->discount(T_);
                     Real vanna25Call_Analytical =
                         vega25Call_Analytical / x0Quote->value() *
                         (1.0 - d125call / (atmVolQuote->value() * sqrt(T_)));
                     Real volga25Call_Analytical = vega25Call_Analytical * d125call *
                                                   (d125call - atmVolQuote->value() * sqrt(T_)) /
                                                   atmVolQuote->value();

                     Real d125Put = (std::log(x0Quote->value() * foreignTS_->discount(T_) /
                                              domesticTS_->discount(T_) / put25Strike) +
                                     0.5 * std::pow(atmVolQuote->value(), 2.0) * T_) /
                                    (atmVolQuote->value() * sqrt(T_));
                     Real vega25Put_Analytical =
                         x0Quote->value() * norm(d125Put) * sqrt(T_) * foreignTS_->discount(T_);
                     Real vanna25Put_Analytical =
                         vega25Put_Analytical / x0Quote->value() *
                         (1.0 - d125Put / (atmVolQuote->value() * sqrt(T_)));
                     Real volga25Put_Analytical = vega25Put_Analytical * d125Put *
                                                  (d125Put - atmVolQuote->value() * sqrt(T_)) /
                                                  atmVolQuote->value();


                     // BS vega
                     ext::static_pointer_cast<SimpleQuote>(atmVolQuote.currentLink())
                         ->setValue(atmVolQuote->value() + sigmaShift_vega);
                     doubleBarrierOption.recalculate();
                     Real vegaBarBS = (doubleBarrierOption.NPV() - priceBS) / sigmaShift_vega;
                     ext::static_pointer_cast<SimpleQuote>(atmVolQuote.currentLink())
                         ->setValue(atmVolQuote->value() - sigmaShift_vega); // setback

                     // BS volga

                     // vegaBar2
                     // base NPV
                     ext::static_pointer_cast<SimpleQuote>(atmVolQuote.currentLink())
                         ->setValue(atmVolQuote->value() + sigmaShift_volga);
                     doubleBarrierOption.recalculate();
                     Real priceBS2 = doubleBarrierOption.NPV();

                     // shifted npv
                     ext::static_pointer_cast<SimpleQuote>(atmVolQuote.currentLink())
                         ->setValue(atmVolQuote->value() + sigmaShift_vega);
                     doubleBarrierOption.recalculate();
    