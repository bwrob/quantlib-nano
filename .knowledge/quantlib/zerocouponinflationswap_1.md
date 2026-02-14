Calendar() const { return fixCalendar_; }
        BusinessDayConvention fixedConvention() const {
            return fixConvention_;
        }
        DayCounter dayCounter() const { return dayCounter_; }
        //! \f$ K \f$ in the above formula.
        Rate fixedRate() const { return fixedRate_; }
        ext::shared_ptr<ZeroInflationIndex> inflationIndex() const {
            return infIndex_;
        }
        Period observationLag() const { return observationLag_; }
        CPI::InterpolationType observationInterpolation() const {
            return observationInterpolation_;
        }
        bool adjustObservationDates() const { return adjustInfObsDates_; }
        Calendar inflationCalendar() const { return infCalendar_; }
        BusinessDayConvention inflationConvention() const {
            return infConvention_;
        }
        //! just one cashflow (that is not a coupon) in each leg
        const Leg& fixedLeg() const;
        //! just one cashflow (that is not a coupon) in each leg
        const Leg& inflationLeg() const;
        //@}

        //! \name Results
        //@{
        Real fixedLegNPV() const;
        Real fixedLegBPS() const;
        Real inflationLegNPV() const;
        Real fairRate() const;
        //@}

      protected:
        Type type_;
        Real nominal_;
        Date startDate_, maturityDate_;
        Calendar fixCalendar_;
        BusinessDayConvention fixConvention_;
        Rate fixedRate_;
        ext::shared_ptr<ZeroInflationIndex> infIndex_;
        Period observationLag_;
        CPI::InterpolationType observationInterpolation_;
        bool adjustInfObsDates_;
        Calendar infCalendar_;
        BusinessDayConvention infConvention_;
        DayCounter dayCounter_;
        Date baseDate_, obsDate_;
    };


    class ZeroCouponInflationSwap::arguments : public Swap::arguments {
      public:
        Rate fixedRate;
    };


    class ZeroCouponInflationSwap::engine
    : public GenericEngine<ZeroCouponInflationSwap::arguments,
                           ZeroCouponInflationSwap::results> {};

}


#endif