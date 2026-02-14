red_ptr<YieldTermStructure> rateCurve_;
        GFunctionFactory::YieldCurveModel modelOfYieldCurve_;
        ext::shared_ptr<GFunction> gFunction_;
        const CmsCoupon* coupon_;
        Date paymentDate_, fixingDate_;
        Rate swapRateValue_;
        DiscountFactor discount_;
        Real annuity_;
        Real gearing_;
        Spread spread_;
        Real spreadLegValue_;
        Rate cutoffForCaplet_ = 2, cutoffForFloorlet_ = 0;
        Handle<Quote> meanReversion_;
        Period swapTenor_;
        ext::shared_ptr<VanillaOptionPricer> vanillaOptionPricer_;
    };


    //! CMS-coupon pricer
    /*! Prices a cms coupon via static replication as in Hagan's
        "Conundrums..." article via numerical integration based on
        prices of vanilla swaptions
    */
    class NumericHaganPricer : public HaganPricer {
      public:
        NumericHaganPricer(
            const Handle<SwaptionVolatilityStructure>& swaptionVol,
            GFunctionFactory::YieldCurveModel modelOfYieldCurve,
            const Handle<Quote>& meanReversion,
            Rate lowerLimit = 0.0,
            Rate upperLimit = 1.0,
            Real precision = 1.0e-6,
            Real hardUpperLimit = QL_MAX_REAL);

        Real upperLimit() const { return upperLimit_; }
        Real lowerLimit() const { return lowerLimit_; }
        Real stdDeviations() const { return stdDeviationsForUpperLimit_; }

        // private:
        class Function {
          public:
            virtual ~Function() = default;
            virtual Real operator()(Real x) const = 0;
        };

        class ConundrumIntegrand : public Function {
            friend class NumericHaganPricer;
          public:
            ConundrumIntegrand(ext::shared_ptr<VanillaOptionPricer> o,
                               const ext::shared_ptr<YieldTermStructure>& rateCurve,
                               ext::shared_ptr<GFunction> gFunction,
                               Date fixingDate,
                               Date paymentDate,
                               Real annuity,
                               Real forwardValue,
                               Real strike,
                               Option::Type optionType);
            Real operator()(Real x) const override;

          protected:
            Real functionF(Real x) const;
            Real firstDerivativeOfF(Real x) const;
            Real secondDerivativeOfF(Real x) const;

            Real strike() const;
            Real annuity() const;
            Date fixingDate() const;
            void setStrike(Real strike);

            const ext::shared_ptr<VanillaOptionPricer> vanillaOptionPricer_;
            const Real forwardValue_, annuity_;
            const Date fixingDate_, paymentDate_;
            Real strike_;
            const Option::Type optionType_;
            ext::shared_ptr<GFunction> gFunction_;
        };

        Real integrate(Real a,
                       Real b,
                       const ConundrumIntegrand& Integrand) const;
        Real optionletPrice(Option::Type optionType, Rate strike) const override;
        Real swapletPrice() const override;
        Real resetUpperLimit(Real stdDeviationsForUpperLimit) const;
        Real resetLowerLimit(Real stdDeviationsForLowerLimit) const;
        Real refineIntegration(Real integralValue, const ConundrumIntegrand& integrand) const;

        mutable Real lowerLimit_, stdDeviationsForLowerLimit_, upperLimit_, stdDeviationsForUpperLimit_;
        const Real  requiredStdDeviations_ = 8, precision_,
                                refiningIntegrationTolerance_ = .0001;
        const Real hardUpperLimit_;
    };

    //! CMS-coupon pricer
    class AnalyticHaganPricer : public HaganPricer {
      public:
        AnalyticHaganPricer(
            const Handle<SwaptionVolatilityStructure>& swaptionVol,
            GFunctionFactory::YieldCurveModel modelOfYieldCurve,
            const Handle<Quote>& meanReversion);
      protected:
        Real optionletP
