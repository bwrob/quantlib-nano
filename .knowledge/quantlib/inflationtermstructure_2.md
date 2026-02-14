flationTermStructure(Natural settlementDays,
                                  const Calendar& calendar,
                                  Date baseDate,
                                  Rate baseYoYRate,
                                  Frequency frequency,
                                  const DayCounter& dayCounter,
                                  const ext::shared_ptr<Seasonality>& seasonality = {});
        //@}

        //! \name Inspectors
        //@{
        //! year-on-year inflation rate.
        /*! This does not return the year-on-year swap (YYIIS) rate.
            If you need that rate, retrieve it from the corresponding
            instrument instead.
        */
        Rate yoyRate(const Date& d, bool extrapolate = false) const;

        /*! \deprecated Use the overload without a lag instead.
                        Deprecated in version 1.41.
        */
        [[deprecated("Use the overload without a lag instead")]]
        Rate yoyRate(const Date& d, const Period& instObsLag,
                     bool forceLinearInterpolation = false,
                     bool extrapolate = false) const;

        //! year-on-year inflation rate.
        /*! \warning Since inflation is highly linked to dates (lags,
                     interpolation, months for seasonality, etc) this
                     method cannot account for all effects.  If you
                     call it, You'll have to manage lag, seasonality
                     etc. yourself.
        */
        Rate yoyRate(Time t,
                     bool extrapolate = false) const;
        //@}

      protected:
        //! to be defined in derived classes
        virtual Rate yoyRateImpl(Time time) const = 0;
    };


    //! utility function giving the inflation period for a given date
    std::pair<Date,Date> inflationPeriod(const Date&,
                                         Frequency);

    //! utility function giving the time between two dates depending on
    //! index frequency and interpolation, and a day counter
    Time inflationYearFraction(Frequency ,
                               bool indexIsInterpolated,
                               const DayCounter&,
                               const Date&, const Date&);


    // inline

    inline Period InflationTermStructure::observationLag() const {
        QL_DEPRECATED_DISABLE_WARNING
        return observationLag_;
        QL_DEPRECATED_ENABLE_WARNING
    }

    inline Frequency InflationTermStructure::frequency() const {
        return frequency_;
    }

    inline Rate InflationTermStructure::baseRate() const {
        QL_REQUIRE(baseRate_ != Null<Real>(), "base rate not available");
        return baseRate_;
    }

    inline ext::shared_ptr<Seasonality> InflationTermStructure::seasonality() const {
        return seasonality_;
    }

    inline bool InflationTermStructure::hasSeasonality() const {
        return static_cast<bool>(seasonality_);
    }

}

#endif
