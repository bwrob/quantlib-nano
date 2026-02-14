int default covariance term
        if(iNamei !=iNamej) {
            E1i1j = integratedExpectedValue(
                [&](const std::vector<Real>& v1) {
                    return condProbProduct(invPi, invPj, iNamei, iNamej, v1); });
        }else{
            E1i1j = pi;
        }
        return (E1i1j - pipj )/std::sqrt(pipj*(1.-pi)*(1.-pj));
    }


    template<class CP>
    Real DefaultLatentModel<CP>::conditionalProbAtLeastNEvents(Size n,
        const Date& date,
        const std::vector<Real>& mktFactors) const {
            QL_REQUIRE(basket_, "No portfolio basket set.");

            /* \todo
            This algorithm traverses all permutations starting form the
            lowest one. This is inneficient, there shouldnt be any need to
            go through the invalid ones. Use combinations of n elements.

            See integration in O'Kane for homogeneous ntds.
            */
            // first position with as many defaults as desired:
            Size poolSize = basket_->size();//move to 'livesize'
            const ext::shared_ptr<Pool>& pool = basket_->pool();

            auto limit = static_cast<BigNatural>(std::pow(2., (int)(poolSize)));

            // Precalc conditional probabilities
            std::vector<Probability> pDefCond;
            pDefCond.reserve(poolSize);
            for(Size i=0; i<poolSize; i++)
                pDefCond.push_back(conditionalDefaultProbability(
                    pool->get(pool->names()[i]).
                    defaultProbability(basket_->defaultKeys()[i])->
                    defaultProbability(date), i, mktFactors));

            Probability probNEventsOrMore = 0.;
            // cheap permutations
            // dynamic_bitset (std::vector) memory manipulations moved out of the hot loop
            auto mask = static_cast<BigNatural>((1 << (int)(n)) - 1);
            boost::dynamic_bitset<> bsetMask(poolSize, mask);
            auto bits_set = bsetMask.count();
            auto increaseMask = [&]() {
                for (Size i = 0; i < bsetMask.size(); i++) {
                    // NOLINTBEGIN(modernize-use-bool-literals)
                    if (bsetMask[i]) {bsetMask[i] = 0; bits_set--;}
                    else {bsetMask[i] = 1; bits_set++; break;}
                    // NOLINTEND(modernize-use-bool-literals)
                }
            };
            for (; mask < limit; mask++) {
                if (bits_set >= n) {
                    Probability pConfig = 1;
                    for (Size i = 0; i < bsetMask.size(); i++)
                        pConfig *= (bsetMask[i] ? pDefCond[i] : (1. - pDefCond[i]));
                    probNEventsOrMore += pConfig;
                }
                increaseMask();
            }
            return probNEventsOrMore;
    }


    // often used:
    typedef DefaultLatentModel<GaussianCopulaPolicy> GaussianDefProbLM;
    typedef DefaultLatentModel<TCopulaPolicy> TDefProbLM;
}

#endif
