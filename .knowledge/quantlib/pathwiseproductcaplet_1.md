tedNumeraires() const override;
       const EvolutionDescription& evolution() const override;
       std::vector<Time> possibleCashFlowTimes() const override;
       Size numberOfProducts() const override;
       Size maxNumberOfCashFlowsPerProductPerStep() const override;

       // has division by the numeraire already been done?
       bool alreadyDeflated() const override;


       //! during simulation put product at start of path
       void reset() override;

       //! return value indicates whether path is finished, TRUE means done

       bool nextTimeStep(const CurveState& currentState,
                         std::vector<Size>& numberCashFlowsThisStep,
                         std::vector<std::vector<MarketModelPathwiseMultiProduct::CashFlow> >&
                             cashFlowsGenerated) override;

        //! returns a newly-allocated copy of itself
        std::unique_ptr<MarketModelPathwiseMultiProduct> clone() const override;

    private:
        std::vector<Real> rateTimes_;
        std::vector<Real> accruals_;
        std::vector<Time> paymentTimes_;
        std::vector<Rate> strikes_;
        Size numberRates_;
        // things that vary in a path
        Size currentIndex_;

        EvolutionDescription evolution_;
    };

    /*! MarketModelPathwiseMultiDeflatedCap to price several caps and get their derivatives
    simultaneously. Mainly useful for testing pathwise market vegas code.

    */

  class MarketModelPathwiseMultiDeflatedCap : public MarketModelPathwiseMultiProduct
    {
     public:
       MarketModelPathwiseMultiDeflatedCap(const std::vector<Time>& rateTimes,
                                           const std::vector<Real>& accruals,
                                           const std::vector<Time>& paymentTimes,
                                           Rate strike,
                                           std::vector<std::pair<Size, Size> > startsAndEnds);


       ~MarketModelPathwiseMultiDeflatedCap() override = default;

       std::vector<Size> suggestedNumeraires() const override;
       const EvolutionDescription& evolution() const override;
       std::vector<Time> possibleCashFlowTimes() const override;
       Size numberOfProducts() const override;
       Size maxNumberOfCashFlowsPerProductPerStep() const override;

       // has division by the numeraire already been done?
       bool alreadyDeflated() const override;


       //! during simulation put product at start of path
       void reset() override;

       //! return value indicates whether path is finished, TRUE means done

       bool nextTimeStep(const CurveState& currentState,
                         std::vector<Size>& numberCashFlowsThisStep,
                         std::vector<std::vector<MarketModelPathwiseMultiProduct::CashFlow> >&
                             cashFlowsGenerated) override;

        //! returns a newly-allocated copy of itself
        std::unique_ptr<MarketModelPathwiseMultiProduct> clone() const override;

    private:
        MarketModelPathwiseMultiDeflatedCaplet underlyingCaplets_;

        Size numberRates_;

        std::vector<std::pair<Size,Size> > startsAndEnds_;

        // things that vary in a path
        Size currentIndex_;
        std::vector<Size> innerCashFlowSizes_;
        std::vector<std::vector<MarketModelPathwiseMultiProduct::CashFlow> > innerCashFlowsGenerated_;

    };


}
#endif
