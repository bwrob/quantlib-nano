teVariable() const;
        const Handle<YieldTermStructure>& dividendYield() const;
        const Handle<YieldTermStructure>& riskFreeRate() const;
        const Handle<BlackVolTermStructure>& blackVolatility() const;
        const Handle<LocalVolTermStructure>& localVolatility() const;
        //@}
      private:
        Handle<Quote> x0_;
        Handle<YieldTermStructure> riskFreeRate_, dividendYield_;
        Handle<BlackVolTermStructure> blackVolatility_;
        Handle<LocalVolTermStructure> externalLocalVolTS_;
        bool forceDiscretization_;
        bool hasExternalLocalVol_;
        mutable RelinkableHandle<LocalVolTermStructure> localVolatility_;
        mutable bool updated_, isStrikeIndependent_;
    };

    //! Black-Scholes (1973) stochastic process
    /*! This class describes the stochastic process \f$ S \f$ for a stock
        given by
        \f[
            d\ln S(t) = (r(t) - \frac{\sigma(t, S)^2}{2}) dt + \sigma dW_t.
        \f]

        \warning while the interface is expressed in terms of \f$ S \f$,
                 the internal calculations work on \f$ ln S \f$.

        \ingroup processes
    */
    class BlackScholesProcess : public GeneralizedBlackScholesProcess {
      public:
        BlackScholesProcess(
            const Handle<Quote>& x0,
            const Handle<YieldTermStructure>& riskFreeTS,
            const Handle<BlackVolTermStructure>& blackVolTS,
            const ext::shared_ptr<discretization>& d =
                  ext::shared_ptr<discretization>(new EulerDiscretization),
            bool forceDiscretization = false);
    };

    //! Merton (1973) extension to the Black-Scholes stochastic process
    /*! This class describes the stochastic process ln(S) for a stock or
        stock index paying a continuous dividend yield given by
        \f[
            d\ln S(t, S) = (r(t) - q(t) - \frac{\sigma(t, S)^2}{2}) dt
                     + \sigma dW_t.
        \f]

        \ingroup processes
    */
    class BlackScholesMertonProcess : public GeneralizedBlackScholesProcess {
      public:
        BlackScholesMertonProcess(
            const Handle<Quote>& x0,
            const Handle<YieldTermStructure>& dividendTS,
            const Handle<YieldTermStructure>& riskFreeTS,
            const Handle<BlackVolTermStructure>& blackVolTS,
            const ext::shared_ptr<discretization>& d =
                  ext::shared_ptr<discretization>(new EulerDiscretization),
            bool forceDiscretization = false);
    };

    //! Black (1976) stochastic process
    /*! This class describes the stochastic process \f$ S \f$ for a
        forward or futures contract given by
        \f[
            d\ln S(t) = -\frac{\sigma(t, S)^2}{2} dt + \sigma dW_t.
        \f]

        \warning while the interface is expressed in terms of \f$ S \f$,
                 the internal calculations work on \f$ ln S \f$.

        \ingroup processes
    */
    class BlackProcess : public GeneralizedBlackScholesProcess {
      public:
        BlackProcess(
            const Handle<Quote>& x0,
            const Handle<YieldTermStructure>& riskFreeTS,
            const Handle<BlackVolTermStructure>& blackVolTS,
            const ext::shared_ptr<discretization>& d =
                  ext::shared_ptr<discretization>(new EulerDiscretization),
            bool forceDiscretization = false);
    };

    //! Garman-Kohlhagen (1983) stochastic process
    /*! This class describes the stochastic process \f$ S \f$ for an exchange
        rate given by
        \f[
            d\ln S(t) = (r(t) - r_f(t) - \frac{\sigma(t, S)^2}{2}) dt
                     + \sigma dW_t.
        \f]

        \warning while the interface is expressed in terms of \f$ S \f$,
                 the internal calculations work on \f$ ln S \f$.

        \ingroup processes
    */
    class GarmanKohlagenProcess : public GeneralizedBlackScholesProcess {
      public:
        GarmanKohlagenProcess(
            const Handle<Quote>& x0,
            const Handle<