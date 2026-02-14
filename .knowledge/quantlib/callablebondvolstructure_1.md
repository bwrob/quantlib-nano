red_ptr<SmileSection> smileSection(
                                              const Date& optionDate,
                                              const Period& bondTenor) const {
            const std::pair<Time, Time> p = convertDates(optionDate, bondTenor);
            return smileSectionImpl(p.first, p.second);
        }

        //! returns the volatility for a given option tenor and bond tenor
        Volatility volatility(const Period& optionTenor,
                              const Period& bondTenor,
                              Rate strike,
                              bool extrapolate = false) const;
        //! returns the Black variance for a given option tenor and bond tenor
        Real blackVariance(const Period& optionTenor,
                           const Period& bondTenor,
                           Rate strike,
                           bool extrapolate = false) const;
        ext::shared_ptr<SmileSection> smileSection(
                                               const Period& optionTenor,
                                               const Period& bondTenor) const;
        //@}
        //! \name Limits
        //@{
        //! the largest length for which the term structure can return vols
        virtual const Period& maxBondTenor() const = 0;
        //! the largest bondLength for which the term structure can return vols
        virtual Time maxBondLength() const;
        //! the minimum strike for which the term structure can return vols
        virtual Rate minStrike() const = 0;
        //! the maximum strike for which the term structure can return vols
        virtual Rate maxStrike() const = 0;
        //@}
        //! implements the conversion between dates and times
        virtual std::pair<Time,Time> convertDates(
                                               const Date& optionDate,
                                               const Period& bondTenor) const;
        //! the business day convention used for option date calculation
        virtual BusinessDayConvention businessDayConvention() const;
        //! implements the conversion between optionTenors and optionDates
        Date optionDateFromTenor(const Period& optionTenor) const;
    protected:

        //! return smile section
        virtual ext::shared_ptr<SmileSection> smileSectionImpl(
                                                   Time optionTime,
                                                   Time bondLength) const = 0;

        //! implements the actual volatility calculation in derived classes
        virtual Volatility volatilityImpl(Time optionTime,
                                          Time bondLength,
                                          Rate strike) const = 0;
        virtual Volatility volatilityImpl(const Date& optionDate,
                                          const Period& bondTenor,
                                          Rate strike) const {
            const std::pair<Time, Time> p = convertDates(optionDate, bondTenor);
            return volatilityImpl(p.first, p.second, strike);
        }
        void checkRange(Time, Time, Rate strike, bool extrapolate) const;
        void checkRange(const Date& optionDate,
                        const Period& bondTenor,
                        Rate strike, bool extrapolate) const;
      private:
        BusinessDayConvention bdc_;
    };


    // inline definitions

    inline BusinessDayConvention
    CallableBondVolatilityStructure::businessDayConvention() const {
        return bdc_;
    }

    inline Date CallableBondVolatilityStructure::optionDateFromTenor(
                                            const Period& optionTenor) const {
        return calendar().advance(referenceDate(),
                                  optionTenor,
                                  businessDayConvention());
    }

    inline Volatility CallableBondVolatilityStructure::volatility(
                                                     Time optionTime,

