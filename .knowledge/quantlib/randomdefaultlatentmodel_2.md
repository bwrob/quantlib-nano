thEvent(Size n, const Date& d) const override;
        //! Pearsons' default probability correlation.
        Real defaultCorrelation(const Date& d, Size iName, Size jName) const override;
        Real expectedTrancheLoss(const Date& d) const override;
        virtual std::pair<Real, Real> expectedTrancheLossInterval(const Date& d,
            Probability confidencePerc) const;
        std::map<Real, Probability> lossDistribution(const Date& d) const override;
        virtual Histogram computeHistogram(const Date& d) const;
        Real expectedShortfall(const Date& d, Real percent) const override;
        Real percentile(const Date& d, Real percentile) const override;
        /*! Returns the VaR value for a given percentile and the 95 confidence
        interval of that value. */
        virtual std::tuple<Real, Real, Real> percentileAndInterval(
            const Date& d, Real percentile) const;
        /*! Distributes the total VaR amount along the portfolio counterparties.
            The passed loss amount is in loss units.
        */
        std::vector<Real> splitVaRLevel(const Date& date, Real loss) const override;
        /*! Distributes the total VaR amount along the portfolio
            counterparties.

            Provides confidence interval for split so that portfolio
            optimization can be performed outside those limits.

            The passed loss amount is in loss units.
        */
        virtual std::vector<std::vector<Real> > splitVaRAndError(
            const Date& date, Real loss, Probability confInterval) const;
        //@}
    public:
      ~RandomLM() override = default;

    private:
        BigNatural seed_;
    protected:
        const Size numFactors_;
        const Size numLMVars_;

        const Size nSims_;

        mutable std::vector<std::vector<simEvent<derivedRandomLM<copulaPolicy,
            USNG > > > > simsBuffer_;

        mutable copulaPolicy copula_;
        mutable ext::shared_ptr<copulaRNG_type> copulasRng_;

        // Maximum time inversion horizon
        static const Size maxHorizon_ = 4050; // over 11 years
        // Inversion probability limits are computed by children in initdates()
    };


    /* ---- Statistics ---------------------------------------------------  */

    template<template <class, class> class D, class C, class URNG>
    Probability RandomLM<D, C, URNG>::probAtLeastNEvents(Size n,
        const Date& d) const
    {
        calculate();
        Date today = Settings::instance().evaluationDate();

        QL_REQUIRE(d>today, "Date for statistic must be in the future.");
        // casted to natural to avoid warning, we have just checked the sign
        Natural val = d.serialNumber() - today.serialNumber();

        if(n==0) return 1.;

        Real counts = 0.;
        for(Size iSim=0; iSim < nSims_; iSim++) {
            Size simCount = 0;
            const std::vector<simEvent<D<C, URNG> > >& events =
                getSim(iSim);
            for(Size iEvt=0; iEvt < events.size(); iEvt++)
                // duck type on the members:
                if(val > events[iEvt].dayFromRef) simCount++;
            if(simCount >= n) counts++;
        }
        return counts/nSims_;
        // \todo Provide confidence interval
    }

    template<template <class, class> class D, class C, class URNG>
    std::vector<Probability> RandomLM<D, C, URNG>::probsBeingNthEvent(Size n,
                                                                      const Date& d) const
    {
        calculate();
        Size basketSize = basket_->size();

        QL_REQUIRE(n>0 && n<=basketSize, "Impossible number of defaults.");
        Date today = Settings::instance().evaluationDate();

        QL_REQUIRE(d>today, "Date for statistic must be in the future.");
        // casted to natural to avoid warning, we have just checked the sign
        Natural val = d.serialNumber() - today.serialNumber();

        std::vector<Probability> hitsByDate(basketSize, 0.);
        for(S