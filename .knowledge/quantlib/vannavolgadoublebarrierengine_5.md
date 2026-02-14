                    Real h =
                         1.0 / atmVol_->value() * std::log(H / x0Quote->value()) / std::sqrt(T_);
                     Real l =
                         1.0 / atmVol_->value() * std::log(L / x0Quote->value()) / std::sqrt(T_);
                     CumulativeNormalDistribution cnd;

                     Real doubleNoTouch = 0.0;
                     for (int j = -series_; j < series_; j++) {
                         Real e_minus = 2 * j * (h - l) - theta_tilt_minus;
                         doubleNoTouch +=
                             std::exp(-2.0 * j * theta_tilt_minus * (h - l)) *
                                 (cnd(h + e_minus) - cnd(l + e_minus)) -
                             std::exp(-2.0 * j * theta_tilt_minus * (h - l) +
                                      2.0 * theta_tilt_minus * h) *
                                 (cnd(h - 2.0 * h + e_minus) - cnd(l - 2.0 * h + e_minus));
                     }

                     Real p_survival = doubleNoTouch;

                     Real lambda = p_survival;
                     Real adjust = q[0] * (priceAtmCallMkt - priceAtmCallBS) +
                                   q[1] * (price25CallMkt - price25CallBS) +
                                   q[2] * (price25PutMkt - price25PutBS);
                     Real outPrice = priceBS + lambda * adjust; //
                     Real inPrice;

                     // adapt Vanilla delta
                     if (adaptVanDelta_) {
                         outPrice += lambda * (bsPriceWithSmile_ - vanillaOption);
                         // capfloored by (0, vanilla)
                         outPrice = std::max(0.0, std::min(bsPriceWithSmile_, outPrice));
                         inPrice = bsPriceWithSmile_ - outPrice;
                     } else {
                         // capfloored by (0, vanilla)
                         outPrice = std::max(0.0, std::min(vanillaOption, outPrice));
                         inPrice = vanillaOption - outPrice;
                     }

                     if (arguments_.barrierType == DoubleBarrier::KnockOut)
                         results_.value = outPrice;
                     else
                         results_.value = inPrice;
                     results_.additionalResults["VanillaPrice"] = vanillaOption;
                     results_.additionalResults["BarrierInPrice"] = inPrice;
                     results_.additionalResults["BarrierOutPrice"] = outPrice;
                     results_.additionalResults["lambda"] = lambda;
                 }
             }


         private:
           const Handle<DeltaVolQuote> atmVol_;
           const Handle<DeltaVolQuote> vol25Put_;
           const Handle<DeltaVolQuote> vol25Call_;
           const Time T_;
           const Handle<Quote> spotFX_;
           const Handle<YieldTermStructure> domesticTS_;
           const Handle<YieldTermStructure> foreignTS_;
           const bool adaptVanDelta_;
           const Real bsPriceWithSmile_;
           const int series_;
       };


}

#endif
