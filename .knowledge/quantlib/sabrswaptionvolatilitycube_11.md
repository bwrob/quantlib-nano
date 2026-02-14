       interpolators_[k]->enableExtrapolation();
        }
        setPoints(points);
     }

    template<class Model> XabrSwaptionVolatilityCube<Model>::Cube::Cube(const Cube& o)
    : optionTimes_(o.optionTimes_), swapLengths_(o.swapLengths_),
      optionDates_(o.optionDates_), swapTenors_(o.swapTenors_),
      nLayers_(o.nLayers_), transposedPoints_(o.transposedPoints_),
      extrapolation_(o.extrapolation_), backwardFlat_(o.backwardFlat_) {
        for (Size k=0; k<nLayers_; ++k) {
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
            interpolators_.push_back(ext::shared_ptr<Interpolation2D>(
                new FlatExtrapolator2D(interpolation)));
            interpolators_[k]->enableExtrapolation();
        }
        setPoints(o.points_);
    }

    template<class Model> typename XabrSwaptionVolatilityCube<Model>::Cube&
    XabrSwaptionVolatilityCube<Model>::Cube::operator=(const Cube& o) {
        optionTimes_ = o.optionTimes_;
        swapLengths_ = o.swapLengths_;
        optionDates_ = o.optionDates_;
        swapTenors_ = o.swapTenors_;
        nLayers_ = o.nLayers_;
        extrapolation_ = o.extrapolation_;
        backwardFlat_ = o.backwardFlat_;
        transposedPoints_ = o.transposedPoints_;
        for(Size k=0;k<nLayers_;k++){
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
            interpolators_.push_back(ext::shared_ptr<Interpolation2D>(
                new FlatExtrapolator2D(interpolation)));
            interpolators_[k]->enableExtrapolation();
        }
        setPoints(o.points_);
        return *this;
    }

    template<class Model> void XabrSwaptionVolatilityCube<Model>::Cube::setElement(Size IndexOfLayer,
                                                        Size IndexOfRow,
                                                        Size IndexOfColumn,
                                                        Real x) {
        QL_REQUIRE(IndexOfLayer<nLayers_,
            "Cube::setElement: incompatible IndexOfLayer ");
        QL_REQUIRE(IndexOfRow<optionTimes_.size(),
            "Cube::setElement: incompatible IndexOfRow");
        QL_REQUIRE(IndexOfColumn<swapLengths_.size(),
            "Cube::setElement: incompatible IndexOfColumn");
        points_[IndexOfLayer][IndexOfRow][IndexOfColumn] = x;
    }

    template<class Model> void XabrSwaptionVolatilityCube<Model>::Cube::setPoints(
                                               const std::vector<Matrix>& x) {
        QL_REQUIRE(x.size()==nLayers_,
            "Cube::setPoints: incompatible number of layers ");
        QL_REQUIRE(x[0].rows()==optionTimes_.size(),
            "Cube::setPoints: incompatible size 1");
        QL_REQUIRE(x[0].columns()==swapLengths_.size(),
            "Cube::setPoints: incompat