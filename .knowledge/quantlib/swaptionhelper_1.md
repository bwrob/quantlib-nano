                       VolatilityType type = ShiftedLognormal,
                       Real shift = 0.0,
                       Natural settlementDays = Null<Size>(),
                       RateAveraging::Type averagingMethod = RateAveraging::Compound);

        void addTimesTo(std::list<Time>& times) const override;
        Real modelValue() const override;
        Real blackPrice(Volatility volatility) const override;

        const ext::shared_ptr<FixedVsFloatingSwap>& underlying() const {
            calculate();
            return swap_;
        }
        ext::shared_ptr<Swaption> swaption() const { calculate(); return swaption_; }

      private:
        void performCalculations() const override;
        ext::shared_ptr<FixedVsFloatingSwap> makeSwap(Schedule fixedSchedule,
                                                      Schedule floatSchedule,
                                                      Rate exerciseRate,
                                                      Swap::Type type) const;
        mutable Date exerciseDate_, endDate_;
        const Period maturity_, length_, fixedLegTenor_;
        const ext::shared_ptr<IborIndex> index_;
        const Handle<YieldTermStructure> termStructure_;
        const DayCounter fixedLegDayCounter_, floatingLegDayCounter_;
        const Real strike_, nominal_;
        const Natural settlementDays_;
        const RateAveraging::Type averagingMethod_;
        mutable Rate exerciseRate_;
        mutable ext::shared_ptr<FixedVsFloatingSwap> swap_;
        mutable ext::shared_ptr<Swaption> swaption_;
    };

}

#endif
