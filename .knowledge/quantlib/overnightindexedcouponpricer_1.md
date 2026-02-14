ightIndexedCoupon* coupon_ = nullptr;
        Handle<OptionletVolatilityStructure> capletVol_;
        bool effectiveVolatilityInput_ = false;
        mutable Real effectiveCapletVolatility_ = Null<Real>();
        mutable Real effectiveFloorletVolatility_ = Null<Real>();
    };

    //! Base pricer for compounded overnight-indexed floating coupons
    class CompoundingOvernightIndexedCouponPricer : public OvernightIndexedCouponPricer {
      public:
        explicit CompoundingOvernightIndexedCouponPricer(
          Handle<OptionletVolatilityStructure> v = Handle<OptionletVolatilityStructure>(),
          bool effectiveVolatilityInput = false);
        //! \name FloatingRateCoupon interface
        //@{
        //void initialize(const FloatingRateCoupon& coupon) override;
        Rate swapletRate() const override;
        Real swapletPrice() const override { QL_FAIL("swapletPrice not available"); }
        Real capletPrice(Rate) const override { QL_FAIL("capletPrice not available"); }
        Rate capletRate(Rate) const override { QL_FAIL("capletRate not available"); }
        Real floorletPrice(Rate) const override { QL_FAIL("floorletPrice not available"); }
        Rate floorletRate(Rate) const override { QL_FAIL("floorletRate not available"); }
        //@}
        Rate capletRate([[maybe_unused]] Rate effectiveCap, [[maybe_unused]] bool dailyCapFloor) const override {
          QL_FAIL("CompoundingOvernightIndexedCouponPricer::capletRate(Rate, bool) not implemented");
        }
        Rate floorletRate([[maybe_unused]] Rate effectiveCap, [[maybe_unused]] bool dailyCapFloor) const override {
          QL_FAIL("CompoundingOvernightIndexedCouponPricer::floorletRate(Rate, bool) not implemented");
        }
        Rate averageRate(const Date& date) const override;
        Rate effectiveSpread() const;
        Rate effectiveIndexFixing() const;

      protected:
        std::tuple<Rate, Spread, Rate> compute(const Date& date) const;
        mutable Real swapletRate_, effectiveSpread_, effectiveIndexFixing_;
    };

    //! Base pricer for arithmetically averaged overnight-indexed floating coupons
    /*! Reference: Katsumi Takada 2011, Valuation of Arithmetically Average of
        Fed Funds Rates and Construction of the US Dollar Swap Yield Curve
    */
    class ArithmeticAveragedOvernightIndexedCouponPricer : public OvernightIndexedCouponPricer {
      public:
        explicit ArithmeticAveragedOvernightIndexedCouponPricer(
            Real meanReversion = 0.03,
            Real volatility = 0.00, // NO convexity adjustment by default
            bool byApprox = false, // TRUE to use Katsumi Takada approximation
            Handle<OptionletVolatilityStructure> v = Handle<OptionletVolatilityStructure>(),
            const bool effectiveVolatilityInput = false)
        : OvernightIndexedCouponPricer(std::move(v), effectiveVolatilityInput),
         byApprox_(byApprox), mrs_(meanReversion), vol_(volatility) {}

        explicit ArithmeticAveragedOvernightIndexedCouponPricer(
            bool byApprox) // Simplified constructor assuming no convexity correction
        : ArithmeticAveragedOvernightIndexedCouponPricer(0.03, 0.0, byApprox) {}

        //void initialize(const FloatingRateCoupon& coupon) override;
        Rate swapletRate() const override;
        Real swapletPrice() const override { QL_FAIL("swapletPrice not available"); }
        Real capletPrice(Rate) const override { QL_FAIL("capletPrice not available"); }
        Rate capletRate(Rate) const override { QL_FAIL("capletRate not available"); }
        Real floorletPrice(Rate) const override { QL_FAIL("floorletPrice not available"); }
        Rate floorletRate(Rate) const override { QL_FAIL("floorletRate not available"); }

        Rate capletRate([[maybe_unused]] Rate effectiveCap, [[maybe_unused]] bool dailyCapFloor) const override {
          QL_FAIL("ArithmeticAveragedOvernightIndexedCouponPricer::capletRate(Rate, bool) not implemented");
        }
        Rate
