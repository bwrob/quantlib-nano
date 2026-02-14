result.reserve(nLayers_);
        for (Size k=0; k<nLayers_; ++k)
            result.push_back((*interpolators_[k])(optionTime, swapLength));
        return result;
    }

    template<class Model> const std::vector<Time>&
    XabrSwaptionVolatilityCube<Model>::Cube::optionTimes() const {
        return optionTimes_;
    }

    template<class Model> const std::vector<Time>&
    XabrSwaptionVolatilityCube<Model>::Cube::swapLengths() const {
        return swapLengths_;
    }

    template<class Model> void XabrSwaptionVolatilityCube<Model>::Cube::updateInterpolators() const {
        for (Size k = 0; k < nLayers_; ++k) {
            transposedPoints_[k] = transpose(points_[k]);
            ext::shared_ptr<Interpolation2D> interpolation;
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
            interpolators_[k] = ext::shared_ptr<Interpolation2D>(
                new FlatExtrapolator2D(interpolation));
            interpolators_[k]->enableExtrapolation();
        }
    }

    template<class Model> Matrix XabrSwaptionVolatilityCube<Model>::Cube::browse() const {
        Matrix result(swapLengths_.size()*optionTimes_.size(), nLayers_+2, 0.0);
        for (Size i=0; i<swapLengths_.size(); ++i) {
            for (Size j=0; j<optionTimes_.size(); ++j) {
                result[i*optionTimes_.size()+j][0] = swapLengths_[i];
                result[i*optionTimes_.size()+j][1] = optionTimes_[j];
                for (Size k=0; k<nLayers_; ++k)
                    result[i*optionTimes_.size()+j][2+k] = points_[k][j][i];
            }
        }
        return result;
    }

    //======================================================================//
    //                      SabrSwaptionVolatilityCube                      //
    //======================================================================//

    //! Swaption Volatility Cube SABR 
    /*! This struct defines the types used by SABR Volatility cubes
        for interpolation (SABRInterpolation) and for modeling the
        smile (SabrSmileSection).
    */
    struct SwaptionVolCubeSabrModel {
        typedef SABRInterpolation Interpolation;
        typedef SabrSmileSection SmileSection;
    };


    //! SABR volatility cube for swaptions
    typedef XabrSwaptionVolatilityCube<SwaptionVolCubeSabrModel> SabrSwaptionVolatilityCube;

}

#endif