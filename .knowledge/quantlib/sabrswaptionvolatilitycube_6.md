olationError;
            calibrationResult[6]=sabrInterpolation->maxError();
            calibrationResult[7]=sabrInterpolation->endCriteria();

            QL_ENSURE(calibrationResult[7] != Integer(EndCriteria::MaxIterations),
                      "section calibration failed: "
                      "option tenor " << optionDates[j] <<
                      ", swap tenor " << swapTenors[k] <<
                      ": max iteration (" <<
                      endCriteria_->maxIterations() << ")" <<
                          ", alpha " <<  calibrationResult[0]<<
                          ", beta "  <<  calibrationResult[1] <<
                          ", nu "    <<  calibrationResult[2]   <<
                          ", rho "   <<  calibrationResult[3]  <<
                          ", max error " << calibrationResult[6] <<
                          ", error " <<  calibrationResult[5]
                          );

            QL_ENSURE((useMaxError_ ? calibrationResult[6] : calibrationResult[5]) < maxErrorTolerance_,
                      "section calibration failed: "
                      "option tenor " << optionDates[j] <<
                      ", swap tenor " << swapTenors[k] <<
                      (useMaxError_ ? ": max error " : ": error ") <<
                      (useMaxError_ ? calibrationResult[6] : calibrationResult[5]) <<
                          ", alpha " <<  calibrationResult[0] <<
                          ", beta "  <<  calibrationResult[1] <<
                          ", nu "    <<  calibrationResult[2] <<
                          ", rho "   <<  calibrationResult[3] <<
                      (useMaxError_ ? ": error" : ": max error ") <<
                      (useMaxError_ ? calibrationResult[5] : calibrationResult[6])
            );

            parametersCube.setPoint(optionDates[j], swapTenors[k],
                                    optionTimes[j], swapLengths[k],
                                    calibrationResult);
            parametersCube.updateInterpolators();
        }

    }

    template<class Model> void XabrSwaptionVolatilityCube<Model>::fillVolatilityCube() const {

        const ext::shared_ptr<SwaptionVolatilityDiscrete> atmVolStructure =
            ext::dynamic_pointer_cast<SwaptionVolatilityDiscrete>(*atmVol_);

        std::vector<Time> atmOptionTimes(atmVolStructure->optionTimes());
        std::vector<Time> optionTimes(volCubeAtmCalibrated_.optionTimes());
        atmOptionTimes.insert(atmOptionTimes.end(),
                              optionTimes.begin(), optionTimes.end());
        std::sort(atmOptionTimes.begin(),atmOptionTimes.end());
        auto new_end = std::unique(atmOptionTimes.begin(), atmOptionTimes.end());
        atmOptionTimes.erase(new_end, atmOptionTimes.end());

        std::vector<Time> atmSwapLengths(atmVolStructure->swapLengths());
        std::vector<Time> swapLengths(volCubeAtmCalibrated_.swapLengths());
        atmSwapLengths.insert(atmSwapLengths.end(),
                              swapLengths.begin(), swapLengths.end());
        std::sort(atmSwapLengths.begin(),atmSwapLengths.end());
        new_end = std::unique(atmSwapLengths.begin(), atmSwapLengths.end());
        atmSwapLengths.erase(new_end, atmSwapLengths.end());

        std::vector<Date> atmOptionDates = atmVolStructure->optionDates();
        std::vector<Date> optionDates(volCubeAtmCalibrated_.optionDates());
        atmOptionDates.insert(atmOptionDates.end(),
                                optionDates.begin(), optionDates.end());
        std::sort(atmOptionDates.begin(),atmOptionDates.end());
        auto new_end_1 = std::unique(atmOptionDates.begin(), atmOptionDates.end());
        atmOptionDates.erase(new_end_1, atmOptionDates.end());

        std::vector<Period> atmSwapTenors = atmVolStructure->swapTenors();
        std::vector<Period> swapTenors(volCubeAtmCalibrated_.swapTenors());
        atmSwapTenors.insert(atmSwapTenors.end(),
                             swapTenors.begin(), swapTenor
