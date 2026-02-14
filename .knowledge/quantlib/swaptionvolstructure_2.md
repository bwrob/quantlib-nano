ol extr = false) const;
        //! returns the smile for a given option time and swap tenor
        ext::shared_ptr<SmileSection> smileSection(Time optionTime,
                                                     const Period& swapTenor,
                                                     bool extr = false) const;
        //! returns the smile for a given option tenor and swap length
        ext::shared_ptr<SmileSection> smileSection(const Period& optionTenor,
                                                     Time swapLength,
                                                     bool extr = false) const;
        //! returns the smile for a given option date and swap length
        ext::shared_ptr<SmileSection> smileSection(const Date& optionDate,
                                                     Time swapLength,
                                                     bool extr = false) const;
        //! returns the smile for a given option time and swap length
        ext::shared_ptr<SmileSection> smileSection(Time optionTime,
                                                     Time swapLength,
                                                     bool extr = false) const;
        //@}
        //! \name Limits
        //@{
        //! the largest length for which the term structure can return vols
        virtual const Period& maxSwapTenor() const = 0;
        //! the largest swapLength for which the term structure can return vols
        Time maxSwapLength() const;
        //@}
        //@{
        //! volatility type
        virtual VolatilityType volatilityType() const {
            return ShiftedLognormal;
        }
        //@}
        //! implements the conversion between swap tenor and swap (time) length
        Time swapLength(const Period& swapTenor) const;
        //! implements the conversion between swap dates and swap (time) length
        Time swapLength(const Date& start,
                        const Date& end) const;
      protected:
        virtual ext::shared_ptr<SmileSection> smileSectionImpl(
                                                const Date& optionDate,
                                                const Period& swapTenor) const;
        virtual ext::shared_ptr<SmileSection> smileSectionImpl(
                                                Time optionTime,
                                                Time swapLength) const = 0;
        virtual Volatility volatilityImpl(const Date& optionDate,
                                          const Period& swapTenor,
                                          Rate strike) const;
        virtual Volatility volatilityImpl(Time optionTime,
                                          Time swapLength,
                                          Rate strike) const = 0;
        virtual Real shiftImpl(const Date &optionDate,
                               const Period &swapTenor) const;
        virtual Real shiftImpl(Time optionTime, Time swapLength) const;
        void checkSwapTenor(const Period& swapTenor,
                            bool extrapolate) const;
        void checkSwapTenor(Time swapLength,
                            bool extrapolate) const;
    };

    // inline definitions

    // 1. methods with Period-denominated exercise convert Period to Date and then
    //    use the equivalent Date-denominated exercise methods
    inline Volatility
    SwaptionVolatilityStructure::volatility(const Period& optionTenor,
                                            const Period& swapTenor,
                                            Rate strike,
                                            bool extrapolate) const {
        Date optionDate = optionDateFromTenor(optionTenor);
        return volatility(optionDate, swapTenor, strike, extrapolate);
    }

    inline Volatility
    SwaptionVolatilityStructure::volatility(const Period& optionTenor,
                                            Time swapLength,
                                            Rate strik
