,
                       Currency currency);

        //! \name Index interface
        //@{
        std::string name() const override;

        /*! Inflation indices are not associated to a particular day,
            but to months or quarters.  Therefore, they do not have
            fixing calendars.  Since we're forced by the base `Index`
            interface to add one, this method returns a NullCalendar
            instance.
        */
        Calendar fixingCalendar() const override;
        bool isValidFixingDate(const Date&) const override { return true; }

        /*! Forecasting index values requires an inflation term
            structure, with a base date that is earlier than its asof
            date.  This must be so because indices are available only
            with a lag.  Usually, it makes sense for the base date to
            be the first day of the month of the last published
            fixing.
        */
        Real fixing(const Date& fixingDate, bool forecastTodaysFixing = false) const override = 0;

        //! returns a past fixing at the given date
        Real pastFixing(const Date& fixingDate) const override = 0;

        void addFixing(const Date& fixingDate, Rate fixing, bool forceOverwrite = false) override;
        //@}

        //! \name Inspectors
        //@{
        std::string familyName() const;
        Region region() const;
        bool revised() const;
        Frequency frequency() const;
        /*! The availability lag describes when the index might be
            available; for instance, the inflation value for January
            may only be available in April.  This doesn't mean that
            that inflation value is considered as the April fixing; it
            remains the January fixing, independently of the lag in
            availability.
        */
        Period availabilityLag() const;
        Currency currency() const;
        //@}

      protected:
        Date referenceDate_;
        std::string familyName_;
        Region region_;
        bool revised_;
        Frequency frequency_;
        Period availabilityLag_;
        Currency currency_;

      private:
        std::string name_;
    };


    //! Base class for zero inflation indices.
    class ZeroInflationIndex : public InflationIndex {
      public:
        ZeroInflationIndex(
            const std::string& familyName,
            const Region& region,
            bool revised,
            Frequency frequency,
            const Period& availabilityLag,
            const Currency& currency,
            Handle<ZeroInflationTermStructure> ts = {});

        //! \name Index interface
        //@{
        /*! \warning the forecastTodaysFixing parameter (required by
                     the Index interface) is currently ignored.
        */
        Real fixing(const Date& fixingDate, bool forecastTodaysFixing = false) const override;
        Real pastFixing(const Date& fixingDate) const override;
        //@}
        //! \name Other methods
        //@{
        Date lastFixingDate() const;
        Handle<ZeroInflationTermStructure> zeroInflationTermStructure() const;
        ext::shared_ptr<ZeroInflationIndex> clone(const Handle<ZeroInflationTermStructure>& h) const;
        bool needsForecast(const Date& fixingDate) const;
        //@}
      private:
        Real forecastFixing(const Date& fixingDate) const;
        Handle<ZeroInflationTermStructure> zeroInflation_;
    };


    //! Base class for year-on-year inflation indices.
    /*! These may be quoted indices published on, say, Bloomberg, or can be
        defined as the ratio of an index at different time points.
    */
    class YoYInflationIndex : public InflationIndex {
      public:
        //! \name Constructors
        //@{
        //! Constructor for year-on-year indices defined as a ratio.
        /*! An index build with this constructor won't store
            past fixings of its own; they will be calculated as a
            ratio from the past fi