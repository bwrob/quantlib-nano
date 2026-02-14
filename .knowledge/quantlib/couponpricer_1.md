ckIborCouponPricer : public IborCouponPricer {
      public:
        enum TimingAdjustment { Black76, BivariateLognormal };
        BlackIborCouponPricer(
            const Handle<OptionletVolatilityStructure>& v = Handle<OptionletVolatilityStructure>(),
            const TimingAdjustment timingAdjustment = Black76,
            Handle<Quote> correlation = Handle<Quote>(ext::shared_ptr<Quote>(new SimpleQuote(1.0))),
            const ext::optional<bool> useIndexedCoupon = ext::nullopt)
        : IborCouponPricer(v, useIndexedCoupon), timingAdjustment_(timingAdjustment),
          correlation_(std::move(correlation)) {
            { // this additional scope seems required to avoid a misleading-indentation warning
                QL_REQUIRE(timingAdjustment_ == Black76 || timingAdjustment_ == BivariateLognormal,
                           "unknown timing adjustment (code " << timingAdjustment_ << ")");
            }
            registerWith(correlation_);
        };
        void initialize(const FloatingRateCoupon& coupon) override;
        Real swapletPrice() const override;
        Rate swapletRate() const override;
        Real capletPrice(Rate effectiveCap) const override;
        Rate capletRate(Rate effectiveCap) const override;
        Real floorletPrice(Rate effectiveFloor) const override;
        Rate floorletRate(Rate effectiveFloor) const override;

      protected:
        Real optionletPrice(Option::Type optionType, Real effStrike) const;
        Real optionletRate(Option::Type optionType, Real effStrike) const;

        virtual Rate adjustedFixing(Rate fixing = Null<Rate>()) const;

        Real discount_;

      private:
        const TimingAdjustment timingAdjustment_;
        const Handle<Quote> correlation_;
    };

    //! base pricer for vanilla CMS coupons
    class CmsCouponPricer : public FloatingRateCouponPricer {
      public:
        explicit CmsCouponPricer(
            Handle<SwaptionVolatilityStructure> v = Handle<SwaptionVolatilityStructure>())
        : swaptionVol_(std::move(v)) {
            registerWith(swaptionVol_);
        }

        Handle<SwaptionVolatilityStructure> swaptionVolatility() const{
            return swaptionVol_;
        }
        void setSwaptionVolatility(
                            const Handle<SwaptionVolatilityStructure>& v=
                                    Handle<SwaptionVolatilityStructure>()) {
            unregisterWith(swaptionVol_);
            swaptionVol_ = v;
            registerWith(swaptionVol_);
            update();
        }
      private:
        Handle<SwaptionVolatilityStructure> swaptionVol_;
    };

    /*! (CMS) coupon pricer that has a mean reversion parameter which can be
      used to calibrate to cms market quotes */
    class MeanRevertingPricer {
    public:
        virtual Real meanReversion() const = 0;
        virtual void setMeanReversion(const Handle<Quote>&) = 0;
        virtual ~MeanRevertingPricer() = default;
    };

    void setCouponPricer(const Leg& leg,
                         const ext::shared_ptr<FloatingRateCouponPricer>&);

    void setCouponPricers(
            const Leg& leg,
            const std::vector<ext::shared_ptr<FloatingRateCouponPricer> >&);

    /*! set the first matching pricer (if any) to each coupon of the leg */
    void setCouponPricers(
            const Leg& leg,
            const ext::shared_ptr<FloatingRateCouponPricer>&,
            const ext::shared_ptr<FloatingRateCouponPricer>&);

    void setCouponPricers(
            const Leg& leg,
            const ext::shared_ptr<FloatingRateCouponPricer>&,
            const ext::shared_ptr<FloatingRateCouponPricer>&,
            const ext::shared_ptr<FloatingRateCouponPricer>&);

    void setCouponPricers(
            const Leg& leg,
            const ext::shared_ptr<FloatingRateCouponPricer>&,
            const ext::shared_ptr<FloatingRateCouponPricer>&,
            const ext::shared_ptr<FloatingRateCouponPricer>&,
            const ext::shared_ptr<FloatingRat
