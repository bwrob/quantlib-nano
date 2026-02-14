             ext::shared_ptr<ZeroInflationIndex> index,
               Real baseCPI,
               const Period& observationLag);
        CPILeg& withNotionals(Real notional);
        CPILeg& withNotionals(const std::vector<Real>& notionals);
        CPILeg& withFixedRates(Real fixedRate);
        CPILeg& withFixedRates(const std::vector<Real>& fixedRates);
        CPILeg& withPaymentDayCounter(const DayCounter&);
        CPILeg& withPaymentAdjustment(BusinessDayConvention);
        CPILeg& withPaymentCalendar(const Calendar&);
        CPILeg& withObservationInterpolation(CPI::InterpolationType);
        CPILeg& withSubtractInflationNominal(bool);
        CPILeg& withCaps(Rate cap);
        CPILeg& withCaps(const std::vector<Rate>& caps);
        CPILeg& withFloors(Rate floor);
        CPILeg& withFloors(const std::vector<Rate>& floors);
        CPILeg& withExCouponPeriod(const Period&,
                                         const Calendar&,
                                         BusinessDayConvention,
                                         bool endOfMonth = false);
        CPILeg& withBaseDate(const Date& baseDate);

        operator Leg() const;

      private:
        Schedule schedule_;
        ext::shared_ptr<ZeroInflationIndex> index_;
        Real baseCPI_;
        Period observationLag_;
        std::vector<Real> notionals_;
        std::vector<Real> fixedRates_;
        DayCounter paymentDayCounter_;
        BusinessDayConvention paymentAdjustment_ = ModifiedFollowing;
        Calendar paymentCalendar_;
        CPI::InterpolationType observationInterpolation_ = CPI::AsIndex;
        bool subtractInflationNominal_ = true;
        std::vector<Rate> caps_, floors_;
        Period exCouponPeriod_;
        Calendar exCouponCalendar_;
        BusinessDayConvention exCouponAdjustment_ = Following;
        bool exCouponEndOfMonth_ = false;
        Date baseDate_;
    };


    // inline definitions

    inline Real CPICoupon::fixedRate() const {
        return fixedRate_;
    }

    inline Rate CPICoupon::adjustedIndexGrowth() const {
        return rate()/fixedRate();
    }

    inline Rate CPICoupon::indexFixing() const {
        return CPI::laggedFixing(cpiIndex(), accrualEndDate(), observationLag(), observationInterpolation());
    }

    inline Rate CPICoupon::baseCPI() const {
        return baseCPI_;
    }

    inline Date CPICoupon::baseDate() const {
        return baseDate_;
    }

    inline CPI::InterpolationType CPICoupon::observationInterpolation() const {
        return observationInterpolation_;
    }

    inline ext::shared_ptr<ZeroInflationIndex> CPICoupon::cpiIndex() const {
        return ext::dynamic_pointer_cast<ZeroInflationIndex>(index());
    }


    inline ext::shared_ptr<ZeroInflationIndex> CPICashFlow::cpiIndex() const {
        return ext::dynamic_pointer_cast<ZeroInflationIndex>(index());
    }

}

#endif
