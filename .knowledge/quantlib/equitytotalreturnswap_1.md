; }
        BusinessDayConvention paymentConvention() const { return paymentConvention_; }
        Natural paymentDelay() const { return paymentDelay_; }

        const Leg& equityLeg() const;
        const Leg& interestRateLeg() const;
        //@}

        //! \name Results
        //@{
        Real equityLegNPV() const;
        Real interestRateLegNPV() const;
        Real fairMargin() const;
        //@}

      private:
        EquityTotalReturnSwap(ext::shared_ptr<EquityIndex> equityIndex,
                              ext::shared_ptr<InterestRateIndex> interestRateIndex,
                              Type type,
                              Real nominal,
                              Schedule schedule,
                              DayCounter dayCounter,
                              Rate margin,
                              Real gearing = 1.0,
                              Calendar paymentCalendar = Calendar(),
                              BusinessDayConvention paymentConvention = Unadjusted,
                              Natural paymentDelay = 0);

        ext::shared_ptr<EquityIndex> equityIndex_;
        ext::shared_ptr<InterestRateIndex> interestRateIndex_;
        Type type_;
        Real nominal_;
        Schedule schedule_;
        DayCounter dayCounter_;
        Rate margin_;
        Real gearing_;
        Calendar paymentCalendar_;
        BusinessDayConvention paymentConvention_;
        Natural paymentDelay_;
    };
}

#endif