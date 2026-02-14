s.end());
        std::sort(atmSwapTenors.begin(),atmSwapTenors.end());
        auto new_end_2 = std::unique(atmSwapTenors.begin(), atmSwapTenors.end());
        atmSwapTenors.erase(new_end_2, atmSwapTenors.end());

        createSparseSmiles();

        for (Size j=0; j<atmOptionTimes.size(); j++) {

            for (Size k=0; k<atmSwapLengths.size(); k++) {
                bool expandOptionTimes =
                    !(std::binary_search(optionTimes.begin(),
                                         optionTimes.end(),
                                         atmOptionTimes[j]));
                bool expandSwapLengths =
                    !(std::binary_search(swapLengths.begin(),
                                         swapLengths.end(),
                                         atmSwapLengths[k]));
                if(expandOptionTimes || expandSwapLengths){
                    Rate atmForward = atmStrike(atmOptionDates[j],
                                                atmSwapTenors[k]);
                    Volatility atmVol = atmVol_->volatility(
                        atmOptionDates[j], atmSwapTenors[k], atmForward);
                    std::vector<Real> spreadVols =
                        spreadVolInterpolation(atmOptionDates[j],
                                               atmSwapTenors[k]);
                    std::vector<Real> volAtmCalibrated;
                    volAtmCalibrated.reserve(nStrikes_);
                    for (Size i=0; i<nStrikes_; i++)
                        volAtmCalibrated.push_back(atmVol + spreadVols[i]);
                    volCubeAtmCalibrated_.setPoint(
                                    atmOptionDates[j], atmSwapTenors[k],
                                    atmOptionTimes[j], atmSwapLengths[k],
                                    volAtmCalibrated);
                }
            }
        }
        volCubeAtmCalibrated_.updateInterpolators();
    }


    template<class Model> void XabrSwaptionVolatilityCube<Model>::createSparseSmiles() const {

        std::vector<Time> optionTimes(sparseParameters_.optionTimes());
        std::vector<Time> swapLengths(sparseParameters_.swapLengths());
        sparseSmiles_.clear();

        for (Real& optionTime : optionTimes) {
            std::vector<ext::shared_ptr<SmileSection> > tmp;
            Size n = swapLengths.size();
            tmp.reserve(n);
            for (Size k=0; k<n; ++k) {
                tmp.push_back(smileSection(optionTime, swapLengths[k], sparseParameters_));
            }
            sparseSmiles_.push_back(tmp);
        }
    }


    template<class Model> std::vector<Real> XabrSwaptionVolatilityCube<Model>::spreadVolInterpolation(
        const Date& atmOptionDate, const Period& atmSwapTenor) const {

        Time atmOptionTime = timeFromReference(atmOptionDate);
        Time atmTimeLength = swapLength(atmSwapTenor);

        std::vector<Real> result;
        const std::vector<Time>& optionTimes(sparseParameters_.optionTimes());
        const std::vector<Time>& swapLengths(sparseParameters_.swapLengths());
        const std::vector<Date>& optionDates =
            sparseParameters_.optionDates();
        const std::vector<Period>& swapTenors = sparseParameters_.swapTenors();

        std::vector<Real>::const_iterator optionTimesPreviousNode,
                                          swapLengthsPreviousNode;

        optionTimesPreviousNode = std::lower_bound(optionTimes.begin(),
                                                   optionTimes.end(),
                                                   atmOptionTime);
        Size optionTimesPreviousIndex =
            optionTimesPreviousNode - optionTimes.begin();
        if (optionTimesPreviousIndex >0)
            optionTimesPreviousIndex --;

        swapLengthsPreviousNode = std::lower_bound(swapLengths.begin(),
                                                   swapLengths.end(),
                                                   atmTimeLength);
        Size swapLengthsPrevi