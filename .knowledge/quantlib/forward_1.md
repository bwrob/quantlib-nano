mpliedYield should reproduce the
            spot repo rate. For FRA's, this should reproduce the
            relevant zero rate at the FRA's maturityDate_;
        */
        InterestRate impliedYield(Real underlyingSpotValue,
                                  Real forwardValue,
                                  Date settlementDate,
                                  Compounding compoundingConvention,
                                  const DayCounter& dayCounter);
        //@}
      protected:
        Forward(DayCounter dayCounter,
                Calendar calendar,
                BusinessDayConvention businessDayConvention,
                Natural settlementDays,
                ext::shared_ptr<Payoff> payoff,
                const Date& valueDate,
                const Date& maturityDate,
                Handle<YieldTermStructure> discountCurve = Handle<YieldTermStructure>());

        void performCalculations() const override;
        /*! derived classes must set this, typically via spotIncome() */
        mutable Real underlyingIncome_;
        /*! derived classes must set this, typically via spotValue() */
        mutable Real underlyingSpotValue_;

        DayCounter dayCounter_;
        Calendar calendar_;
        BusinessDayConvention businessDayConvention_;
        Natural settlementDays_;
        ext::shared_ptr<Payoff> payoff_;
        /*! valueDate = settlement date (date the fwd contract starts
            accruing)
        */
        Date valueDate_;
        //! maturityDate of the forward contract or delivery date of underlying
        Date maturityDate_;
        Handle<YieldTermStructure> discountCurve_;
        /*! must set this in derived classes, based on particular underlying */
        Handle<YieldTermStructure> incomeDiscountCurve_;
    };


    //! Class for forward type payoffs
    class ForwardTypePayoff : public Payoff {
      public:
        ForwardTypePayoff(Position::Type type, Real strike)
        : type_(type),strike_(strike) {
            QL_REQUIRE(strike >= 0.0,"negative strike given");
        }
        Position::Type forwardType() const { return type_; };
        Real strike() const { return strike_; };
        //! \name Payoff interface
        //@{
        std::string name() const override { return "Forward"; }
        std::string description() const override;
        Real operator()(Real price) const override;
        //@}
      protected:
        Position::Type type_;
        Real strike_;
    };



    // inline definitions

    inline const Calendar& Forward::calendar() const {
        return calendar_;
    }

    inline BusinessDayConvention Forward::businessDayConvention() const {
        return businessDayConvention_;
    }

    inline const DayCounter& Forward::dayCounter() const {
        return dayCounter_;
    }

    inline Handle<YieldTermStructure> Forward::discountCurve() const {
        return discountCurve_;
    }

    inline Handle<YieldTermStructure> Forward::incomeDiscountCurve() const {
        return incomeDiscountCurve_;
    }


    inline std::string ForwardTypePayoff::description() const {
        std::ostringstream result;
        result << name() << ", " << strike() << " strike";
        return result.str();
    }

    inline Real ForwardTypePayoff::operator()(Real price) const {
        switch (type_) {
          case Position::Long:
            return (price-strike_);
          case Position::Short:
            return (strike_-price);
          default:
            QL_FAIL("unknown/illegal position type");
        }
    }

}


#endif
