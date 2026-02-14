const std::vector<Real>& v1)>& f ) const {
            detail::multiplyV M;
            return integration()->integrateV(//see note in LMIntegrators base class
                [&](const std::vector<Real>& x){ return M(copula_.density(x), f(x)); });
        }
    protected:
        // Integrable models must provide their integrator.
        // Arguable, not having the integration in the LM class saves that 
        //   memory but have an entry in the VT... 
        virtual const ext::shared_ptr<LMIntegration>& integration() const {
            QL_FAIL("Integration non implemented in Latent model.");
        }
        //@}

        // Ordering is: factorWeights_[iVariable][iFactor]
        mutable std::vector<std::vector<Real> > factorWeights_;
        /* This is a duplicated value from the data above chosen for memory 
        reasons.
        I have opted for this one value redundant memory rather than have the 
        memory load of the observable in all factors. Typically Latent models 
        are used in two very different ways: with many factors and not linked 
        to a market observable (typical matrix size above is of tens of 
        thousands entries) or with just one observable value and the matrix is 
        just a scalar. Otherwise, to remove the redundancy, the matrix 
        factorWeights_ should be one of Quotes Handles.
        Yet it is not entirely true that quotes might be used only in pricing, 
        think sensitivity analysis....
        \todo Reconsider this, see how expensive truly is.
        */
        mutable Handle<Quote> cachedMktFactor_;

        // updated only by correlation observability and constructors.
        // \sqrt{1-\sum_k \beta_{i,k}^2} the addition being along the factors. 
        // It has therefore the size of the basket. Cached for perfomance
        mutable std::vector<Real> idiosyncFctrs_;
        //! Number of systemic factors.
        mutable Size nFactors_;//matches idiosyncFctrs_[0].size();i=0 or any
        //! Number of latent model variables, idiosyncratic terms or model dim
        mutable Size nVariables_;// matches idiosyncFctrs_.size() 

        mutable copulaType copula_;
    };




    // Defines ----------------------------------------------------------------

#ifndef __DOXYGEN__

    template <class Impl>
    LatentModel<Impl>::LatentModel(
        const std::vector<std::vector<Real> >& factorWeights,
        const typename Impl::initTraits& ini)
    : factorWeights_(factorWeights),
      nFactors_(factorWeights[0].size()), 
      nVariables_(factorWeights.size()), copula_(factorWeights, ini)
    {
        for(Size i=0; i<factorWeights.size(); i++) {
            idiosyncFctrs_.push_back(std::sqrt(1.-
                    std::inner_product(factorWeights[i].begin(), 
                factorWeights[i].end(), 
                factorWeights[i].begin(), Real(0.))));
            // while at it, check sizes are coherent:
            QL_REQUIRE(factorWeights[i].size() == nFactors_, 
                "Name " << i << " provides a different number of factors");
        }
    }

    template <class Impl>
    LatentModel<Impl>::LatentModel(
        const std::vector<Real>& factorWeights,
        const typename Impl::initTraits& ini)
    : nFactors_(1),
      nVariables_(factorWeights.size())
    {
        for (Real factorWeight : factorWeights)
            factorWeights_.emplace_back(1, factorWeight);
        for (Real factorWeight : factorWeights)
            idiosyncFctrs_.push_back(std::sqrt(1. - factorWeight * factorWeight));
        //convert row to column vector....
        copula_ = copulaType(factorWeights_, ini);
    }

    template <class Impl>
    LatentModel<Impl>::LatentModel(
        const Real correlSqr,
        Size nVariables,
        const typename Impl::initTraits& ini)
    : factorWeights_(nVariables, std::vector<Real>(1, correlSqr)),
      idiosyncFctrs_(nVariables, 
        std::sqrt(1.-correlSqr*correlSqr)),
      nFactors_(1), 
      nVariables_(n