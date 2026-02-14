xStrike() const override;
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
        const std::vector<Rate>& strikes() const;
        //@}
      protected:
        Volatility volatilityImpl(Time t, Rate strike) const override;

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

        Size nStrikes_;
        std::vector<Rate> strikes_;

        std::vector<std::vector<Handle<Quote> > > volHandles_;
        mutable Matrix vols_;

        // make it not mutable if possible
        mutable Interpolation2D interpolation_;
    };

    // inline definitions

    inline Date CapFloorTermVolSurface::maxDate() const {
        calculate();
        return optionDateFromTenor(optionTenors_.back());
    }

    inline Real CapFloorTermVolSurface::minStrike() const {
        return strikes_.front();
    }

    inline Real CapFloorTermVolSurface::maxStrike() const {
        return strikes_.back();
    }

    inline
    Volatility CapFloorTermVolSurface::volatilityImpl(Time t,
                                                      Rate strike) const {
        calculate();
        return interpolation_(strike, t, true);
    }

    inline
    const std::vector<Period>& CapFloorTermVolSurface::optionTenors() const {
        return optionTenors_;
    }

    inline
    const std::vector<Date>& CapFloorTermVolSurface::optionDates() const {
        // what if quotes are not available?
        calculate();
        return optionDates_;
    }

    inline
    const std::vector<Time>& CapFloorTermVolSurface::optionTimes() const {
        // what if quotes are not available?
        calculate();
        return optionTimes_;
    }

    inline const std::vector<Rate>& CapFloorTermVolSurface::strikes() const {
        return strikes_;
    }
}

#endif