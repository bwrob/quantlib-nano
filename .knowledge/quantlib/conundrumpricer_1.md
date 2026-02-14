    protected:
            /* fraction of a period between the swap start date and
               the pay date  */
            Real delta_;
            /* accruals fraction*/
            std::vector<Time> accruals_;
        };

        class GFunctionWithShifts : public GFunction {

            Time swapStartTime_;

            Time shapedPaymentTime_;
            std::vector<Time> shapedSwapPaymentTimes_;

            std::vector<Time> accruals_;
            std::vector<Real> swapPaymentDiscounts_;
            Real discountAtStart_, discountRatio_;

            Real swapRateValue_;
            Handle<Quote> meanReversion_;

            Real calibratedShift_ = 0.03, tmpRs_ = 10000000.0;
            const Real accuracy_ = 1.0e-14;

            //* function describing the non-parallel shape of the curve shift*/
            Real shapeOfShift(Real s) const;
            //* calibration of shift*/
            Real calibrationOfShift(Real Rs);
            Real functionZ(Real x);
            Real derRs_derX(Real x);
            Real derZ_derX(Real x);
            Real der2Rs_derX2(Real x);
            Real der2Z_derX2(Real x);

            class ObjectiveFunction {
                const GFunctionWithShifts& o_;
                Real Rs_;
                mutable Real derivative_;
                public:
                  virtual ~ObjectiveFunction() = default;
                  ObjectiveFunction(const GFunctionWithShifts& o, const Real Rs) : o_(o), Rs_(Rs) {}
                  virtual Real operator()(const Real& x) const;
                  Real derivative(const Real& x) const;
                  void setSwapRateValue(Real x);
                  const GFunctionWithShifts& gFunctionWithShifts() const { return o_; }
            };

            ext::shared_ptr<ObjectiveFunction> objectiveFunction_;
          public:
            GFunctionWithShifts(const CmsCoupon& coupon, Handle<Quote> meanReversion);
            Real operator()(Real x) override;
            Real firstDerivative(Real x) override;
            Real secondDerivative(Real x) override;
        };

    };

    inline std::ostream& operator<<(std::ostream& out,
                                    GFunctionFactory::YieldCurveModel type) {
        switch (type) {
          case GFunctionFactory::Standard:
            return out << "Standard";
          case GFunctionFactory::ExactYield:
            return out << "ExactYield";
          case GFunctionFactory::ParallelShifts:
            return out << "ParallelShifts";
          case GFunctionFactory::NonParallelShifts:
            return out << "NonParallelShifts";
          default:
            QL_FAIL("unknown option type");
        }
    }

    //! CMS-coupon pricer
    /*! Base class for the pricing of a CMS coupon via static replication
        as in Hagan's "Conundrums..." article
    */
    class HaganPricer: public CmsCouponPricer, public MeanRevertingPricer {
      public:
        /* */
        Real swapletPrice() const override = 0;
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
        };

      protected:
        HaganPricer(const Handle<SwaptionVolatilityStructure>& swaptionVol,
                    GFunctionFactory::YieldCurveModel modelOfYieldCurve,
                    Handle<Quote> meanReversion);
        void initialize(const FloatingRateCoupon& coupon) override;

        virtual Real optionletPrice(Option::Type optionType,
                                    Real strike) const = 0;

        ext::sha