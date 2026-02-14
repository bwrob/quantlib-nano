PriceWithSmile(Real strike,
                    Real initialValue,
                    Real expiry,
                    Real deflator) const;

        Real callSpreadPrice(Real previousInitialValue,
                            Real nextInitialValue,
                            Real previousStrike,
                            Real nextStrike,
                            Real deflator,
                            Real previousVariance,
                            Real nextVariance) const;

        Real smileCorrection(Real strike,
                               Real initialValue,
                               Real expiry,
                               Real deflator) const;

     private:
        Real correlation_;   // correlation between L(S) and L(T)
        bool withSmile_;
        bool byCallSpread_;

        ext::shared_ptr<SmileSection> smilesOnExpiry_;
        ext::shared_ptr<SmileSection> smilesOnPayment_;
        Real eps_ = 1.0e-8;
    };


    //! helper class building a sequence of range-accrual floating-rate coupons
    class RangeAccrualLeg {
      public:
        RangeAccrualLeg(Schedule schedule, ext::shared_ptr<IborIndex> index);
        RangeAccrualLeg& withNotionals(Real notional);
        RangeAccrualLeg& withNotionals(const std::vector<Real>& notionals);
        RangeAccrualLeg& withPaymentDayCounter(const DayCounter&);
        RangeAccrualLeg& withPaymentAdjustment(BusinessDayConvention);
        RangeAccrualLeg& withFixingDays(Natural fixingDays);
        RangeAccrualLeg& withFixingDays(const std::vector<Natural>& fixingDays);
        RangeAccrualLeg& withGearings(Real gearing);
        RangeAccrualLeg& withGearings(const std::vector<Real>& gearings);
        RangeAccrualLeg& withSpreads(Spread spread);
        RangeAccrualLeg& withSpreads(const std::vector<Spread>& spreads);
        RangeAccrualLeg& withLowerTriggers(Rate trigger);
        RangeAccrualLeg& withLowerTriggers(const std::vector<Rate>& triggers);
        RangeAccrualLeg& withUpperTriggers(Rate trigger);
        RangeAccrualLeg& withUpperTriggers(const std::vector<Rate>& triggers);
        RangeAccrualLeg& withObservationTenor(const Period&);
        RangeAccrualLeg& withObservationConvention(BusinessDayConvention);
        operator Leg() const;
      private:
        Schedule schedule_;
        ext::shared_ptr<IborIndex> index_;
        std::vector<Real> notionals_;
        DayCounter paymentDayCounter_;
        BusinessDayConvention paymentAdjustment_ = Following;
        std::vector<Natural> fixingDays_;
        std::vector<Real> gearings_;
        std::vector<Spread> spreads_;
        std::vector<Rate> lowerTriggers_, upperTriggers_;
        Period observationTenor_;
        BusinessDayConvention observationConvention_ = ModifiedFollowing;
    };

}


#endif