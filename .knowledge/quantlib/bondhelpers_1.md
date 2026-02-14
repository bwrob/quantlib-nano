            Real baseCPI,
                      const Period& observationLag,
                      const ext::shared_ptr<ZeroInflationIndex>& cpiIndex,
                      CPI::InterpolationType observationInterpolation,
                      Schedule schedule,
                      const std::vector<Rate>& fixedRate,
                      const DayCounter& accrualDayCounter,
                      BusinessDayConvention paymentConvention = Following,
                      const Date& issueDate = Date(),
                      const Calendar& paymentCalendar = Calendar(),
                      const Period& exCouponPeriod = Period(),
                      const Calendar& exCouponCalendar = Calendar(),
                      BusinessDayConvention exCouponConvention = Unadjusted,
                      bool exCouponEndOfMonth = false,
                      Bond::Price::Type priceType = Bond::Price::Clean);

        /*! \deprecated Use the overload without the growthOnly parameter.
                        Deprecated in version 1.40.
        */
        [[deprecated("Use the overload without the growthOnly parameter")]]
        CPIBondHelper(const Handle<Quote>& price,
                      Natural settlementDays,
                      Real faceAmount,
                      bool growthOnly,
                      Real baseCPI,
                      const Period& observationLag,
                      const ext::shared_ptr<ZeroInflationIndex>& cpiIndex,
                      CPI::InterpolationType observationInterpolation,
                      Schedule schedule,
                      const std::vector<Rate>& fixedRate,
                      const DayCounter& accrualDayCounter,
                      BusinessDayConvention paymentConvention = Following,
                      const Date& issueDate = Date(),
                      const Calendar& paymentCalendar = Calendar(),
                      const Period& exCouponPeriod = Period(),
                      const Calendar& exCouponCalendar = Calendar(),
                      BusinessDayConvention exCouponConvention = Unadjusted,
                      bool exCouponEndOfMonth = false,
                      Bond::Price::Type priceType = Bond::Price::Clean);

        //! \name Visitability
        //@{
        void accept(AcyclicVisitor&) override;
        //@}
    };


    // inline

    inline ext::shared_ptr<Bond> BondHelper::bond() const {
        return bond_;
    }

    inline Bond::Price::Type BondHelper::priceType() const {
        return priceType_;
    }


}

#endif