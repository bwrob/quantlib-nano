ze i = 0; i < cfMaturities_.size(); i++) {
            Time t = cfMaturityTimes_[i];
            // determine the sum of discount factors
            Size numYears = (Size)std::lround(t);
            Real sumDiscount = 0.0;
            for (Size j=0; j<numYears; ++j)
                sumDiscount += nominalTS_->discount(j + 1.0);
            // determine the minimum value of the ATM swap point
            Real tmpMinSwapRateIntersection = -1.e10;
            Real tmpMaxSwapRateIntersection = 1.e10;
            for (Size j=0; j<fStrikes_.size(); ++j) {
                Real price = floorPrice_(t,fStrikes_[j]);
                Real minSwapRate = fStrikes_[j] - price / (sumDiscount * 10000);
                if (minSwapRate > tmpMinSwapRateIntersection)
                    tmpMinSwapRateIntersection = minSwapRate;
            }
            for (Size j=0; j<cStrikes_.size(); ++j) {
                Real price = capPrice_(t,cStrikes_[j]);
                Real maxSwapRate = cStrikes_[j] + price / (sumDiscount * 10000);
                if (maxSwapRate < tmpMaxSwapRateIntersection)
                    tmpMaxSwapRateIntersection = maxSwapRate;
            }
            maxSwapRateIntersection[i] = tmpMaxSwapRateIntersection;
            minSwapRateIntersection[i] = tmpMinSwapRateIntersection;

            // find the interval where the intersection lies
            bool trialsExceeded = false;
            int numTrials = (int)(maxSearchRange / searchStep);
            if ( floorPrice_(t,fStrikes_.back()) > capPrice_(t,fStrikes_.back()) ) {
                int counter = 1;
                bool stop = false;
                Real strike = 0.0;
                while (!stop) {
                    strike = fStrikes_.back() - counter * searchStep;
                    if (floorPrice_(t, strike) < capPrice_(t, strike))
                        stop = true;
                    counter++;
                    if (counter == numTrials + 1) {
                        if (!stop) {
                            stop = true;
                            trialsExceeded = true;
                        }
                    }
                }
                lo = strike;
                hi = strike + searchStep;
            } else {
                int counter = 1;
                bool stop = false;
                Real strike = 0.0;
                while (!stop) {
                    strike = fStrikes_.back() + counter * searchStep;
                    if (floorPrice_(t, strike) > capPrice_(t, strike))
                        stop = true;
                    counter++;
                    if (counter == numTrials + 1) {
                        if (!stop) {
                            stop = true;
                            trialsExceeded = true;
                        }
                    }
                }
                lo = strike - searchStep;
                hi = strike;
            }

            guess = (hi+lo)/2.0;
            Rate kI = -999.999;

            if (!trialsExceeded) {
                try{
                    kI = solver.solve(  ObjectiveFunction(t, capPrice_, floorPrice_), solverTolerance_, guess, lo, hi );
                } catch( std::exception &e) {
                    QL_FAIL("cap/floor intersection finding failed at t = " << t << ", error msg: "<< e.what());
                }
                // error message if kI is economically nonsensical (only if t is large)
                if (kI <= minSwapRateIntersection[i]) {
                    if (t > maxExtrapolationMaturity)
                        QL_FAIL("cap/floor intersection finding failed at t = " << t <<
                                ", error msg: intersection value is below the arbitrage free lower bound "
                                << minSwapRateIntersection[i]);
                }
                else
                {
                    tmpSwapMaturities.push_back(t);
                    tmpSwapRates.push_back(kI);
                    validMaturity[i] = true;
         