ride { return fixingDays_; }

        //! \name YoYCapFloorTermPriceSurface interface
        //@{
        std::pair<std::vector<Time>, std::vector<Rate> > atmYoYSwapTimeRates() const override {
            return atmYoYSwapTimeRates_;
        }
        std::pair<std::vector<Date>, std::vector<Rate> > atmYoYSwapDateRates() const override {
            return atmYoYSwapDateRates_;
        }
        ext::shared_ptr<YoYInflationTermStructure> YoYTS() const override { return yoy_; }
        Rate price(const Date& d, Rate k) const override;
        Real floorPrice(const Date& d, Rate k) const override;
        Real capPrice(const Date& d, Rate k) const override;
        Rate atmYoYSwapRate(const Date& d, bool extrapolate = true) const override {
            return atmYoYSwapRateCurve_(timeFromReference(d),extrapolate);
        }
        Rate atmYoYRate(const Date& d,
                        const Period& obsLag = Period(-1, Days),
                        bool extrapolate = true) const override {
            // work in terms of maturity-of-instruments
            // so ask for rate with observation lag
            Period p = (obsLag == Period(-1, Days)) ? observationLag() : obsLag;
            return yoy_->yoyRate(d - p, extrapolate);
        }
        //@}

        //! \name LazyObject interface
        //@{
        void update() override;
        void performCalculations() const;
        //@}

      protected:
        //! intersection of cap and floor price surfaces at given strikes
        void intersect() const;
        class ObjectiveFunction {
          public:
            ObjectiveFunction(Time t, const Interpolation2D&, const Interpolation2D&);
            Real operator()(Rate guess) const;
          protected:
            const Time t_;
            const Interpolation2D &a_, &b_; // work on references
        };

        //! mess of making it, i.e. create instruments from quotes and bootstrap
        void calculateYoYTermStructure() const;

        // data for surfaces and curve
        mutable std::vector<Rate> cStrikesB_;
        mutable std::vector<Rate> fStrikesB_;
        mutable Matrix cPriceB_;
        mutable Matrix fPriceB_;
        mutable Interpolation2D capPrice_, floorPrice_;
        mutable Interpolation2D floorPrice2_;
        mutable Interpolator2D interpolator2d_;
        mutable Interpolation atmYoYSwapRateCurve_;
        mutable Interpolator1D interpolator1d_;
    };


    // inline definitions

    inline bool YoYCapFloorTermPriceSurface::indexIsInterpolated() const {
        return indexIsInterpolated_;
    }

    inline Period YoYCapFloorTermPriceSurface::observationLag() const {
        return observationLag_;
    }

    inline Frequency YoYCapFloorTermPriceSurface::frequency() const {
        return yoyIndex_->frequency();
    }

    // template definitions

    #ifndef __DOXYGEN__

    template<class I2D, class I1D>
    InterpolatedYoYCapFloorTermPriceSurface<I2D,I1D>::
    InterpolatedYoYCapFloorTermPriceSurface(
                                    Natural fixingDays,
                                    const Period &yyLag,
                                    const ext::shared_ptr<YoYInflationIndex>& yii,
                                    CPI::InterpolationType interpolation,
                                    const Handle<YieldTermStructure> &nominal,
                                    const DayCounter &dc,
                                    const Calendar &cal,
                                    const BusinessDayConvention &bdc,
                                    const std::vector<Rate> &cStrikes,
                                    const std::vector<Rate> &fStrikes,
                                    const std::vector<Period> &cfMaturities,
                                    const Matrix &cPrice,
                                    const Matrix &fPrice,
                                    const I2D &interpolator2d,
                                    const I1D &interpolator1d)
    : YoY
