; k++)
                    privateObserver_->registerWith(parametersGuessQuotes_[j*nSwapTenors_+k][i]);
    }

    template<class Model> void XabrSwaptionVolatilityCube<Model>::setParameterGuess() const {

        //! set parametersGuess_ by parametersGuessQuotes_
        parametersGuess_ = Cube(optionDates_, swapTenors_,
                                optionTimes_, swapLengths_, 4,
                                true, backwardFlat_);
        Size i;
        for (i=0; i<4; i++)
            for (Size j=0; j<nOptionTenors_ ; j++)
                for (Size k=0; k<nSwapTenors_; k++) {
                    parametersGuess_.setElement(i, j, k,
                        parametersGuessQuotes_[j*nSwapTenors_+k][i]->value());
                }
        parametersGuess_.updateInterpolators();

    }

    template<class Model> void XabrSwaptionVolatilityCube<Model>::performCalculations() const {

        SwaptionVolatilityCube::performCalculations();

        //! set marketVolCube_ by volSpreads_ quotes
        marketVolCube_ = Cube(optionDates_, swapTenors_,
                              optionTimes_, swapLengths_, nStrikes_);
        Rate atmForward;
        Volatility atmVol, vol;
        for (Size j=0; j<nOptionTenors_; ++j) {
            for (Size k=0; k<nSwapTenors_; ++k) {
                atmForward = atmStrike(optionDates_[j], swapTenors_[k]);
                atmVol = atmVol_->volatility(optionDates_[j], swapTenors_[k],
                                                              atmForward);
                for (Size i=0; i<nStrikes_; ++i) {
                    vol = atmVol + volSpreads_[j*nSwapTenors_+k][i]->value();
                    marketVolCube_.setElement(i, j, k, vol);
                }
            }
        }
        marketVolCube_.updateInterpolators();

        sparseParameters_ = sabrCalibration(marketVolCube_);
        //parametersGuess_ = sparseParameters_;
        sparseParameters_.updateInterpolators();
        //parametersGuess_.updateInterpolators();
        volCubeAtmCalibrated_= marketVolCube_;

        if(isAtmCalibrated_){
            fillVolatilityCube();
            denseParameters_ = sabrCalibration(volCubeAtmCalibrated_);
            denseParameters_.updateInterpolators();
        }
    }

    template<class Model> void XabrSwaptionVolatilityCube<Model>::updateAfterRecalibration() {
        volCubeAtmCalibrated_ = marketVolCube_;
        if(isAtmCalibrated_){
            fillVolatilityCube();
            denseParameters_ = sabrCalibration(volCubeAtmCalibrated_);
            denseParameters_.updateInterpolators();
        }
        notifyObservers();
    }

    template <class Model>
    typename XabrSwaptionVolatilityCube<Model>::Cube
    XabrSwaptionVolatilityCube<Model>::sabrCalibration(const Cube &marketVolCube) const {

        const std::vector<Time>& optionTimes = marketVolCube.optionTimes();
        const std::vector<Time>& swapLengths = marketVolCube.swapLengths();
        const std::vector<Date>& optionDates = marketVolCube.optionDates();
        const std::vector<Period>& swapTenors = marketVolCube.swapTenors();
        Matrix alphas(optionTimes.size(), swapLengths.size(),0.);
        Matrix betas(alphas);
        Matrix nus(alphas);
        Matrix rhos(alphas);
        Matrix forwards(alphas);
        Matrix errors(alphas);
        Matrix maxErrors(alphas);
        Matrix endCriteria(alphas);

        const std::vector<Matrix>& tmpMarketVolCube = marketVolCube.points();

        std::vector<Real> strikes(strikeSpreads_.size());
        std::vector<Real> volatilities(strikeSpreads_.size());

        for (Size j=0; j<optionTimes.size(); j++) {
            for (Size k=0; k<swapLengths.size(); k++) {
                Rate atmForward = atmStrike(optionDates[j], swapTenors[k]);
                Real shiftTmp = atmVol_->shift(optionTimes[j], swapLengths[k]);
                strikes.clear();
                volatilities.clear();
                for (Size i=0; i<nStrikes_; i++){
                    Real