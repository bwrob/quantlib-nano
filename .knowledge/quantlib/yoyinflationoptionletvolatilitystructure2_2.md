axStrike,
                                            Volatility baseYoYVolatility,
                                            const Interpolator1D &i)
    : YoYOptionletVolatilitySurface(settlementDays, cal, bdc, dc, lag,
                                    frequency, indexIsInterpolated),
      InterpolatedCurve<Interpolator1D>(i),
      minStrike_(minStrike), maxStrike_(maxStrike) {
        // don't have the data yet except for the base volatility
        // must set to communicate with bootstrap
        setBaseLevel(baseYoYVolatility);
    }



    //! For the curve strike is ignored because the smile is (can only be) flat.
    template<class Interpolator1D>
    inline Volatility InterpolatedYoYOptionletVolatilityCurve<Interpolator1D>::
    volatilityImpl(const Time t,
                   Rate) const {
        return this->interpolation_(t);
    }

} // namespace QuantLib

#endif