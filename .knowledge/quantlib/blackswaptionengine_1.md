 *
                   blackFormulaStdDevDerivative(strike, atmForward, stdDev,
                                                annuity, displacement);
        }
        Real delta(const Option::Type type, const Real strike,
                   const Real atmForward, const Real stdDev, const Real annuity,
                   const Real displacement) {
            return blackFormulaForwardDerivative(type, strike, atmForward, stdDev,
                                                 annuity, displacement);
        }
    };

    // normal type engine
    struct BachelierSpec {
        static constexpr VolatilityType type = Normal;
        Real value(const Option::Type type, const Real strike,
                   const Real atmForward, const Real stdDev, const Real annuity,
                   const Real) {
            return bachelierBlackFormula(type, strike, atmForward, stdDev,
                                         annuity);
        }
        Real vega(const Real strike, const Real atmForward, const Real stdDev,
                  const Real exerciseTime, const Real annuity, const Real) {
            return std::sqrt(exerciseTime) *
                   bachelierBlackFormulaStdDevDerivative(
                       strike, atmForward, stdDev, annuity);
        }
        Real delta(const Option::Type type, const Real strike,
                   const Real atmForward, const Real stdDev, const Real annuity,
                   const Real) {
            return bachelierBlackFormulaForwardDerivative(
                type, strike, atmForward, stdDev, annuity);
        }
    };

    } // namespace detail

    //! Shifted Lognormal Black-formula swaption engine
    /*! \ingroup swaptionengines

        \warning The engine assumes that the exercise date lies before the
                 start date of the passed swap.
    */

    class BlackSwaptionEngine
        : public detail::BlackStyleSwaptionEngine<detail::Black76Spec> {
      public:
        BlackSwaptionEngine(const Handle<YieldTermStructure>& discountCurve,
                            Volatility vol,
                            const DayCounter& dc = Actual365Fixed(),
                            Real displacement = 0.0,
                            CashAnnuityModel model = DiscountCurve);
        BlackSwaptionEngine(const Handle<YieldTermStructure>& discountCurve,
                            const Handle<Quote>& vol,
                            const DayCounter& dc = Actual365Fixed(),
                            Real displacement = 0.0,
                            CashAnnuityModel model = DiscountCurve);
        BlackSwaptionEngine(const Handle<YieldTermStructure>& discountCurve,
                            const Handle<SwaptionVolatilityStructure>& vol,
                            CashAnnuityModel model = DiscountCurve);
    };

    //! Normal Bachelier-formula swaption engine
    /*! \ingroup swaptionengines

        \warning The engine assumes that the exercise date lies before the
                 start date of the passed swap.
    */

    class BachelierSwaptionEngine
        : public detail::BlackStyleSwaptionEngine<detail::BachelierSpec> {
      public:
        BachelierSwaptionEngine(const Handle<YieldTermStructure>& discountCurve,
                                Volatility vol,
                                const DayCounter& dc = Actual365Fixed(),
                                CashAnnuityModel model = DiscountCurve);
        BachelierSwaptionEngine(const Handle<YieldTermStructure>& discountCurve,
                                const Handle<Quote>& vol,
                                const DayCounter& dc = Actual365Fixed(),
                                CashAnnuityModel model = DiscountCurve);
        BachelierSwaptionEngine(const Handle<YieldTermStructure>& discountCurve,
                                const Handle<SwaptionVolatilityStructure>& vol,
                                CashAnnuityModel model = DiscountCurve);
    };

    // implementation

    namespace detai
