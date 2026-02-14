      Leg leg;
        // if not initialized by constructors means theres no flows.
        ext::shared_ptr<SimpleCashFlow> upfrontPayment;
        ext::shared_ptr<SimpleCashFlow> accrualRebate;
        bool settlesAccrual;
        bool paysAtDefaultTime;
        ext::shared_ptr<Claim> claim;
        Date protectionStart;
        Date maturity;
        void validate() const override;
    };

    class CreditDefaultSwap::results : public Instrument::results {
      public:
        Rate fairSpread;
        Rate fairUpfront;
        Real couponLegBPS;
        Real couponLegNPV;
        Real defaultLegNPV;
        Real upfrontBPS;
        Real upfrontNPV;
        Real accrualRebateNPV;
        void reset() override;
    };

    class CreditDefaultSwap::engine
        : public GenericEngine<CreditDefaultSwap::arguments,
                               CreditDefaultSwap::results> {};

    /*! Return the CDS maturity date given the CDS trade date, \p tradeDate, the CDS \p tenor and a CDS \p rule.

        A null date is returned when a \p rule of \c CDS2015 and a \p tenor length of zero fail to yield a valid
        CDS maturity date.

        \warning An exception will be thrown if the \p rule is not \c CDS2015, \c CDS or \c OldCDS.

        \warning An exception will be thrown if the \p rule is \c OldCDS and a \p tenor of 0 months is provided. This
                 restriction can be removed if 0M tenor was available before the CDS Big Bang 2009.

        \warning An exception will be thrown if the \p tenor is not a multiple of 3 months. For the avoidance of
                 doubt, a \p tenor of 0 months is supported.
    */
    Date cdsMaturity(const Date& tradeDate, const Period& tenor, DateGeneration::Rule rule);

}


#endif