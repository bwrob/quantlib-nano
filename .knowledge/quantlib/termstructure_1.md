ce date calculation
        virtual Natural settlementDays() const;
        //@}
        //! \name Observer interface
        //@{
        void update() override;
        //@}
      protected:
        //! date-range check
        void checkRange(const Date& d,
                        bool extrapolate) const;
        //! time-range check
        void checkRange(Time t,
                        bool extrapolate) const;
        bool moving_ = false;
        mutable bool updated_ = true;
        Calendar calendar_;
      private:
        mutable Date referenceDate_;
        Natural settlementDays_;
        DayCounter dayCounter_;
    };

    // inline definitions

    inline DayCounter TermStructure::dayCounter() const {
        return dayCounter_;
    }

    inline Time TermStructure::maxTime() const {
        return timeFromReference(maxDate());
    }

    inline Calendar TermStructure::calendar() const {
        return calendar_;
    }

    inline Natural TermStructure::settlementDays() const {
        QL_REQUIRE(settlementDays_!=Null<Natural>(),
                   "settlement days not provided for this instance");
        return settlementDays_;
    }

    inline Time TermStructure::timeFromReference(const Date& d) const {
        return dayCounter().yearFraction(referenceDate(), d);
    }

}

#endif
