       Real blackVariance(const Date& optionDate,
                           Rate strike,
                           bool extrapolate = false) const;
        //! returns the Black variance for a given option time and strike rate
        Real blackVariance(Time optionTime,
                           Rate strike,
                           bool extrapolate = false) const;

        //! returns the smile for a given option tenor
        ext::shared_ptr<SmileSection> smileSection(const Period& optionTenor,
                                                     bool extr = false) const;
        //! returns the smile for a given option date
        ext::shared_ptr<SmileSection> smileSection(const Date& optionDate,
                                                     bool extr = false) const;
        //! returns the smile for a given option time
        ext::shared_ptr<SmileSection> smileSection(Time optionTime,
                                                     bool extr = false) const;
        //@}
        virtual VolatilityType volatilityType() const;
        virtual Real displacement() const;

      protected:
        virtual ext::shared_ptr<SmileSection> smileSectionImpl(
                                                const Date& optionDate) const;
        //! implements the actual smile calculation in derived classes
        virtual ext::shared_ptr<SmileSection> smileSectionImpl(
                                                    Time optionTime) const = 0;
        virtual Volatility volatilityImpl(const Date& optionDate,
                                          Rate strike) const;
        //! implements the actual volatility calculation in derived classes
        virtual Volatility volatilityImpl(Time optionTime,
                                          Rate strike) const = 0;
    };

    // inline definitions

    // 1. Period-based methods convert Period to Date and then
    //    use the equivalent Date-based methods
    inline Volatility
    OptionletVolatilityStructure::volatility(const Period& optionTenor,
                                             Rate strike,
                                             bool extrapolate) const {
        Date optionDate = optionDateFromTenor(optionTenor);
        return volatility(optionDate, strike, extrapolate);
    }

    inline
    Real OptionletVolatilityStructure::blackVariance(const Period& optionTenor,
                                                     Rate strike,
                                                     bool extrapolate) const {
        Date optionDate = optionDateFromTenor(optionTenor);
        return blackVariance(optionDate, strike, extrapolate);
    }

    inline ext::shared_ptr<SmileSection>
    OptionletVolatilityStructure::smileSection(const Period& optionTenor,
                                               bool extrapolate) const {
        Date optionDate = optionDateFromTenor(optionTenor);
        return smileSection(optionDate, extrapolate);
    }

    // 2. blackVariance methods rely on volatility methods
    inline
    Real OptionletVolatilityStructure::blackVariance(const Date& optionDate,
                                                     Rate strike,
                                                     bool extrapolate) const {
        Volatility v = volatility(optionDate, strike, extrapolate);
        Time t = timeFromReference(optionDate);
        return v*v*t;
    }

    inline
    Real OptionletVolatilityStructure::blackVariance(Time optionTime,
                                                     Rate strike,
                                                     bool extrapolate) const {
        Volatility v = volatility(optionTime, strike, extrapolate);
        return v*v*optionTime;
    }

    // 3. relying on xxxImpl methods
    inline Volatility
    OptionletVolatilityStructure::volatility(const Date& optionDate,
                                             Rate strike,
                                             bool extrapolate) 