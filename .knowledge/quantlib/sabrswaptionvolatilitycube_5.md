][k] << "\n"
                              << "   rho = " << rhos[j][k] << "\n");
            }
        }
        Cube sabrParametersCube(optionDates, swapTenors,
                                optionTimes, swapLengths, 8,
                                true, backwardFlat_);
        sabrParametersCube.setLayer(0, alphas);
        sabrParametersCube.setLayer(1, betas);
        sabrParametersCube.setLayer(2, nus);
        sabrParametersCube.setLayer(3, rhos);
        sabrParametersCube.setLayer(4, forwards);
        sabrParametersCube.setLayer(5, errors);
        sabrParametersCube.setLayer(6, maxErrors);
        sabrParametersCube.setLayer(7, endCriteria);

        return sabrParametersCube;

    }

    template<class Model> void XabrSwaptionVolatilityCube<Model>::sabrCalibrationSection(
                                            const Cube& marketVolCube,
                                            Cube& parametersCube,
                                            const Period& swapTenor) const {

        const std::vector<Time>& optionTimes = marketVolCube.optionTimes();
        const std::vector<Time>& swapLengths = marketVolCube.swapLengths();
        const std::vector<Date>& optionDates = marketVolCube.optionDates();
        const std::vector<Period>& swapTenors = marketVolCube.swapTenors();

        Size k = std::find(swapTenors.begin(), swapTenors.end(),
                           swapTenor) - swapTenors.begin();
        QL_REQUIRE(k != swapTenors.size(), "swap tenor not found");

        std::vector<Real> calibrationResult(8,0.);
        const std::vector<Matrix>& tmpMarketVolCube = marketVolCube.points();

        std::vector<Real> strikes(strikeSpreads_.size());
        std::vector<Real> volatilities(strikeSpreads_.size());

        for (Size j=0; j<optionTimes.size(); j++) {
            Rate atmForward = atmStrike(optionDates[j], swapTenors[k]);
            Real shiftTmp = atmVol_->shift(optionTimes[j], swapLengths[k]);
            strikes.clear();
            volatilities.clear();
            for (Size i=0; i<nStrikes_; i++){
                Real strike = atmForward+strikeSpreads_[i];
                if(strike+shiftTmp>=cutoffStrike_) {
                    strikes.push_back(strike);
                    volatilities.push_back(tmpMarketVolCube[i][j][k]);
                }
            }

            const std::vector<Real>& guess =
                parametersGuess_(optionTimes[j], swapLengths[k]);

                const ext::shared_ptr<typename Model::Interpolation> sabrInterpolation =
                    ext::shared_ptr<typename Model::Interpolation>(new
                                          (typename Model::Interpolation)(strikes.begin(), strikes.end(),
                                      volatilities.begin(),
                                      optionTimes[j], atmForward,
                                      guess[0], guess[1],
                                      guess[2], guess[3],
                                      isParameterFixed_[0],
                                      isParameterFixed_[1],
                                      isParameterFixed_[2],
                                      isParameterFixed_[3],
                                      vegaWeightedSmileFit_,
                                      endCriteria_,
                                      optMethod_,
                                      errorAccept_,
                                      useMaxError_,
                                      maxGuesses_,
                                      shiftTmp));

            sabrInterpolation->update();
            Real interpolationError = sabrInterpolation->rmsError();
            calibrationResult[0]=sabrInterpolation->alpha();
            calibrationResult[1]=sabrInterpolation->beta();
            calibrationResult[2]=sabrInterpolation->nu();
            calibrationResult[3]=sabrInterpolation->rho();
            calibrationResult[4]=atmForward;
            calibrationResult[5]=interp
