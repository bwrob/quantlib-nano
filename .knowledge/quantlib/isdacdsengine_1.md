uponPeriod forwardsInCouponPeriod = Piecewise);

        Handle<YieldTermStructure> isdaRateCurve() const { return discountCurve_; }
        Handle<DefaultProbabilityTermStructure> isdaCreditCurve() const { return probability_; }

        void calculate() const override;

      private:
        Handle<DefaultProbabilityTermStructure> probability_;
        const Real recoveryRate_;
        Handle<YieldTermStructure> discountCurve_;
        const ext::optional<bool> includeSettlementDateFlows_;
        const NumericalFix numericalFix_;
        const AccrualBias accrualBias_;
        const ForwardsInCouponPeriod forwardsInCouponPeriod_;
    };
}

#endif