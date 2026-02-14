       const ext::shared_ptr<ZeroInflationIndex>& index,
                  const Period& observationLag,
                  CPI::InterpolationType observationInterpolation,
                  const DayCounter& dayCounter,
                  Real fixedRate,
                  const Date& refPeriodStart = Date(),
                  const Date& refPeriodEnd = Date(),
                  const Date& exCouponDate = Date());
        //@}

        //! \name Inspectors
        //@{
        //! fixed rate that will be inflated by the index ratio
        Real fixedRate() const;

        //! base value for the CPI index
        /*! \warning make sure that the interpolation used to create
                     this is what you are using for the fixing,
                     i.e. the observationInterpolation.
        */
        Rate baseCPI() const;

        //! base date for the base fixing of the CPI index
        Date baseDate() const;

        //! how do you observe the index?  as-is, flat, linear?
        CPI::InterpolationType observationInterpolation() const;

        //! index used
        ext::shared_ptr<ZeroInflationIndex> cpiIndex() const;
        //@}

        //! \name Calculations
        //@{
        Real accruedAmount(const Date&) const override;

        //! the index value observed (with a lag) at the end date
        Rate indexFixing() const override;

        //! the ratio between the index fixing at the passed date and the base CPI
        /*! No adjustments are applied */
        Rate indexRatio(Date d) const;

        //! the ratio between the end index fixing and the base CPI
        /*! This might include adjustments calculated by the pricer */
        Rate adjustedIndexGrowth() const;
        //@}

        //! \name Visitability
        //@{
        void accept(AcyclicVisitor&) override;
        //@}
      protected:
        Real baseCPI_;
        Real fixedRate_;
        CPI::InterpolationType observationInterpolation_;
        Date baseDate_;

        bool checkPricerImpl(const ext::shared_ptr<InflationCouponPricer>&) const override;
    };


    //! Cash flow paying the performance of a CPI (zero inflation) index
    /*! It is NOT a coupon, i.e. no accruals. */
    class CPICashFlow : public IndexedCashFlow {
      public:
        CPICashFlow(Real notional,
                    const ext::shared_ptr<ZeroInflationIndex>& index,
                    const Date& baseDate,
                    Real baseFixing,
                    const Date& observationDate,
                    const Period& observationLag,
                    CPI::InterpolationType interpolation,
                    const Date& paymentDate,
                    bool growthOnly = false);

        //! value used on base date
        /*! This does not have to agree with index on that date. */
        Real baseFixing() const override;
        //! you may not have a valid date
        Date baseDate() const override;

        Date observationDate() const { return observationDate_; }
        Period observationLag() const { return observationLag_; }
        //! do you want linear/constant/as-index interpolation of future data?
        virtual CPI::InterpolationType interpolation() const {
            return interpolation_;
        }
        virtual Frequency frequency() const { return frequency_; }

        ext::shared_ptr<ZeroInflationIndex> cpiIndex() const;

        Real indexFixing() const override;

      protected:
        Real baseFixing_;
        Date observationDate_;
        Period observationLag_;
        CPI::InterpolationType interpolation_;
        Frequency frequency_;
    };


    //! Helper class building a sequence of capped/floored CPI coupons.
    /*! Also allowing for the inflated notional at the end...
        especially if there is only one date in the schedule.
        If the fixed rate is zero you get a FixedRateCoupon, otherwise
        you get a ZeroInflationCoupon.
    */
    class CPILeg {
      public:
        CPILeg(Schedule schedule,
  