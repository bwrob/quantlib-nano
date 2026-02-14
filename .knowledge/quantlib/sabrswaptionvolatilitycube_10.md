            fillVolatilityCube();
            sabrCalibrationSection(volCubeAtmCalibrated_, denseParameters_,
                                   swapTenor);
        }
        notifyObservers();

    }

    template<class Model> void XabrSwaptionVolatilityCube<Model>::recalibration(const std::vector<Period> &swapLengths,
                                         const std::vector<Real> &beta,
                                         const Period &swapTenor) {

        QL_REQUIRE(beta.size() == swapLengths.size(),
                   "beta size ("
                       << beta.size()
                       << ") must be equal to number of swap lengths ("
                       << swapLengths.size() << ")");

        std::vector<Time> betaTimes;
        betaTimes.reserve(beta.size());
        for (Size i = 0; i < beta.size(); i++)
            betaTimes.push_back(
                timeFromReference(optionDateFromTenor(swapLengths[i])));

        LinearInterpolation betaInterpolation(betaTimes.begin(),
                                              betaTimes.end(), beta.begin());

        std::vector<Real> cubeBeta;
        for (Size i = 0; i < optionTimes().size(); i++) {
            Real t = optionTimes()[i];
            // flat extrapolation ensures admissable values
            if (t < betaTimes.front())
                t = betaTimes.front();
            if (t > betaTimes.back())
                t = betaTimes.back();
            cubeBeta.push_back(betaInterpolation(t));
        }

        recalibration(cubeBeta, swapTenor);

    }

    //======================================================================//
    //                      XabrSwaptionVolatilityCube::Cube                         //
    //======================================================================//


    template<class Model> XabrSwaptionVolatilityCube<Model>::Cube::Cube(const std::vector<Date>& optionDates,
                                    const std::vector<Period>& swapTenors,
                                    const std::vector<Time>& optionTimes,
                                    const std::vector<Time>& swapLengths,
                                    Size nLayers,
                                    bool extrapolation,
                                    bool backwardFlat)
    : optionTimes_(optionTimes), swapLengths_(swapLengths),
      optionDates_(optionDates), swapTenors_(swapTenors),
        nLayers_(nLayers), extrapolation_(extrapolation),
        backwardFlat_(backwardFlat) {

        QL_REQUIRE(optionTimes.size()>1,"Cube::Cube(...): optionTimes.size()<2");
        QL_REQUIRE(swapLengths.size()>1,"Cube::Cube(...): swapLengths.size()<2");

        QL_REQUIRE(optionTimes.size()==optionDates.size(),
                   "Cube::Cube(...): optionTimes/optionDates mismatch");
        QL_REQUIRE(swapTenors.size()==swapLengths.size(),
                   "Cube::Cube(...): swapTenors/swapLengths mismatch");

        std::vector<Matrix> points(nLayers_, Matrix(optionTimes_.size(),
                                                    swapLengths_.size(), 0.0));
        for (Size k=0;k<nLayers_;k++) {
            ext::shared_ptr<Interpolation2D> interpolation;
            transposedPoints_.push_back(transpose(points[k]));
            if (k <= 4 && backwardFlat_)
                interpolation =
                    ext::make_shared<BackwardflatLinearInterpolation>(
                        optionTimes_.begin(), optionTimes_.end(),
                        swapLengths_.begin(), swapLengths_.end(),
                        transposedPoints_[k]);
            else
                interpolation =
                    ext::make_shared<BilinearInterpolation>(
                        optionTimes_.begin(), optionTimes_.end(),
                        swapLengths_.begin(), swapLengths_.end(),
                        transposedPoints_[k]);
            interpolators_.push_back(ext::shared_ptr<Interpolation2D>(
                new FlatExtrapolator2D(interpolation)));

