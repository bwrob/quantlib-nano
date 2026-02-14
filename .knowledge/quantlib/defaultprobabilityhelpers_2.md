nningSpread,
                         const Period& tenor,
                         Integer settlementDays,
                         const Calendar& calendar,
                         Frequency frequency,
                         BusinessDayConvention paymentConvention,
                         DateGeneration::Rule rule,
                         const DayCounter& dayCounter,
                         Real recoveryRate,
                         const Handle<YieldTermStructure>& discountCurve,
                         Natural upfrontSettlementDays = 3,
                         bool settlesAccrual = true,
                         bool paysAtDefaultTime = true,
                         const Date& startDate = Date(),
                         const DayCounter& lastPeriodDayCounter = DayCounter(),
                         bool rebatesAccrual = true,
                         CreditDefaultSwap::PricingModel model = CreditDefaultSwap::Midpoint);

        Real impliedQuote() const override;

      private:
        Date upfrontDate();
        void initializeDates() override;
        void resetEngine() override;
        Natural upfrontSettlementDays_;
        Date upfrontDate_;
        Rate runningSpread_;
    };

}


#endif
