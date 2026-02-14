       }
            }
            else
            {
                // error message if t is too large
                if (t > maxExtrapolationMaturity)
                    QL_FAIL("cap/floor intersection finding failed at t = " << t <<
                            ", error msg: no interection found inside the admissible range");
            }
        }

        // extrapolation of swap rates if necessary
        //Polynomial2D tmpInterpol;
        //Interpolation interpol = tmpInterpol.interpolate(tmpSwapMaturities.begin(), tmpSwapMaturities.end(), tmpSwapRates.begin());
        //interpol.enableExtrapolation();
        int counter = 0;
        for (Size i=0; i<cfMaturities_.size(); ++i) {
            if ( !validMaturity[i] ) {
                atmYoYSwapDateRates_.first.push_back(referenceDate()+cfMaturities_[i]);
                atmYoYSwapTimeRates_.first.push_back(timeFromReference(referenceDate()+cfMaturities_[i]));
                // atmYoYSwapRates_->second.push_back(interpol((*cfMaturities_)[i]));
                // Heuristic: overwrite the the swap rate with a value that guarantees that the
                // intrinsic value of all options is lower than the price
                Real newSwapRate = minSwapRateIntersection[i] + intrinsicValueAddOn;
                if (newSwapRate > maxSwapRateIntersection[i])
                    newSwapRate = 0.5 * (minSwapRateIntersection[i] + maxSwapRateIntersection[i]);
                atmYoYSwapTimeRates_.second.push_back(newSwapRate);
                atmYoYSwapDateRates_.second.push_back(newSwapRate);
            } else {
                atmYoYSwapTimeRates_.first.push_back(tmpSwapMaturities[counter]);
                atmYoYSwapTimeRates_.second.push_back(tmpSwapRates[counter]);
                atmYoYSwapDateRates_.first.push_back(
                    yoyOptionDateFromTenor(cfMaturities_.at(counter)));
                atmYoYSwapDateRates_.second.push_back(tmpSwapRates[counter]);
                counter++;
            }
        }

        // create the swap curve using the factory
        atmYoYSwapRateCurve_ =
            interpolator1d_.interpolate(atmYoYSwapTimeRates_.first.begin(),
                                        atmYoYSwapTimeRates_.first.end(),
                                        atmYoYSwapTimeRates_.second.begin());
    }


    template<class I2D, class I1D>
    void InterpolatedYoYCapFloorTermPriceSurface<I2D,I1D>::
    calculateYoYTermStructure() const {

        // which yoy-swap points to use in building the yoy-fwd curve?
        // for now pick every year
        Size nYears = (Size)std::lround(timeFromReference(referenceDate()+cfMaturities_.back()));

        std::vector<ext::shared_ptr<BootstrapHelper<YoYInflationTermStructure> > > YYhelpers;
        for (Size i=1; i<=nYears; i++) {
            Date maturity = nominalTS_->referenceDate() + Period(i,Years);
            Handle<Quote> quote(ext::shared_ptr<Quote>(
                               new SimpleQuote( atmYoYSwapRate( maturity ) )));//!
            auto anInstrument =
                ext::make_shared<YearOnYearInflationSwapHelper>(
                                quote, observationLag(), maturity,
                                calendar(), bdc_, dayCounter(),
                                yoyIndex(),
                                this->indexIsInterpolated() ? CPI::Linear: CPI::Flat,
                                nominalTS_);
            YYhelpers.push_back (anInstrument);
        }

        Date baseDate =
            inflationPeriod(nominalTS_->referenceDate() - observationLag(),
                            yoyIndex()->frequency()).first;
        // usually this base rate is known
        // however for the data to be self-consistent
        // we pick this as the end of the curve
        Rate baseYoYRate = atmYoYSwapRate( referenceDate() );//!

        // Linear is OK because we have every year
        auto pYITS =
            ext::make_shared<PiecewiseYoYInflationCurve<Linear>>(
           