obability of default between two given times
        Probability defaultProbability(Time,
                                       Time,
                                       bool extrapo = false) const;
        //@}

        /*! \name Default densities

            These methods return the default density at a given date or time.
            In the latter case, the time is calculated as a fraction of year
            from the reference date.
        */
        //@{
        Real defaultDensity(const Date& d,
                            bool extrapolate = false) const;
        Real defaultDensity(Time t,
                            bool extrapolate = false) const;
        //@}

        /*! \name Hazard rates

            These methods returns the hazard rate at a given date or time.
            In the latter case, the time is calculated as a fraction of year
            from the reference date.
            
            Hazard rates are defined with annual frequency and continuous
            compounding.
        */

        //@{
        Rate hazardRate(const Date& d,
                        bool extrapolate = false) const;
        Rate hazardRate(Time t,
                        bool extrapolate = false) const;
        //@}

        //! \name Jump inspectors
        //@{
        const std::vector<Date>& jumpDates() const;
        const std::vector<Time>& jumpTimes() const;
        //@}

        //! \name Observer interface
        //@{
        void update() override;
        //@}
      protected:
        /*! \name Calculations
            The first two methods must be implemented in derived classes to
            perform the actual calculations. When they are called,
            range check has already been performed; therefore, they
            must assume that extrapolation is required.
            The third method has a default implementation which can be
            overridden with a more efficient implementation in derived
            classes.
        */
        //@{
        //! survival probability calculation
        virtual Probability survivalProbabilityImpl(Time) const = 0;
        //! default density calculation
        virtual Real defaultDensityImpl(Time) const = 0;
        //! hazard rate calculation
        virtual Real hazardRateImpl(Time) const;
        //@}
      private:
        // methods
        void setJumps();
        // data members
        std::vector<Handle<Quote> > jumps_;
        std::vector<Date> jumpDates_;
        std::vector<Time> jumpTimes_;
        Size nJumps_;
        Date latestReference_;
    };

    // inline definitions

    inline
    Probability DefaultProbabilityTermStructure::survivalProbability(
                                                     const Date& d,
                                                     bool extrapolate) const {
        return survivalProbability(timeFromReference(d), extrapolate);
    }

    inline
    Probability DefaultProbabilityTermStructure::defaultProbability(
                                                     const Date& d,
                                                     bool extrapolate) const {
        return 1.0 - survivalProbability(d, extrapolate);
    }

    inline
    Probability DefaultProbabilityTermStructure::defaultProbability(
                                                     Time t,
                                                     bool extrapolate) const {
        return 1.0 - survivalProbability(t, extrapolate);
    }

    inline
    Real DefaultProbabilityTermStructure::defaultDensity(
                                                     const Date& d,
                                                     bool extrapolate) const {
        return defaultDensity(timeFromReference(d), extrapolate);
    }

    inline
    Real DefaultProbabilityTermStructure::defaultDensity(
                                                     Time t,
                                                     bool extrapolate) const {
        checkRa