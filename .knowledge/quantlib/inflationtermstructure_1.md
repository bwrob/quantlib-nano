t::shared_ptr<Seasonality> seasonality_;

        /*! \deprecated Do not use; inflation curves always have an explicit
                        base date now.
                        Deprecated in version 1.39.
        */
        [[deprecated("Do not use; inflation curves always have an explicit base date now.")]]
        Period observationLag_;

        Frequency frequency_;
        mutable Rate baseRate_;
        // Can be set by subclasses that don't have baseDate available in constructors.
        Date baseDate_;
    };

    //! Interface for zero inflation term structures.
    class ZeroInflationTermStructure : public InflationTermStructure {
      public:
        //! \name Constructors
        //@{
        ZeroInflationTermStructure(Date baseDate,
                                   Frequency frequency,
                                   const DayCounter& dayCounter,
                                   const ext::shared_ptr<Seasonality>& seasonality = {});

        ZeroInflationTermStructure(const Date& referenceDate,
                                   Date baseDate,
                                   Frequency frequency,
                                   const DayCounter& dayCounter,
                                   const ext::shared_ptr<Seasonality>& seasonality = {});

        ZeroInflationTermStructure(Natural settlementDays,
                                   const Calendar& calendar,
                                   Date baseDate,
                                   Frequency frequency,
                                   const DayCounter& dayCounter,
                                   const ext::shared_ptr<Seasonality>& seasonality = {});
        //@}

        //! \name Inspectors
        //@{
        //! zero-coupon inflation rate.
        /*! The zero term structure uses yearly compounding, which is
            assumed for ZCIIS instrument quotes.

            If you want to get predictions of RPI/CPI/etc. use the
            corresponding index instead; if you need a ZCIIS rate,
            retrieve it from the instrument.
        */
        Rate zeroRate(const Date& d, bool extrapolate = false) const;

        /*! \deprecated Use the overload without a lag instead.
                        Deprecated in version 1.41.
        */
        [[deprecated("Use the overload without a lag instead")]]
        Rate zeroRate(const Date& d, const Period& instObsLag,
                      bool forceLinearInterpolation = false,
                      bool extrapolate = false) const;

        //! zero-coupon inflation rate.
        /*! \warning Since inflation is highly linked to dates (lags,
                     interpolation, months for seasonality, etc) this
                     method cannot account for all effects.  If you
                     call it, You'll have to manage lag, seasonality
                     etc. yourself.
        */
        Rate zeroRate(Time t,
                      bool extrapolate = false) const;
        //@}
      protected:
        //! to be defined in derived classes
        virtual Rate zeroRateImpl(Time t) const = 0;
    };


    //! Base class for year-on-year inflation term structures.
    class YoYInflationTermStructure : public InflationTermStructure {
      public:
        //! \name Constructors
        //@{
        YoYInflationTermStructure(Date baseDate,
                                  Rate baseYoYRate,
                                  Frequency frequency,
                                  const DayCounter& dayCounter,
                                  const ext::shared_ptr<Seasonality>& seasonality = {});

        YoYInflationTermStructure(const Date& referenceDate,
                                  Date baseDate,
                                  Rate baseYoYRate,
                                  Frequency frequency,
                                  const DayCounter& dayCounter,
                                  const ext::shared_ptr<Seasonality>& seasonality = {});

        YoYIn
