                        VolatilityType volType = ShiftedLognormal,
                                       Real displacement = 0.0);

        // costructor taking a quote
        ConstantYoYOptionletVolatility(Handle<Quote> v,
                                       Natural settlementDays,
                                       const Calendar&,
                                       BusinessDayConvention bdc,
                                       const DayCounter& dc,
                                       const Period& observationLag,
                                       Frequency frequency,
                                       bool indexIsInterpolated,
                                       Rate minStrike = -1.0,  // -100%
                                       Rate maxStrike = 100.0, // +10,000%
                                       VolatilityType volType = ShiftedLognormal,
                                       Real displacement = 0.0);
        //@}

        //! \name Limits
        //@{
        Date maxDate() const override { return Date::maxDate(); }
        //! the minimum strike for which the term structure can return vols
        Real minStrike() const override { return minStrike_; }
        //! the maximum strike for which the term structure can return vols
        Real maxStrike() const override { return maxStrike_; }
        //@}
    protected:
        //! implements the actual volatility calculation in derived classes
      Volatility volatilityImpl(Time length, Rate strike) const override;

      Handle<Quote> volatility_;
      Rate minStrike_, maxStrike_;
    };



} // namespace QuantLib

#endif
