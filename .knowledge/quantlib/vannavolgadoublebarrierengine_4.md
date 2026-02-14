                 Real vegaBarBS2 = (doubleBarrierOption.NPV() - priceBS2) / sigmaShift_vega;
                     Real volgaBarBS = (vegaBarBS2 - vegaBarBS) / sigmaShift_volga;
                     ext::static_pointer_cast<SimpleQuote>(atmVolQuote.currentLink())
                         ->setValue(atmVolQuote->value() - sigmaShift_volga -
                                    sigmaShift_vega); // setback

                     // BS Delta
                     // base delta
                     ext::static_pointer_cast<SimpleQuote>(x0Quote.currentLink())
                         ->setValue(x0Quote->value() + spotShift_delta); // shift forth
                     doubleBarrierOption.recalculate();
                     Real priceBS_delta1 = doubleBarrierOption.NPV();

                     ext::static_pointer_cast<SimpleQuote>(x0Quote.currentLink())
                         ->setValue(x0Quote->value() - 2 * spotShift_delta); // shift back
                     doubleBarrierOption.recalculate();
                     Real priceBS_delta2 = doubleBarrierOption.NPV();

                     ext::static_pointer_cast<SimpleQuote>(x0Quote.currentLink())
                         ->setValue(x0Quote->value() + spotShift_delta); // set back
                     Real deltaBar1 = (priceBS_delta1 - priceBS_delta2) / (2.0 * spotShift_delta);

                     // shifted vanna
                     ext::static_pointer_cast<SimpleQuote>(atmVolQuote.currentLink())
                         ->setValue(atmVolQuote->value() + sigmaShift_vanna); // shift sigma
                     // shifted delta
                     ext::static_pointer_cast<SimpleQuote>(x0Quote.currentLink())
                         ->setValue(x0Quote->value() + spotShift_delta); // shift forth
                     doubleBarrierOption.recalculate();
                     priceBS_delta1 = doubleBarrierOption.NPV();

                     ext::static_pointer_cast<SimpleQuote>(x0Quote.currentLink())
                         ->setValue(x0Quote->value() - 2 * spotShift_delta); // shift back
                     doubleBarrierOption.recalculate();
                     priceBS_delta2 = doubleBarrierOption.NPV();

                     ext::static_pointer_cast<SimpleQuote>(x0Quote.currentLink())
                         ->setValue(x0Quote->value() + spotShift_delta); // set back
                     Real deltaBar2 = (priceBS_delta1 - priceBS_delta2) / (2.0 * spotShift_delta);

                     Real vannaBarBS = (deltaBar2 - deltaBar1) / sigmaShift_vanna;

                     ext::static_pointer_cast<SimpleQuote>(atmVolQuote.currentLink())
                         ->setValue(atmVolQuote->value() - sigmaShift_vanna); // set back

                     // Matrix
                     Matrix A(3, 3, 0.0);

                     // analytical
                     A[0][0] = vegaAtm_Analytical;
                     A[0][1] = vega25Call_Analytical;
                     A[0][2] = vega25Put_Analytical;
                     A[1][0] = vannaAtm_Analytical;
                     A[1][1] = vanna25Call_Analytical;
                     A[1][2] = vanna25Put_Analytical;
                     A[2][0] = volgaAtm_Analytical;
                     A[2][1] = volga25Call_Analytical;
                     A[2][2] = volga25Put_Analytical;

                     Array b(3, 0.0);
                     b[0] = vegaBarBS;
                     b[1] = vannaBarBS;
                     b[2] = volgaBarBS;
                     Array q = inverse(A) * b;

                     Real H = arguments_.barrier_hi;
                     Real L = arguments_.barrier_lo;
                     Real theta_tilt_minus = ((domesticTS_->zeroRate(T_, Continuous).rate() -
                                               foreignTS_->zeroRate(T_, Continuous).rate()) /
                                                  atmVol_->value() -
                                              atmVol_->value() / 2.0) *
                                             std::sqrt(T_);

