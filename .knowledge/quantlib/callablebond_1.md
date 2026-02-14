        //! the yield term structure divided by current dirty price
        Real effectiveDuration(Real oas,
                               const Handle<YieldTermStructure>& engineTS,
                               const DayCounter& dayCounter,
                               Compounding compounding,
                               Frequency frequency,
                               Real bump=2e-4);

        //! Calculate the effective convexity, i.e., the second
        //! differential of the dirty price w.r.t. a parallel shift of
        //! the yield term structure divided by current dirty price
        Real effectiveConvexity(Real oas,
                                const Handle<YieldTermStructure>& engineTS,
                                const DayCounter& dayCounter,
                                Compounding compounding,
                                Frequency frequency,
                                Real bump=2e-4);
        //@}

        void setupArguments(PricingEngine::arguments* args) const override;

      protected:
        CallableBond(Natural settlementDays,
                     const Date& maturityDate,
                     const Calendar& calendar,
                     DayCounter paymentDayCounter,
                     Real faceAmount,
                     const Date& issueDate = Date(),
                     CallabilitySchedule putCallSchedule = CallabilitySchedule());

        DayCounter paymentDayCounter_;
        Frequency frequency_;
        CallabilitySchedule putCallSchedule_;
        Real faceAmount_;
        // helper class for Black implied volatility calculation
        class ImpliedVolHelper;
        // helper class for option adjusted spread calculations
        class NPVSpreadHelper;

      private:
        /*  Used internally.
            same as Bond::accruedAmount() but with enable early
            payments true.  Forces accrued to be calculated in a
            consistent way for future put/ call dates, which can be
            problematic in lattice engines when option dates are also
            coupon dates.
        */
        Real accrued(Date settlement) const;
    };

    class CallableBond::arguments : public Bond::arguments {
      public:
        arguments() = default;
        std::vector<Date> couponDates;
        std::vector<Real> couponAmounts;
        Real faceAmount;
        //! redemption = face amount * redemption / 100.
        Real redemption;
        Date redemptionDate;
        DayCounter paymentDayCounter;
        Frequency frequency;
        CallabilitySchedule putCallSchedule;
        //! bond full/dirty/cash prices
        std::vector<Real> callabilityPrices;
        std::vector<Date> callabilityDates;
        //! Spread to apply to the valuation. This is a continuously
        //! componded rate added to the model. Currently only applied
        //! by the TreeCallableFixedRateBondEngine
        Real spread;
        void validate() const override;
    };

    //! results for a callable bond calculation
    class CallableBond::results : public Bond::results {
      public:
        // no extra results set yet
    };

    //! base class for callable fixed rate bond engine
    class CallableBond::engine
        : public GenericEngine<CallableBond::arguments,
                               CallableBond::results> {};


    //! callable/puttable fixed rate bond
    /*! Callable fixed rate bond class.

        \ingroup instruments
    */
    class CallableFixedRateBond : public CallableBond {
      public:
        CallableFixedRateBond(Natural settlementDays,
                              Real faceAmount,
                              Schedule schedule,
                              const std::vector<Rate>& coupons,
                              const DayCounter& accrualDayCounter,
                              BusinessDayConvention paymentConvention = Following,
                              Real redemption = 100.0,
                              const Date& issueDate =
