               recoveries_.size(), copulaTraits_);
        ext::shared_ptr<GaussianConstantLossLM> lmD = 
            ext::make_shared<GaussianConstantLossLM>(
                Handle<Quote>(localCorrelationDetach_), recoveries_, 
                LatentModelIntegrationType::GaussianQuadrature, 
                recoveries_.size(), copulaTraits_);

        // \todo Allow the sending specific model params, as the number of 
        //   buckets here.
        scalarCorrelModelAttach_ = 
            ext::make_shared<IHGaussPoolLossModel>(lmA, 500);
        scalarCorrelModelDetach_ = 
            ext::make_shared<IHGaussPoolLossModel>(lmD, 500);
            
        basketAttach_->setLossModel(scalarCorrelModelAttach_);
        basketDetach_->setLossModel(scalarCorrelModelDetach_);
    }

    #endif


    // Vanilla BC model
    #ifndef QL_PATCH_SOLARIS
    typedef BaseCorrelationLossModel<GaussianLHPLossModel, 
                BilinearInterpolation> GaussianLHPFlatBCLM;
    #endif

}

#endif