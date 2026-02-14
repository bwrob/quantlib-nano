ousIndex = swapLengthsPreviousNode - swapLengths.begin();
        if (swapLengthsPreviousIndex >0)
            swapLengthsPreviousIndex --;

        std::vector< std::vector<ext::shared_ptr<SmileSection> > > smiles;
        std::vector<ext::shared_ptr<SmileSection> >  smilesOnPreviousExpiry;
        std::vector<ext::shared_ptr<SmileSection> >  smilesOnNextExpiry;

        QL_REQUIRE(optionTimesPreviousIndex+1 < sparseSmiles_.size(),
                   "optionTimesPreviousIndex+1 >= sparseSmiles_.size()");
        QL_REQUIRE(swapLengthsPreviousIndex+1 < sparseSmiles_[0].size(),
                   "swapLengthsPreviousIndex+1 >= sparseSmiles_[0].size()");
        smilesOnPreviousExpiry.push_back(
              sparseSmiles_[optionTimesPreviousIndex][swapLengthsPreviousIndex]);
        smilesOnPreviousExpiry.push_back(
              sparseSmiles_[optionTimesPreviousIndex][swapLengthsPreviousIndex+1]);
        smilesOnNextExpiry.push_back(
              sparseSmiles_[optionTimesPreviousIndex+1][swapLengthsPreviousIndex]);
        smilesOnNextExpiry.push_back(
              sparseSmiles_[optionTimesPreviousIndex+1][swapLengthsPreviousIndex+1]);

        smiles.push_back(smilesOnPreviousExpiry);
        smiles.push_back(smilesOnNextExpiry);

        std::vector<Real> optionsNodes(2);
        optionsNodes[0] = optionTimes[optionTimesPreviousIndex];
        optionsNodes[1] = optionTimes[optionTimesPreviousIndex+1];

        std::vector<Date> optionsDateNodes(2);
        optionsDateNodes[0] = optionDates[optionTimesPreviousIndex];
        optionsDateNodes[1] = optionDates[optionTimesPreviousIndex+1];

        std::vector<Real> swapLengthsNodes(2);
        swapLengthsNodes[0] = swapLengths[swapLengthsPreviousIndex];
        swapLengthsNodes[1] = swapLengths[swapLengthsPreviousIndex+1];

        std::vector<Period> swapTenorNodes(2);
        swapTenorNodes[0] = swapTenors[swapLengthsPreviousIndex];
        swapTenorNodes[1] = swapTenors[swapLengthsPreviousIndex+1];

        Rate atmForward = atmStrike(atmOptionDate, atmSwapTenor);
        Real shift = atmVol_->shift(atmOptionTime, atmTimeLength);

        Matrix atmForwards(2, 2, 0.0);
        Matrix atmShifts(2,2,0.0);
        Matrix atmVols(2, 2, 0.0);
        for (Size i=0; i<2; i++) {
            for (Size j=0; j<2; j++) {
                atmForwards[i][j] = atmStrike(optionsDateNodes[i],
                                              swapTenorNodes[j]);
                atmShifts[i][j] = atmVol_->shift(optionsNodes[i], swapLengthsNodes[j]);
                // atmVols[i][j] = smiles[i][j]->volatility(atmForwards[i][j]);
                atmVols[i][j] = atmVol_->volatility(
                    optionsDateNodes[i], swapTenorNodes[j], atmForwards[i][j]);
                /* With the old implementation the interpolated spreads on ATM
                   volatilities were null even if the spreads on ATM volatilities to be
                   interpolated were non-zero. The new implementation removes
                   this behaviour, but introduces a small ERROR in the cube:
                   even if no spreads are applied on any cube ATM volatility corresponding
                   to quoted smile sections (that is ATM volatilities in sparse cube), the
                   cube ATM volatilities corresponding to not quoted smile sections (that
                   is ATM volatilities in dense cube) are no more exactly the quoted values,
                   but that ones PLUS the linear interpolation of the fit errors on the ATM
                   volatilities in sparse cube whose spreads are used in the calculation.
                   A similar imprecision is introduced to the volatilities in dense cube
                   whith moneyness near to 1.
                   (See below how spreadVols are calculated).
                   The extent of this error depends on the quality of the fit: in case of
                   good fits it is negligibile.
                */
            }
        }

        for
