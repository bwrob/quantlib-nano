e>& capletVol);

        //! \name InflationCouponPricer interface
        //@{
        Real swapletPrice() const override;
        Rate swapletRate() const override;
        Real capletPrice(Rate effectiveCap) const override;
        Rate capletRate(Rate effectiveCap) const override;
        Real floorletPrice(Rate effectiveFloor) const override;
        Rate floorletRate(Rate effectiveFloor) const override;
        void initialize(const InflationCoupon&) override;
        //@}

      protected:
        virtual Real optionletPrice(Option::Type optionType,
                                    Real effStrike) const;
        virtual Real optionletRate(Option::Type optionType,
                                   Real effStrike) const;

        /*! Derived classes usually only need to implement this.

            The name of the method is misleading.  This actually
            returns the rate of the optionlet (so not discounted and
            not accrued).
        */
        virtual Real optionletPriceImp(Option::Type, Real strike,
                                       Real forward, Real stdDev) const;
        virtual Rate adjustedFixing(Rate fixing = Null<Rate>()) const;

        //! data
        Handle<YoYOptionletVolatilitySurface> capletVol_;
        Handle<YieldTermStructure> nominalTermStructure_;
        const YoYInflationCoupon* coupon_;
        Real gearing_;
        Spread spread_;
        Real discount_;
    };


    //! Black-formula pricer for capped/floored yoy inflation coupons
    class BlackYoYInflationCouponPricer : public YoYInflationCouponPricer {
      public:
        BlackYoYInflationCouponPricer()
        : YoYInflationCouponPricer(Handle<YoYOptionletVolatilitySurface>(),
                                   Handle<YieldTermStructure>()) {}

        explicit BlackYoYInflationCouponPricer(
            const Handle<YieldTermStructure>& nominalTermStructure)
        : YoYInflationCouponPricer(nominalTermStructure) {}

        BlackYoYInflationCouponPricer(
            const Handle<YoYOptionletVolatilitySurface>& capletVol,
            const Handle<YieldTermStructure>& nominalTermStructure)
        : YoYInflationCouponPricer(capletVol, nominalTermStructure) {}
      protected:
        Real optionletPriceImp(Option::Type, Real strike, Real forward, Real stdDev) const override;
    };


    //! Unit-Displaced-Black-formula pricer for capped/floored yoy inflation coupons
    class UnitDisplacedBlackYoYInflationCouponPricer : public YoYInflationCouponPricer {
      public:
        UnitDisplacedBlackYoYInflationCouponPricer()
        : YoYInflationCouponPricer(Handle<YoYOptionletVolatilitySurface>(),
                                   Handle<YieldTermStructure>()) {}

        explicit UnitDisplacedBlackYoYInflationCouponPricer(
            const Handle<YieldTermStructure>& nominalTermStructure)
        : YoYInflationCouponPricer(nominalTermStructure) {}

        UnitDisplacedBlackYoYInflationCouponPricer(
            const Handle<YoYOptionletVolatilitySurface>& capletVol,
            const Handle<YieldTermStructure>& nominalTermStructure)
        : YoYInflationCouponPricer(capletVol, nominalTermStructure) {}
      protected:
        Real optionletPriceImp(Option::Type, Real strike, Real forward, Real stdDev) const override;
    };


    //! Bachelier-formula pricer for capped/floored yoy inflation coupons
    class BachelierYoYInflationCouponPricer : public YoYInflationCouponPricer {
      public:
        BachelierYoYInflationCouponPricer()
        : YoYInflationCouponPricer(Handle<YoYOptionletVolatilitySurface>(),
                                   Handle<YieldTermStructure>()) {}

        explicit BachelierYoYInflationCouponPricer(
            const Handle<YieldTermStructure>& nominalTermStructure)
        : YoYInflationCouponPricer(nominalTermStructure) {}

        BachelierYoYInflationCouponPricer(
            const Handle<YoYOptionletVolatilitySurface>& capletVol,
            const Handle<YieldTermStructure>& nom
