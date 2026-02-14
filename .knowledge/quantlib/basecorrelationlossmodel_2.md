    /* reset correl and call base models which have the different baskets
        associated.*/
        localCorrelationAttach_->setValue(correlK1);
        Real expLossK1 =
            basketAttach_->expectedTrancheLoss(d);
        localCorrelationDetach_->setValue(correlK2);
        Real expLossK2 =
            basketDetach_->expectedTrancheLoss(d);
        return expLossK2 - expLossK1;
    }


    // ----------------------------------------------------------------------


    /* Concrete specializations submodels construction. With the dummy template
    parameter trick partial specializations leaving the interpolation open
    would be possible.
    */

    #ifndef QL_PATCH_SOLARIS

    template<>
    inline void BaseCorrelationLossModel<GaussianLHPLossModel,
        BilinearInterpolation>::setupModels() const
    {
        // on this assignment any previous registration with the attach and
        //   detach baskets should be removed
        scalarCorrelModelAttach_ = ext::make_shared<GaussianLHPLossModel>(
            Handle<Quote>(localCorrelationAttach_), recoveries_);
        scalarCorrelModelDetach_ = ext::make_shared<GaussianLHPLossModel>(
            Handle<Quote>(localCorrelationDetach_), recoveries_);

        basketAttach_->setLossModel(scalarCorrelModelAttach_);
        basketDetach_->setLossModel(scalarCorrelModelDetach_);
    }

    template<>
    inline void BaseCorrelationLossModel<GaussianBinomialLossModel,
        BilinearInterpolation>::setupModels() const
    {
        ext::shared_ptr<GaussianConstantLossLM> lmA =
            ext::make_shared<GaussianConstantLossLM>(
                Handle<Quote>(localCorrelationAttach_), recoveries_,
                LatentModelIntegrationType::GaussianQuadrature,
                recoveries_.size(), copulaTraits_);
        ext::shared_ptr<GaussianConstantLossLM> lmD =
            ext::make_shared<GaussianConstantLossLM>(
                Handle<Quote>(localCorrelationDetach_), recoveries_,
                LatentModelIntegrationType::GaussianQuadrature,
                recoveries_.size(), copulaTraits_);
        scalarCorrelModelAttach_ =
            ext::make_shared<GaussianBinomialLossModel>(lmA);
        scalarCorrelModelDetach_ =
            ext::make_shared<GaussianBinomialLossModel>(lmD);

        basketAttach_->setLossModel(scalarCorrelModelAttach_);
        basketDetach_->setLossModel(scalarCorrelModelDetach_);

    }

    template<>
    inline void BaseCorrelationLossModel<TBinomialLossModel,
        BilinearInterpolation>::setupModels() const
    {
        ext::shared_ptr<TConstantLossLM> lmA =
            ext::make_shared<TConstantLossLM>(
                Handle<Quote>(localCorrelationAttach_), recoveries_,
                LatentModelIntegrationType::GaussianQuadrature,
                recoveries_.size(), copulaTraits_);
        ext::shared_ptr<TConstantLossLM> lmD =
            ext::make_shared<TConstantLossLM>(
                Handle<Quote>(localCorrelationDetach_), recoveries_,
                LatentModelIntegrationType::GaussianQuadrature,
                recoveries_.size(), copulaTraits_);

        scalarCorrelModelAttach_ =
            ext::make_shared<TBinomialLossModel>(lmA);
        scalarCorrelModelDetach_ =
            ext::make_shared<TBinomialLossModel>(lmD);

        basketAttach_->setLossModel(scalarCorrelModelAttach_);
        basketDetach_->setLossModel(scalarCorrelModelDetach_);
    }

    /* \todo Fix this model, is failing for equity tranches at least, the
    base model works all right, its the link here.
    */
    template<>
    inline void BaseCorrelationLossModel<IHGaussPoolLossModel,
        BilinearInterpolation>::setupModels() const
    {
        ext::shared_ptr<GaussianConstantLossLM> lmA =
            ext::make_shared<GaussianConstantLossLM>(
                Handle<Quote>(localCorrelationAttach_), recoveries_,
                LatentModelIntegrationType::GaussianQuadrature,

