        Handle<YieldTermStructure> discountCurve() const;

        Date fixingDate() const;

        //! Returns the relevant forward rate associated with the FRA term
        InterestRate forwardRate() const;
        //@}

      protected:
        void setupExpired() const override;
        void performCalculations() const override;
        Position::Type fraType_;
        //! aka FRA rate (the market forward rate)
        mutable InterestRate forwardRate_;
        //! aka FRA fixing rate, contract rate
        InterestRate strikeForwardRate_;
        Real notionalAmount_;
        ext::shared_ptr<IborIndex> index_;
        bool useIndexedCoupon_;

        DayCounter dayCounter_;
        Calendar calendar_;
        BusinessDayConvention businessDayConvention_;

        //! the valueDate is the date the underlying index starts accruing and the FRA is settled.
        Date valueDate_;
        //! maturityDate of the underlying index; not the date the FRA is settled.
        Date maturityDate_;
        Handle<YieldTermStructure> discountCurve_;

      private:
        void calculateForwardRate() const;
        void calculateAmount() const;
        mutable Real amount_;
    };

    inline const Calendar& ForwardRateAgreement::calendar() const { return calendar_; }

    inline BusinessDayConvention ForwardRateAgreement::businessDayConvention() const {
        return businessDayConvention_;
    }

    inline const DayCounter& ForwardRateAgreement::dayCounter() const { return dayCounter_; }

    inline Handle<YieldTermStructure> ForwardRateAgreement::discountCurve() const {
        return discountCurve_;
    }

}


#endif
