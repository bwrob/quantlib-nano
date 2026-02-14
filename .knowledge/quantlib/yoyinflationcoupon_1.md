ationLeg& withGearings(Real gearing);
      yoyInflationLeg& withGearings(const std::vector<Real>& gearings);
      yoyInflationLeg& withSpreads(Spread spread);
      yoyInflationLeg& withSpreads(const std::vector<Spread>& spreads);
      yoyInflationLeg& withCaps(Rate cap);
      yoyInflationLeg& withCaps(const std::vector<Rate>& caps);
      yoyInflationLeg& withFloors(Rate floor);
      yoyInflationLeg& withFloors(const std::vector<Rate>& floors);
      operator Leg() const;
    private:
        Schedule schedule_;
        ext::shared_ptr<YoYInflationIndex> index_;
        Period observationLag_;
        CPI::InterpolationType interpolation_;
        std::vector<Real> notionals_;
        DayCounter paymentDayCounter_;
        BusinessDayConvention paymentAdjustment_ = ModifiedFollowing;
        Calendar paymentCalendar_;
        std::vector<Natural> fixingDays_;
        std::vector<Real> gearings_;
        std::vector<Spread> spreads_;
        std::vector<Rate> caps_, floors_;
    };



}

#endif