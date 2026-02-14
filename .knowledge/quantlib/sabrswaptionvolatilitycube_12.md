ible size 2");

        points_ = x;
    }

    template<class Model> void XabrSwaptionVolatilityCube<Model>::Cube::setLayer(Size i,
                                                      const Matrix& x) {
        QL_REQUIRE(i<nLayers_,
            "Cube::setLayer: incompatible number of layer ");
        QL_REQUIRE(x.rows()==optionTimes_.size(),
            "Cube::setLayer: incompatible size 1");
        QL_REQUIRE(x.columns()==swapLengths_.size(),
            "Cube::setLayer: incompatible size 2");

        points_[i] = x;
    }

    template <class Model>
    void XabrSwaptionVolatilityCube<Model>::Cube::setPoint(const Date& optionDate,
                                                  const Period& swapTenor,
                                                  Time optionTime,
                                                  Time swapLength,
                                                  const std::vector<Real>& point)
    {
        const bool expandOptionTimes =
            !(std::binary_search(optionTimes_.begin(),optionTimes_.end(),optionTime));
        const bool expandSwapLengths =
            !(std::binary_search(swapLengths_.begin(),swapLengths_.end(),swapLength));

        std::vector<Real>::const_iterator optionTimesPreviousNode,
                                          swapLengthsPreviousNode;

        optionTimesPreviousNode =
            std::lower_bound(optionTimes_.begin(),optionTimes_.end(),optionTime);
        Size optionTimesIndex = optionTimesPreviousNode - optionTimes_.begin();

        swapLengthsPreviousNode =
            std::lower_bound(swapLengths_.begin(),swapLengths_.end(),swapLength);
        Size swapLengthsIndex = swapLengthsPreviousNode - swapLengths_.begin();

        if (expandOptionTimes || expandSwapLengths)
            expandLayers(optionTimesIndex, expandOptionTimes,
                         swapLengthsIndex, expandSwapLengths);

        for (Size k=0; k<nLayers_; ++k)
            points_[k][optionTimesIndex][swapLengthsIndex] = point[k];

        optionTimes_[optionTimesIndex] = optionTime;
        swapLengths_[swapLengthsIndex] = swapLength;
        optionDates_[optionTimesIndex] = optionDate;
        swapTenors_[swapLengthsIndex] = swapTenor;
    }

    template<class Model> void XabrSwaptionVolatilityCube<Model>::Cube::expandLayers(Size i, bool expandOptionTimes,
                                              Size j, bool expandSwapLengths) {
        QL_REQUIRE(i<=optionTimes_.size(),"Cube::expandLayers: incompatible size 1");
        QL_REQUIRE(j<=swapLengths_.size(),"Cube::expandLayers: incompatible size 2");

        if (expandOptionTimes) {
            optionTimes_.insert(optionTimes_.begin()+i,0.);
            optionDates_.insert(optionDates_.begin()+i, Date());
        }
        if (expandSwapLengths) {
            swapLengths_.insert(swapLengths_.begin()+j,0.);
            swapTenors_.insert(swapTenors_.begin()+j, Period());
        }

        std::vector<Matrix> newPoints(nLayers_,Matrix(optionTimes_.size(),
                                                      swapLengths_.size(), 0.));

        for (Size k=0; k<nLayers_; ++k) {
            for (Size u=0; u<points_[k].rows(); ++u) {
                 Size indexOfRow = u;
                 if (u>=i && expandOptionTimes) indexOfRow = u+1;
                 for (Size v=0; v<points_[k].columns(); ++v) {
                      Size indexOfCol = v;
                      if (v>=j && expandSwapLengths) indexOfCol = v+1;
                      newPoints[k][indexOfRow][indexOfCol]=points_[k][u][v];
                 }
            }
        }
        setPoints(newPoints);
    }

    template<class Model> const std::vector<Matrix>&
    XabrSwaptionVolatilityCube<Model>::Cube::points() const {
        return points_;
    }

    template<class Model> std::vector<Real> XabrSwaptionVolatilityCube<Model>::Cube::operator()(
                            const Time optionTime, const Time swapLength) const {
        std::vector<Real> result;
        