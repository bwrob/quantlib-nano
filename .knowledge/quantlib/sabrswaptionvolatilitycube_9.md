(Size k=0; k<nStrikes_; k++){
            const Real strike = std::max(atmForward + strikeSpreads_[k],cutoffStrike_-shift);
            const Real moneyness = (atmForward+shift)/(strike+shift);

            Matrix strikes(2,2,0.);
            Matrix spreadVols(2,2,0.);
            for (Size i=0; i<2; i++){
                for (Size j=0; j<2; j++){
                    strikes[i][j] = (atmForwards[i][j]+atmShifts[i][j])/moneyness - atmShifts[i][j];
                    spreadVols[i][j] =
                        smiles[i][j]->volatility(strikes[i][j]) - atmVols[i][j];
                }
            }
           Cube localInterpolator(optionsDateNodes, swapTenorNodes,
                                  optionsNodes, swapLengthsNodes, 1);
           localInterpolator.setLayer(0, spreadVols);
           localInterpolator.updateInterpolators();

           result.push_back(localInterpolator(atmOptionTime, atmTimeLength)[0]);
        }
        return result;
    }

    template<class Model> ext::shared_ptr<SmileSection>
    XabrSwaptionVolatilityCube<Model>::smileSection(Time optionTime, Time swapLength,
                                   const Cube& sabrParametersCube) const {

        calculate();
        const std::vector<Real> sabrParameters =
            sabrParametersCube(optionTime, swapLength);
        Real shiftTmp = atmVol_->shift(optionTime,swapLength);
        return ext::shared_ptr<SmileSection>(new (typename Model::SmileSection)(
                          optionTime, sabrParameters[4], sabrParameters,shiftTmp, volatilityType_));
    }

    template<class Model> ext::shared_ptr<SmileSection>
    XabrSwaptionVolatilityCube<Model>::smileSectionImpl(Time optionTime,
                                       Time swapLength) const {
        if (isAtmCalibrated_)
            return smileSection(optionTime, swapLength, denseParameters_);
        else
            return smileSection(optionTime, swapLength, sparseParameters_);
    }

    template<class Model> Matrix XabrSwaptionVolatilityCube<Model>::sparseSabrParameters() const {
        calculate();
        return sparseParameters_.browse();
    }

    template<class Model> Matrix XabrSwaptionVolatilityCube<Model>::denseSabrParameters() const {
        calculate();
        return denseParameters_.browse();
    }

    template<class Model> Matrix XabrSwaptionVolatilityCube<Model>::marketVolCube() const {
        calculate();
        return marketVolCube_.browse();
    }

    template<class Model> Matrix XabrSwaptionVolatilityCube<Model>::volCubeAtmCalibrated() const {
        calculate();
        return volCubeAtmCalibrated_.browse();
    }

    template<class Model> void XabrSwaptionVolatilityCube<Model>::recalibration(Real beta,
                                         const Period& swapTenor) {

        std::vector<Real> betaVector(nOptionTenors_, beta);
        recalibration(betaVector,swapTenor);

    }

    template<class Model> void XabrSwaptionVolatilityCube<Model>::recalibration(const std::vector<Real> &beta,
                                         const Period& swapTenor) {

        QL_REQUIRE(beta.size() == nOptionTenors_,
                   "beta size ("
                       << beta.size()
                       << ") must be equal to number of option tenors ("
                       << nOptionTenors_ << ")");

        const std::vector<Period> &swapTenors = marketVolCube_.swapTenors();
        Size k = std::find(swapTenors.begin(), swapTenors.end(), swapTenor) -
                 swapTenors.begin();

        QL_REQUIRE(k != swapTenors.size(), "swap tenor (" << swapTenor
                                                          << ") not found");

        for (Size i = 0; i < nOptionTenors_; ++i) {
            parametersGuess_.setElement(1, i, k, beta[i]);
        }

        parametersGuess_.updateInterpolators();
        sabrCalibrationSection(marketVolCube_, sparseParameters_, swapTenor);

        volCubeAtmCalibrated_ = marketVolCube_;
        if (isAtmCalibrated_) {
