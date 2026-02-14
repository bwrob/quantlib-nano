lowerRateBound;
                upperRateBound_ = upperRateBound;
                defaultBounds_ = false;
                return *this;
            }

            Settings &withPriceThreshold(const Real priceThreshold = 1.0E-8) {
                strategy_ = PriceThreshold;
                priceThreshold_ = priceThreshold;
                lowerRateBound_ = defaultLowerBound;
                upperRateBound_ = defaultUpperBound;
                defaultBounds_ = true;
                return *this;
            }

            Settings &withPriceThreshold(const Real priceThreshold,
                                         const Real lowerRateBound,
                                         const Real upperRateBound) {
                strategy_ = PriceThreshold;
                priceThreshold_ = priceThreshold;
                lowerRateBound_ = lowerRateBound;
                upperRateBound_ = upperRateBound;
                defaultBounds_ = false;
                return *this;
            }

            Settings &withBSStdDevs(const Real stdDevs = 3.0) {
                strategy_ = BSStdDevs;
                stdDevs_ = stdDevs;
                lowerRateBound_ = defaultLowerBound;
                upperRateBound_ = defaultUpperBound;
                defaultBounds_ = true;
                return *this;
            }

            Settings &withBSStdDevs(const Real stdDevs,
                                    const Real lowerRateBound,
                                    const Real upperRateBound) {
                strategy_ = BSStdDevs;
                stdDevs_ = stdDevs;
                lowerRateBound_ = lowerRateBound;
                upperRateBound_ = upperRateBound;
                defaultBounds_ = false;
                return *this;
            }

            enum Strategy {
                RateBound,
                VegaRatio,
                PriceThreshold,
                BSStdDevs
            };

            Strategy strategy_ = RateBound;
            Real vegaRatio_ = 0.01;
            Real priceThreshold_ = 1.0E-8;
            Real stdDevs_ = 3.0;
            Real lowerRateBound_, upperRateBound_;
            bool defaultBounds_ = true;
        };


        LinearTsrPricer(
            const Handle<SwaptionVolatilityStructure>& swaptionVol,
            Handle<Quote> meanReversion,
            Handle<YieldTermStructure> couponDiscountCurve = Handle<YieldTermStructure>(),
            const Settings& settings = Settings(),
            ext::shared_ptr<Integrator> integrator = ext::shared_ptr<Integrator>());

        /* */
        Real swapletPrice() const override;
        Rate swapletRate() const override;
        Real capletPrice(Rate effectiveCap) const override;
        Rate capletRate(Rate effectiveCap) const override;
        Real floorletPrice(Rate effectiveFloor) const override;
        Rate floorletRate(Rate effectiveFloor) const override;
        /* */
        Real meanReversion() const override;
        void setMeanReversion(const Handle<Quote>& meanReversion) override {
            unregisterWith(meanReversion_);
            meanReversion_ = meanReversion;
            registerWith(meanReversion_);
            update();
        }


      private:

        Real GsrG(const Date &d) const;
        Real singularTerms(Option::Type type, Real strike) const;
        Real integrand(Real strike) const;
        Real a_, b_;

        class integrand_f;

        class VegaRatioHelper {
          public:
            VegaRatioHelper(const SmileSection *section, const Real targetVega)
                : section_(section), targetVega_(targetVega) {}
            Real operator()(Real strike) const {
                return section_->vega(strike) - targetVega_;
            };
            const SmileSection *section_;
            const Real targetVega_;
        };

        class PriceHelper {
          public:
            PriceHelper(const SmileSection *section, const Option::Type type,
                        const Real targetPrice)

