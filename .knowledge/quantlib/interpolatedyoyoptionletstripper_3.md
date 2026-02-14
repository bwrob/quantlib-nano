          }
            // ***bootstrap***
            // this is the artificial vol at zero so that first section works
            Real Tmin = s->timeFromReference(s->yoyOptionDateFromTenor(TPmin));
            Volatility baseYoYVolatility = found - slope * Tmin * found;
            Rate eps = std::max(K, 0.02) / 1000.0;
            Rate minStrike = K-eps;
            Rate maxStrike = K+eps;
            ext::shared_ptr<
                PiecewiseYoYOptionletVolatilityCurve<Interpolator1D> > testPW(
                new PiecewiseYoYOptionletVolatilityCurve<Interpolator1D>(
                                            settlementDays, cal, bdc, dc, lag_,
                                            frequency_, indexIsInterpolated_,
                                            minStrike, maxStrike,
                                            baseYoYVolatility,
                                            helperInstruments) );
            testPW->recalculate();
            volCurves_.push_back(testPW);
        }
    }


    template <class Interpolator1D>
    std::pair<std::vector<Rate>, std::vector<Volatility> >
    InterpolatedYoYOptionletStripper<Interpolator1D>::slice(
                                                        const Date &d) const {

        const std::vector<Real>& Ks = strikes();

        const Size nK = Ks.size();

        std::pair<std::vector<Rate>, std::vector<Volatility> > result =
            std::make_pair(std::vector<Rate>(nK), std::vector<Volatility>(nK));

        for (Size i = 0; i < nK; i++) {
            Rate K = Ks[i];
            Volatility v = volCurves_[i]->volatility(d, K);
            result.first[i] = K;
            result.second[i] = v;
        }

        return result;
    }

}

#endif