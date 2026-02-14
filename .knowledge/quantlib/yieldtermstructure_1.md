               Compounding comp,
                              Frequency freq = Annual,
                              bool extrapolate = false) const;
        //@}

        /*! \name Forward rates

            These methods returns the forward interest rate between two dates
            or times.  In the former case, times are calculated as fractions
            of year from the reference date.

            If both dates (times) are equal the instantaneous forward rate is
            returned.
        */
        //@{
        /*! The resulting interest rate has the required day-counting
            rule.
        */
        InterestRate forwardRate(const Date& d1,
                                 const Date& d2,
                                 const DayCounter& resultDayCounter,
                                 Compounding comp,
                                 Frequency freq = Annual,
                                 bool extrapolate = false) const;
        /*! The resulting interest rate has the required day-counting
            rule.
            \warning dates are not adjusted for holidays
        */
        InterestRate forwardRate(const Date& d,
                                 const Period& p,
                                 const DayCounter& resultDayCounter,
                                 Compounding comp,
                                 Frequency freq = Annual,
                                 bool extrapolate = false) const;

        /*! The resulting interest rate has the same day-counting rule
            used by the term structure. The same rule should be used
            for calculating the passed times t1 and t2.
        */
        InterestRate forwardRate(Time t1,
                                 Time t2,
                                 Compounding comp,
                                 Frequency freq = Annual,
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

            This method must be implemented in derived classes to
            perform the actual calculations. When it is called,
            range check has already been performed; therefore, it
            must assume that extrapolation is required.
        */
        //@{
        //! discount factor calculation
        virtual DiscountFactor discountImpl(Time) const = 0;
        //@}
      private:
        // methods
        void setJumps(const Date& referenceDate);
        // data members
        std::vector<Handle<Quote> > jumps_;
        std::vector<Date> jumpDates_;
        std::vector<Time> jumpTimes_;
        Size nJumps_ = 0;
        Date latestReference_;
    };

    // inline definitions

    inline
    DiscountFactor YieldTermStructure::discount(const Date& d,
                                                bool extrapolate) const {
        return discount(timeFromReference(d), extrapolate);
    }

    inline
    InterestRate YieldTermStructure::forwardRate(const Date& d,
                                                 const Period& p,
                                                 const DayCounter& dayCounter,
                                                 Compounding comp,
                                                 Frequency freq,
                                                 bool extrapolate) const {
        return forwardRate(d, d+p, dayCounter, comp, freq, extrapolate);
    }

    inline const std::vector<Date>& YieldTermStructure::jumpDates() const {
        return this->jumpDates_;
    }

    inline const std::vector<Time>& YieldTermStructure::jumpTimes() const {
        return this->jumpTimes_;
    }

}

#endif