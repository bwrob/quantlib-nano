table Cube sparseParameters_;
        mutable Cube denseParameters_;
        mutable std::vector< std::vector<ext::shared_ptr<SmileSection> > >
                                                                sparseSmiles_;
        std::vector<std::vector<Handle<Quote> > > parametersGuessQuotes_;
        mutable Cube parametersGuess_;
        std::vector<bool> isParameterFixed_;
        bool isAtmCalibrated_;
        const ext::shared_ptr<EndCriteria> endCriteria_;
        Real maxErrorTolerance_;
        const ext::shared_ptr<OptimizationMethod> optMethod_;
        Real errorAccept_;
        const bool useMaxError_;
        const Size maxGuesses_;
        const bool backwardFlat_;
        const Real cutoffStrike_;
        VolatilityType volatilityType_;

        class PrivateObserver : public Observer {
          public:
            explicit PrivateObserver(XabrSwaptionVolatilityCube<Model> *v)
                : v_(v) {}
            void update() override {
                v_->setParameterGuess();
                v_->update();
            }

          private:
            XabrSwaptionVolatilityCube<Model> *v_;
        };

       ext::shared_ptr<PrivateObserver> privateObserver_;

    };

    //=======================================================================//
    //                        XabrSwaptionVolatilityCube                              //
    //=======================================================================//

    template <class Model>
    XabrSwaptionVolatilityCube<Model>::XabrSwaptionVolatilityCube(
        const Handle<SwaptionVolatilityStructure>& atmVolStructure,
        const std::vector<Period>& optionTenors,
        const std::vector<Period>& swapTenors,
        const std::vector<Spread>& strikeSpreads,
        const std::vector<std::vector<Handle<Quote> > >& volSpreads,
        const ext::shared_ptr<SwapIndex>& swapIndexBase,
        const ext::shared_ptr<SwapIndex>& shortSwapIndexBase,
        bool vegaWeightedSmileFit,
        std::vector<std::vector<Handle<Quote> > > parametersGuess,
        std::vector<bool> isParameterFixed,
        bool isAtmCalibrated,
        ext::shared_ptr<EndCriteria> endCriteria,
        Real maxErrorTolerance,
        ext::shared_ptr<OptimizationMethod> optMethod,
        const Real errorAccept,
        const bool useMaxError,
        const Size maxGuesses,
        const bool backwardFlat,
        const Real cutoffStrike)
    : SwaptionVolatilityCube(atmVolStructure,
                             optionTenors,
                             swapTenors,
                             strikeSpreads,
                             volSpreads,
                             swapIndexBase,
                             shortSwapIndexBase,
                             vegaWeightedSmileFit),
      parametersGuessQuotes_(std::move(parametersGuess)),
      isParameterFixed_(std::move(isParameterFixed)), isAtmCalibrated_(isAtmCalibrated),
      endCriteria_(std::move(endCriteria)), optMethod_(std::move(optMethod)),
      useMaxError_(useMaxError), maxGuesses_(maxGuesses), backwardFlat_(backwardFlat),
      cutoffStrike_(cutoffStrike), volatilityType_(atmVolStructure->volatilityType()) {

        if (maxErrorTolerance != Null<Rate>()) {
            maxErrorTolerance_ = maxErrorTolerance;
        } else{
            maxErrorTolerance_ = SWAPTIONVOLCUBE_TOL;
            if (vegaWeightedSmileFit_) maxErrorTolerance_ =  SWAPTIONVOLCUBE_VEGAWEIGHTED_TOL;
        }
        if (errorAccept != Null<Rate>()) {
            errorAccept_ = errorAccept;
        } else{
            errorAccept_ = maxErrorTolerance_ / 5.0;
        }

        privateObserver_ = ext::make_shared<PrivateObserver>(this);
        registerWithParametersGuess();
        setParameterGuess();
    }

    template<class Model> void XabrSwaptionVolatilityCube<Model>::registerWithParametersGuess()
    {
        for (Size i=0; i<4; i++)
            for (Size j=0; j<nOptionTenors_; j++)
                for (Size k=0; k<nSwapTenors_