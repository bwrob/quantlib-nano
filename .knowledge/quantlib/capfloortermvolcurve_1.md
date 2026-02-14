maxDate() const override;
        //@}
        //! \name VolatilityTermStructure interface
        //@{
        Real minStrike() const override;
        Real maxStrike() const override;
        //@}
        //! \name LazyObject interface
        //@{
        void update() override;
        void performCalculations() const override;
        //@}
        //! \name some inspectors
        //@{
        const std::vector<Period>& optionTenors() const;
        const std::vector<Date>& optionDates() const;
        const std::vector<Time>& optionTimes() const;
        //@}
      protected:
        Volatility volatilityImpl(Time length, Rate) const override;

      private:
        void checkInputs() const;
        void initializeOptionDatesAndTimes() const;
        void registerWithMarketData();
        void interpolate();

        Size nOptionTenors_;
        std::vector<Period> optionTenors_;
        mutable std::vector<Date> optionDates_;
        mutable std::vector<Time> optionTimes_;
        Date evaluationDate_;

        std::vector<Handle<Quote> > volHandles_;
        mutable std::vector<Volatility> vols_;

        // make it not mutable if possible
        mutable Interpolation interpolation_;
    };

    // inline definitions

    inline Date CapFloorTermVolCurve::maxDate() const {
        calculate();
        return optionDateFromTenor(optionTenors_.back());
    }

    inline Real CapFloorTermVolCurve::minStrike() const {
        return QL_MIN_REAL;
    }

    inline Real CapFloorTermVolCurve::maxStrike() const {
        return QL_MAX_REAL;
    }

    inline
    Volatility CapFloorTermVolCurve::volatilityImpl(Time t,
                                                    Rate) const {
        calculate();
        return interpolation_(t, true);
    }

    inline
    const std::vector<Period>& CapFloorTermVolCurve::optionTenors() const {
        return optionTenors_;
    }

    inline
    const std::vector<Date>& CapFloorTermVolCurve::optionDates() const {
        // what if quotes are not available?
        calculate();
        return optionDates_;
    }

    inline
    const std::vector<Time>& CapFloorTermVolCurve::optionTimes() const {
        // what if quotes are not available?
        calculate();
        return optionTimes_;
    }

}

#endif