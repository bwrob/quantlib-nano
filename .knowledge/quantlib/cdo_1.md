ault basket represented by a vector of
                               default term structures that allow
                               computing single name default
                               probabilities depending on time
            \param copula      one-factor copula
            \param protectionSeller   sold protection if set to true, purchased
                                      otherwise
            \param premiumSchedule    schedule for premium payments
            \param premiumRate        annual premium rate, e.g. 0.05 for 5% p.a.
            \param dayCounter         day count convention for the premium rate
            \param recoveryRate       recovery rate as a fraction
            \param upfrontPremiumRate premium as a tranche notional fraction
            \param yieldTS            yield term structure handle
            \param nBuckets           number of distribution buckets
            \param integrationStep    time step for integrating over one
                                      premium period; if larger than premium
                                      period length, a single step is taken
        */
        CDO(Real attachment,
            Real detachment,
            std::vector<Real> nominals,
            const std::vector<Handle<DefaultProbabilityTermStructure> >& basket,
            Handle<OneFactorCopula> copula,
            bool protectionSeller,
            Schedule premiumSchedule,
            Rate premiumRate,
            DayCounter dayCounter,
            Rate recoveryRate,
            Rate upfrontPremiumRate,
            Handle<YieldTermStructure> yieldTS,
            Size nBuckets,
            const Period& integrationStep = Period(10, Years));

        Real nominal() const { return nominal_; }
        Real lgd() const { return lgd_; }
        Real attachment() const { return attachment_; }
        Real detachment() const { return detachment_; }
        std::vector<Real> nominals() { return nominals_; }
        Size size() { return basket_.size(); }

        bool isExpired() const override;
        Rate fairPremium() const;
        Rate premiumValue () const;
        Rate protectionValue () const;
        Size error () const;

      private:
        void setupExpired() const override;
        void performCalculations() const override;
        Real expectedTrancheLoss (Date d) const;

        Real attachment_;
        Real detachment_;
        std::vector<Real> nominals_;
        std::vector<Handle<DefaultProbabilityTermStructure> > basket_;
        Handle<OneFactorCopula> copula_;
        bool protectionSeller_;

        Schedule premiumSchedule_;
        Rate premiumRate_;
        DayCounter dayCounter_;
        Rate recoveryRate_;
        Rate upfrontPremiumRate_;
        Handle<YieldTermStructure> yieldTS_;
        Size nBuckets_; // number of buckets up to detachment point
        Period integrationStep_;

        std::vector<Real> lgds_;

        Real nominal_;  // total basket volume (sum of nominals_)
        Real lgd_;      // maximum loss given default (sum of lgds_)
        Real xMax_;     // tranche detachment point (tranche_ * nominal_)
        Real xMin_;     // tranche attachment point (tranche_ * nominal_)

        mutable Size error_;

        mutable Real premiumValue_;
        mutable Real protectionValue_;
        mutable Real upfrontPremiumValue_;
    };

}

#endif