 strike = atmForward+strikeSpreads_[i];
                    if(strike + shiftTmp >=cutoffStrike_) {
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
                                          shiftTmp,
                                          volatilityType_));
                sabrInterpolation->update();

                Real rmsError = sabrInterpolation->rmsError();
                Real maxError = sabrInterpolation->maxError();
                alphas     [j][k] = sabrInterpolation->alpha();
                betas      [j][k] = sabrInterpolation->beta();
                nus        [j][k] = sabrInterpolation->nu();
                rhos       [j][k] = sabrInterpolation->rho();
                forwards   [j][k] = atmForward;
                errors     [j][k] = rmsError;
                maxErrors  [j][k] = maxError;
                endCriteria[j][k] = sabrInterpolation->endCriteria();

                QL_ENSURE(endCriteria[j][k] != Integer(EndCriteria::MaxIterations),
                          "global swaptions calibration failed: "
                          "MaxIterations reached: " << "\n" <<
                          "option maturity = " << optionDates[j] << ", \n" <<
                          "swap tenor = " << swapTenors[k] << ", \n" <<
                          "rms error = " << io::rate(errors[j][k])  << ", \n" <<
                          "max error = " << io::rate(maxErrors[j][k]) << ", \n" <<
                          "   alpha = " <<  alphas[j][k] << "n" <<
                          "   beta = " <<  betas[j][k] << "\n" <<
                          "   nu = " <<  nus[j][k]   << "\n" <<
                          "   rho = " <<  rhos[j][k]  << "\n"
                          );

                QL_ENSURE((useMaxError_ ? maxError : rmsError) < maxErrorTolerance_,
                          "global swaptions calibration failed: "
                          "error tolerance exceeded: "
                              << "\n"
                              << "using " << (useMaxError_ ? "maxError" : "rmsError")
                              << " tolerance " << maxErrorTolerance_ << ", \n"
                              << "option maturity = " << optionDates[j] << ", \n"
                              << "swap tenor = " << swapTenors[k] << ", \n"
                              << "rms error = " << io::rate(errors[j][k]) << ", \n"
                              << "max error = " << io::rate(maxErrors[j][k]) << ", \n"
                              << "   alpha = " << alphas[j][k] << "n"
                              << "   beta = " << betas[j][k] << "\n"
                              << "   nu = " << nus[j