ality can be obtained by giving the same
        number of factors as the frequency dictates e.g. 12 for
        monthly seasonality.

        \warning Multi-year seasonality (i.e. non-stationary) is
                 fragile: the user <b>must</b> ensure that corrections
                 at whole years before and after the inflation term
                 structure base date are the same.  Otherwise there
                 can be an inconsistency with quoted rates.  This is
                 enforced if the frequency is lower than daily.  This
                 is not enforced for daily seasonality because this
                 will always be inconsistent due to weekends,
                 holidays, leap years, etc.  If you use multi-year
                 daily seasonality it is up to you to check.

        \note Factors are normalized relative to their appropriate
              reference dates.  For zero inflation this is the
              inflation curve true base date: since you have a fixing
              for that date the seasonality factor must be one.  For
              YoY inflation the reference is always one year earlier.

        Seasonality is treated as piecewise constant, hence it works
        correctly with uninterpolated indices if the seasonality
        correction factor frequency is the same as the index frequency
        (or less).
    */
    class MultiplicativePriceSeasonality : public Seasonality {

        private:
            Date seasonalityBaseDate_;
            Frequency frequency_;
            std::vector<Rate> seasonalityFactors_;

        public:

            //Constructors
            //
            MultiplicativePriceSeasonality() = default;

            MultiplicativePriceSeasonality(const Date& seasonalityBaseDate,
                                           Frequency frequency,
                                           const std::vector<Rate>& seasonalityFactors);

            virtual void set(const Date& seasonalityBaseDate,
                             Frequency frequency,
                             const std::vector<Rate>& seasonalityFactors);

            //! inspectors
            //@{
            virtual Date seasonalityBaseDate() const;
            virtual Frequency frequency() const;
            virtual std::vector<Rate> seasonalityFactors() const;
            //! The factor returned is NOT normalized relative to ANYTHING.
            virtual Rate seasonalityFactor(const Date &d) const;
            //@}

            //! \name Seasonality interface
            //@{
            Rate correctZeroRate(const Date& d,
                                 Rate r,
                                 const InflationTermStructure& iTS) const override;
            Rate
            correctYoYRate(const Date& d, Rate r, const InflationTermStructure& iTS) const override;
            bool isConsistent(const InflationTermStructure& iTS) const override;
            //@}

            //Destructor
            ~MultiplicativePriceSeasonality() override = default;
            ;

          protected:
            virtual void validate() const;
            virtual Rate seasonalityCorrection(Rate r, const Date &d, const DayCounter &dc,
                                               const Date &curveBaseDate, bool isZeroRate) const;
    };


    class KerkhofSeasonality : public MultiplicativePriceSeasonality {
      public:
        KerkhofSeasonality(const Date& seasonalityBaseDate,
                           const std::vector<Rate>& seasonalityFactors)
        : MultiplicativePriceSeasonality(seasonalityBaseDate,Monthly,
                                         seasonalityFactors) {}

        /*Rate correctZeroRate(const Date &d, const Rate r,
                               const InflationTermStructure& iTS) const;*/
        Real seasonalityFactor(const Date& to) const override;

      protected:
        Rate seasonalityCorrection(Rate rate,
                                   const Date& atDate,
                      