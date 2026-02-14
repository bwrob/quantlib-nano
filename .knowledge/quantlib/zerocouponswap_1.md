onst override { return startDate_; }
        Date maturityDate() const override { return maturityDate_; }
        const ext::shared_ptr<IborIndex>& iborIndex() const { return iborIndex_; }

        //! just one cashflow in each leg
        const Leg& fixedLeg() const;
        //! just one cashflow in each leg
        const Leg& floatingLeg() const;

        Real fixedPayment() const;
        //@}

        //! \name Results
        //@{
        Real fixedLegNPV() const;
        Real floatingLegNPV() const;
        Real fairFixedPayment() const;
        Rate fairFixedRate(const DayCounter& dayCounter) const;
        //@}

      private:
        ZeroCouponSwap(Type type,
                       Real baseNominal,
                       const Date& startDate,
                       const Date& maturityDate,
                       ext::shared_ptr<IborIndex> iborIndex,
                       const Calendar& paymentCalendar,
                       BusinessDayConvention paymentConvention,
                       Natural paymentDelay);

        Type type_;
        Real baseNominal_;
        ext::shared_ptr<IborIndex> iborIndex_;
        Date startDate_;
        Date maturityDate_;
        Date paymentDate_;
    };
}

#endif
