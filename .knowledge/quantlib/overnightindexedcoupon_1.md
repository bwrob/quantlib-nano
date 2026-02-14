const { return lockoutDays_; }
        //! apply observation shift
        bool applyObservationShift() const { return applyObservationShift_; }
        //! is the spread compounded daily or added after compounding?
        bool compoundSpreadDaily() const { return compoundSpreadDaily_; }
        /*! effectiveSpread and effectiveIndexFixing are set such that
            coupon amount = notional * accrualPeriod * ( gearing * effectiveIndexFixing + effectiveSpread )
            notice that
              - gearing = 1 is required if compoundSpreadDaily = true
              - effectiveSpread = spread() if compoundSpreadDaily = false */
        Real effectiveSpread() const;
        Real effectiveIndexFixing() const;
        //! rate computation start date
        const Date& rateComputationStartDate() const { return rateComputationStartDate_; }
        //! rate computation end date
        const Date& rateComputationEndDate() const { return rateComputationEndDate_; }
        //@}
        //! \name FloatingRateCoupon interface
        //@{
        //! the date when the coupon is fully determined
        Date fixingDate() const override { return fixingDates_.back(); }
        Real accruedAmount(const Date&) const override;
        //@}
        //! \name Visitability
        //@{
        void accept(AcyclicVisitor&) override;
        //@}
        //! \name Telescopic property
        //! Telescopic formula cannot be used with lookback days
        //! being different than intrinsic index fixing delay.
        //! Only when index fixing delay is 0 and observation shift is used,
        //! we can apply telescopic formula, when applying lookback period.
        //@{
        bool canApplyTelescopicFormula() const {
            return fixingDays_ == index_->fixingDays() ||
                (applyObservationShift_ && index_->fixingDays() == 0);
        }
        //@}
      private:
        std::vector<Date> valueDates_, interestDates_, fixingDates_;
        mutable std::vector<Rate> fixings_;
        Size n_;
        std::vector<Time> dt_;
        RateAveraging::Type averagingMethod_;
        Natural lockoutDays_;
        bool applyObservationShift_;
        bool compoundSpreadDaily_;
        Date rateComputationStartDate_, rateComputationEndDate_;

        Rate averageRate(const Date& date) const;
    };

    //! capped floored overnight indexed coupon
    class CappedFlooredOvernightIndexedCoupon : public FloatingRateCoupon {
    public:
        /*! capped / floored compounded, backward-looking on coupon.  The cap can be applied to the
            effective period rate (the default) or to the daily rates. */
        explicit CappedFlooredOvernightIndexedCoupon(const ext::shared_ptr<OvernightIndexedCoupon>& underlying,
                                            Real cap = Null<Real>(),
                                            Real floor = Null<Real>(), 
                                            bool nakedOption = false,
                                            bool dailyCapFloor = false);

        //! \name Observer interface
        //@{
        void deepUpdate() override;
        //@}
        //! \name LazyObject interface
        //@{
        void performCalculations() const override;
        void alwaysForwardNotifications();
        //@}
        //! \name Coupon interface
        //@{
        Rate rate() const override;
        Rate convexityAdjustment() const override;
        //@}
        //! \name FloatingRateCoupon interface
        //@{
        Date fixingDate() const override { return underlying_->fixingDate(); }
        //@}
        //! cap
        Rate cap() const;
        //! floor
        Rate floor() const;
        //! effective cap of fixing
        Rate effectiveCap() const;
        //! effective floor of fixing
        Rate effectiveFloor() const;
        //! effective caplet volatility
        Real effectiveCapletVolatility() const;
        //! effective floorlet volatility
        Real effectiveFloorletVolatil