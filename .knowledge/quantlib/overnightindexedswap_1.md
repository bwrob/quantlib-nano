lendar& paymentCalendar = Calendar(),
                             bool telescopicValueDates = false,
                             RateAveraging::Type averagingMethod = RateAveraging::Compound,
                             Natural lookbackDays = Null<Natural>(),
                             Natural lockoutDays = 0,
                             bool applyObservationShift = false);

        OvernightIndexedSwap(Type type,
                             std::vector<Real> fixedNominals,
                             Schedule fixedSchedule,
                             Rate fixedRate,
                             DayCounter fixedDC,
                             const std::vector<Real>& overnightNominals,
                             Schedule overnightSchedule,
                             const ext::shared_ptr<OvernightIndex>& overnightIndex,
                             Spread spread = 0.0,
                             Integer paymentLag = 0,
                             BusinessDayConvention paymentAdjustment = Following,
                             const Calendar& paymentCalendar = Calendar(),
                             bool telescopicValueDates = false,
                             RateAveraging::Type averagingMethod = RateAveraging::Compound,
                             Natural lookbackDays = Null<Natural>(),
                             Natural lockoutDays = 0,
                             bool applyObservationShift = false);

        //! \name Inspectors
        //@{
        Frequency paymentFrequency() const {
            return std::max(fixedSchedule().tenor().frequency(),
                            floatingSchedule().tenor().frequency());
        }

        const std::vector<Real>& overnightNominals() const { return floatingNominals(); }
        const Schedule& overnightSchedule() const { return floatingSchedule(); }
        const ext::shared_ptr<OvernightIndex>& overnightIndex() const { return overnightIndex_; }
        const Leg& overnightLeg() const { return floatingLeg(); }

        RateAveraging::Type averagingMethod() const { return averagingMethod_; }
        Natural lookbackDays() const { return lookbackDays_; }
        Natural lockoutDays() const { return lockoutDays_; }
        bool applyObservationShift() const { return applyObservationShift_; }
        //@}

        //! \name Results
        //@{
        Real overnightLegBPS() const { return floatingLegBPS(); }
        Real overnightLegNPV() const { return floatingLegNPV(); }
        //@}
      private:
        void setupFloatingArguments(arguments* args) const override;

        ext::shared_ptr<OvernightIndex> overnightIndex_;
        RateAveraging::Type averagingMethod_;
        Natural lookbackDays_;
        Natural lockoutDays_;
        bool applyObservationShift_;
    };

}

#endif
