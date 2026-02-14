Quote>(), // continuously
                                                        // compounded w.r.t. yts
                                                        // daycounter
            const Handle<YieldTermStructure> &discountCurve =
                Handle<YieldTermStructure>(),
            const Probabilities probabilities = None)
            : BasketGeneratingEngine(model, oas, discountCurve),
              GenericModelEngine<Gaussian1dModel,
                                 NonstandardSwaption::arguments,
                                 NonstandardSwaption::results>(model),
              integrationPoints_(integrationPoints), stddevs_(stddevs),
              extrapolatePayoff_(extrapolatePayoff),
              flatPayoffExtrapolation_(flatPayoffExtrapolation),
              discountCurve_(discountCurve), oas_(oas),
              probabilities_(probabilities) {

            if (!oas_.empty())
                registerWith(oas_);

            if (!discountCurve_.empty())
                registerWith(discountCurve_);
        }

        void calculate() const override;

      protected:
        Real underlyingNpv(const Date& expiry, Real y) const override;
        Swap::Type underlyingType() const override;
        const Date underlyingLastDate() const override;
        const Array initialGuess(const Date& expiry) const override;

      private:
        const int integrationPoints_;
        const Real stddevs_;
        const bool extrapolatePayoff_, flatPayoffExtrapolation_;
        const Handle<YieldTermStructure> discountCurve_;
        const Handle<Quote> oas_;
        const Probabilities probabilities_;
    };
}

#endif
