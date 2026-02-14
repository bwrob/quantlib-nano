            Real invstRecoveryRate = 0.999);
      /*! Creates an engine with a black volatility model for the 
        exposure. The volatility is given as a quote.
        If the investor default model is not given a default 
        free one is assumed.
        @param discountCurve Used in pricing.
        @param blackVol Black volatility used in the exposure model.
        @param ctptyDTS Counterparty default curve.
        @param ctptyRecoveryRate Counterparty recovey rate.
        @param invstDTS Investor (swap holder) default curve.
        @param invstRecoveryRate Investor recovery rate.
      */
      CounterpartyAdjSwapEngine(
          const Handle<YieldTermStructure>& discountCurve,
          const Handle<Quote>& blackVol,
          const Handle<DefaultProbabilityTermStructure>& ctptyDTS,
          Real ctptyRecoveryRate,
          const Handle<DefaultProbabilityTermStructure>& invstDTS =
              Handle<DefaultProbabilityTermStructure>(),
          Real invstRecoveryRate = 0.999);
      //@}
      void calculate() const override;

    private:
      Handle<PricingEngine> baseSwapEngine_;
      Handle<PricingEngine> swaptionletEngine_;
      Handle<YieldTermStructure> discountCurve_;
      Handle<DefaultProbabilityTermStructure> defaultTS_;	  
      Real ctptyRecoveryRate_;
      Handle<DefaultProbabilityTermStructure> invstDTS_;	  
      Real invstRecoveryRate_;
  };

}

#endif