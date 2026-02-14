 not know whether
         it represents Black, Bachelier or Displaced Diffusion
         variance.  These are virtual so alternate connections
         between const vol and total var are possible.

         Because inflation is highly linked to dates (for interpolation, periods, etc)
         we do NOT provide a time version
         */
        virtual Volatility totalVariance(const Date& exerciseDate,
                                         Rate strike,
                                         const Period &obsLag = Period(-1,Days),
                                         bool extrapolate = false) const;
        //! returns the total integrated variance for a given option tenor and strike rate
        virtual Volatility totalVariance(const Period& optionTenor,
                                         Rate strike,
                                         const Period &obsLag = Period(-1,Days),
                                         bool extrapolate = false) const;

        //! The TS observes with a lag that is usually different from the
        //! availability lag of the index.  An inflation rate is given,
        //! by default, for the maturity requested assuming this lag.
        virtual Period observationLag() const { return observationLag_; }
        virtual Frequency frequency() const { return frequency_; }
        virtual bool indexIsInterpolated() const { return indexIsInterpolated_; }
        virtual Date baseDate() const;
        //! base date will be in the past because of observation lag
        virtual Time timeFromBase(const Date &date,
                                  const Period& obsLag = Period(-1,Days)) const;
        //@}

        //! \name Limits
        //@{
        //! the minimum strike for which the term structure can return vols
        Real minStrike() const override = 0;
        //! the maximum strike for which the term structure can return vols
        Real maxStrike() const override = 0;
        //@}

        // acts as zero time value for boostrapping
        virtual Volatility baseLevel() const {
            QL_REQUIRE(baseLevel_ != Null<Volatility>(),
                       "Base volatility, for baseDate(), not set.");
            return baseLevel_;
        }

    protected:
        virtual void checkRange(const Date &, Rate strike, bool extrapolate) const;
        virtual void checkRange(Time, Rate strike, bool extrapolate) const;

        //! Implements the actual volatility surface calculation in
        //! derived classes e.g. bilinear interpolation.  N.B. does
        //! not derive the surface.
        virtual Volatility volatilityImpl(Time length,
                                          Rate strike) const = 0;

        // acts as zero time value for boostrapping
        virtual void setBaseLevel(Volatility v) { baseLevel_ = v; }
        mutable Volatility baseLevel_;

        // so you do not need an index
        Period observationLag_;
        Frequency frequency_;
        bool indexIsInterpolated_;
        VolatilityType volType_;
        Real displacement_;
    };


    //! Constant surface, no K or T dependence.
    class ConstantYoYOptionletVolatility
    : public YoYOptionletVolatilitySurface {
    public:
        //! \name Constructors
        //@{
        //! calculate the reference date based on the global evaluation date
        ConstantYoYOptionletVolatility(Volatility v,
                                       Natural settlementDays,
                                       const Calendar&,
                                       BusinessDayConvention bdc,
                                       const DayCounter& dc,
                                       const Period& observationLag,
                                       Frequency frequency,
                                       bool indexIsInterpolated,
                                       Rate minStrike = -1.0,   // -100%
                                       Rate maxStrike = 100.0, // +10,000%
               