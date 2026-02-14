ionTimes_;
        }
        const Schedule& observationSchedule() const { return observationSchedule_; }
        /*! \deprecated Use observationSchedule instead.
                        Deprecated in version 1.40.
        */
        [[deprecated("Use observationSchedule instead")]]
        ext::shared_ptr<Schedule> observationsSchedule() const {
            return ext::make_shared<Schedule>(observationSchedule_);
        }

        Real priceWithoutOptionality(
                       const Handle<YieldTermStructure>& discountCurve) const;
        //! \name Visitability
        //@{
        void accept(AcyclicVisitor&) override;
        //@}
      private:

        Real startTime_;                               // S
        Real endTime_;                                 // T

        Schedule observationSchedule_;
        std::vector<Date> observationDates_;
        std::vector<Real> observationTimes_;
        Size observationsNo_;

        Real lowerTrigger_;
        Real upperTrigger_;
     };

    class RangeAccrualPricer: public FloatingRateCouponPricer {
      public:
        //! \name Observer interface
        //@{
        Rate swapletRate() const override;
        Real capletPrice(Rate effectiveCap) const override;
        Rate capletRate(Rate effectiveCap) const override;
        Real floorletPrice(Rate effectiveFloor) const override;
        Rate floorletRate(Rate effectiveFloor) const override;
        void initialize(const FloatingRateCoupon& coupon) override;
        //@}

    protected:
        const RangeAccrualFloatersCoupon* coupon_;
        Real startTime_;                                   // S
        Real endTime_;                                     // T
        Real accrualFactor_;                               // T-S
        std::vector<Real> observationTimeLags_;            // d
        std::vector<Real> observationTimes_;               // U
        std::vector<Real> initialValues_;
        Size observationsNo_;
        Real lowerTrigger_;
        Real upperTrigger_;
        Real discount_;
        Real gearing_;
        Spread spread_;
        Real spreadLegValue_;

    };

    class RangeAccrualPricerByBgm : public RangeAccrualPricer {

     public:
       RangeAccrualPricerByBgm(Real correlation,
                               ext::shared_ptr<SmileSection> smilesOnExpiry,
                               ext::shared_ptr<SmileSection> smilesOnPayment,
                               bool withSmile,
                               bool byCallSpread);
       //! \name Observer interface
       //@{
       Real swapletPrice() const override;
       //@}

     protected:

        Real drift(Real U, Real lambdaS, Real lambdaT, Real correlation) const;
        Real derDriftDerLambdaS(Real U, Real lambdaS, Real lambdaT,
                                Real correlation) const;
        Real derDriftDerLambdaT(Real U, Real lambdaS, Real lambdaT,
                                Real correlation) const;

        Real lambda(Real U, Real lambdaS, Real lambdaT) const;
        Real derLambdaDerLambdaS(Real U) const;
        Real derLambdaDerLambdaT(Real U) const;

        std::vector<Real> driftsOverPeriod(Real U, Real lambdaS, Real lambdaT,
                                           Real correlation) const;
        std::vector<Real> lambdasOverPeriod(Real U, Real lambdaS,
                                            Real lambdaT) const;

        Real digitalRangePrice(Real lowerTrigger,
                                Real upperTrigger,
                                Real initialValue,
                                Real expiry,
                                Real deflator) const;

        Real digitalPrice(Real strike,
                    Real initialValue,
                    Real expiry,
                    Real deflator) const;

        Real digitalPriceWithoutSmile(Real strike,
                    Real initialValue,
                    Real expiry,
                    Real deflator) const;

        Real digital