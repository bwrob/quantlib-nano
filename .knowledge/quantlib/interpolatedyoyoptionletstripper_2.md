g and frequency are correct
        RelinkableHandle<YoYInflationTermStructure> hYoY(
                                       YoYCapFloorTermPriceSurface_->YoYTS());
        ext::shared_ptr<YoYInflationIndex> anIndex(
                                           new YYGenericCPI(frequency_,
                                                            false, lag_,
                                                            Currency(), hYoY));

        // strip each K separatly
        for (Size i=0; i<YoYCapFloorTermPriceSurface_->strikes().size(); i++) {
            Rate K = YoYCapFloorTermPriceSurface_->strikes()[i];
            if (K > maxFloor) useType = YoYInflationCapFloor::Cap;

            // solve for the initial point on the vol curve
            Brent solver;
            Real solverTolerance_ = 1e-7;
             // these are VOLATILITY guesses (always +)
            Real lo = 0.00001, hi = 0.08;
            Real guess = (hi+lo)/2.0;
            Real found;
            Real priceToMatch =
                (useType == YoYInflationCapFloor::Cap ?
                 YoYCapFloorTermPriceSurface_->capPrice(TPmin, K) :
                 YoYCapFloorTermPriceSurface_->floorPrice(TPmin, K));

            try{
                found = solver.solve(
                      ObjectiveFunction(useType, slope, K, lag_, fixingDays_,
                                        anIndex, YoYCapFloorTermPriceSurface_,
                                        p_, priceToMatch),
                      solverTolerance_, guess, lo, hi );
            } catch( std::exception &e) {
                QL_FAIL("failed to find solution here because: " << e.what());
            }

            // ***create helpers***
            Real notional = 10000; // work in bps
            std::vector<ext::shared_ptr<BootstrapHelper<YoYOptionletVolatilitySurface> > > helperInstruments;
            std::vector<ext::shared_ptr<YoYOptionletHelper> > helpers;
            for (Size j = 0; j < YoYCapFloorTermPriceSurface_->maturities().size(); j++){
                Period Tp = YoYCapFloorTermPriceSurface_->maturities()[j];

                Real nextPrice =
                    (useType == YoYInflationCapFloor::Cap ?
                     YoYCapFloorTermPriceSurface_->capPrice(Tp, K) :
                     YoYCapFloorTermPriceSurface_->floorPrice(Tp, K));

                Handle<Quote> quote1(ext::shared_ptr<Quote>(
                                               new SimpleQuote( nextPrice )));
                // helper should be an integer number of periods away,
                // this is enforced by rounding
                Size nT = (Size)floor(s->timeFromReference(s->yoyOptionDateFromTenor(Tp))+0.5);
                helpers.push_back(ext::shared_ptr<YoYOptionletHelper>(
                          new YoYOptionletHelper(quote1, notional, useType,
                                                 lag_,
                                                 dc, cal,
                                                 fixingDays_,
                                                 anIndex, CPI::Flat,
                                                 K, nT, p_)));

                ext::shared_ptr<ConstantYoYOptionletVolatility> yoyVolBLACK(
                          new ConstantYoYOptionletVolatility(found, settlementDays,
                                                             cal, bdc, dc,
                                                             lag_, frequency_,
                                                             false,
                                                             // -100% to +300%
                                                             -1.0,3.0));

                helpers[j]->setTermStructure(
                       // gets underlying pointer & removes const
                       const_cast<ConstantYoYOptionletVolatility*>(
                                                          yoyVolBLACK.get()));
                helperInstruments.push_back(helpers[j]);
  