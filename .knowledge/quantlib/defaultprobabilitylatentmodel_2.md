ltProbability(const Date& date, Size iName,
            const std::vector<Real>& mktFactors) const
        {
            const ext::shared_ptr<Pool>& pool = basket_->pool();
            Probability pDefUncond =
                pool->get(pool->names()[iName]).
                defaultProbability(basket_->defaultKeys()[iName])
                  ->defaultProbability(date);
            return conditionalDefaultProbability(pDefUncond, iName, mktFactors);
        }
        /*! Conditional default probability product, intermediate step in the
            correlation calculation.*/
        Probability condProbProduct(Real invCumYProb1, Real invCumYProb2,
            Size iName1, Size iName2,
            const std::vector<Real>& mktFactors) const {
            return
                conditionalDefaultProbabilityInvP(invCumYProb1, iName1,
                    mktFactors) *
                conditionalDefaultProbabilityInvP(invCumYProb2, iName2,
                    mktFactors);
        }
        //! Conditional probability of n default events or more.
        // \todo: check the issuer has not defaulted.
        Real conditionalProbAtLeastNEvents(Size n, const Date& date,
            const std::vector<Real>& mktFactors) const;
        //! access to integration:
        const ext::shared_ptr<LMIntegration>& integration() const override { return integration_; }

      public:
        /*! Computes the unconditional probability of default of a given name.
        Trivial method for testing
        */
        Probability probOfDefault(Size iName, const Date& d) const {
            QL_REQUIRE(basket_, "No portfolio basket set.");
            const ext::shared_ptr<Pool>& pool = basket_->pool();
            // avoid repeating this in the integration:
            Probability pUncond = pool->get(pool->names()[iName]).
                defaultProbability(basket_->defaultKeys()[iName])
                ->defaultProbability(d);
            if (pUncond < 1.e-10) return 0.;

            return integratedExpectedValue(
                [&](const std::vector<Real>& v1) {
                    return conditionalDefaultProbabilityInvP(
                        inverseCumulativeY(pUncond, iName), iName, v1);
                });
        }
        /*! Pearsons' default probability correlation.
            Users should consider specialization on the copula type for specific
            distributions since that might simplify the integrations, most
            importantly if this is to be used in calibration of observations for
            factor coefficients as it is expensive to integrate directly.
        */
        Real defaultCorrelation(const Date& d, Size iNamei, Size iNamej) const;

        /*! Returns the probaility of having a given or larger number of
        defaults in the basket portfolio at a given time.
        */
        Probability probAtLeastNEvents(Size n, const Date& date) const {
            return integratedExpectedValue(
                [&](const std::vector<Real>& v1) {
                    return conditionalProbAtLeastNEvents(n, date, v1);
                });
        }
    };


    //---- Defines -----------------------------------------------------------

    template<class CP>
    Real DefaultLatentModel<CP>::defaultCorrelation(const Date& d,
        Size iNamei, Size iNamej) const
    {
        QL_REQUIRE(basket_, "No portfolio basket set.");

        const ext::shared_ptr<Pool>& pool = basket_->pool();
        // unconditionals:
        Probability pi = pool->get(pool->names()[iNamei]).
            defaultProbability(basket_->defaultKeys()[iNamei])
            ->defaultProbability(d);
        Probability pj = pool->get(pool->names()[iNamej]).
            defaultProbability(basket_->defaultKeys()[iNamej])
            ->defaultProbability(d);
        Real pipj = pi * pj;
        Real invPi = inverseCumulativeY(pi, iNamei);
        Real invPj = inverseCumulativeY(pj, iNamej);
        // avoid repetitive calls when i=j?
        Real E1i1j; // jo
