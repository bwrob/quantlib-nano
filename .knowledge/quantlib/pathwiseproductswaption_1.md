e;


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
        std::vector<Rate> strikes_;
        Size numberRates_;
        // things that vary in a path
        Size currentIndex_;

        EvolutionDescription evolution_;

        Real bumpSize_;
        LMMCurveState up_;
        LMMCurveState down_;
        std::vector<Rate> forwards_;
    };




}


#endif