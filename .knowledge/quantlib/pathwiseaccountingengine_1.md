se computation of Deltas and vegas
    // using Giles--Glasserman smoking adjoints method
    // note only works with displaced LMM, 
    // 
    // The method is intimately connected with log-normal Euler evolution 
    // 
    // We must work with discretely compounding MM account
    // To compute a vega means changing the pseudo-square root at each time step
    // So for each vega, we have a vector of matrices. So we need a vector of vectors of matrices to compute all the vegas.
    // We do the outermost vector by time step and inner one by which vega.
    // This is tested in MarketModelTest::testPathwiseVegas

    class PathwiseVegasAccountingEngine 
    {
      public:
        PathwiseVegasAccountingEngine(
            ext::shared_ptr<LogNormalFwdRateEuler> evolver, // method relies heavily on LMM Euler
            const Clone<MarketModelPathwiseMultiProduct>& product,
            ext::shared_ptr<MarketModel>
                pseudoRootStructure, // we need pseudo-roots and displacements
            const std::vector<std::vector<Matrix> >& VegaBumps,
            Real initialNumeraireValue);

        void multiplePathValues(std::vector<Real>& means,
                                std::vector<Real>& errors,
                                Size numberOfPaths);
      private:
          Real singlePathValues(std::vector<Real>& values);

        ext::shared_ptr<LogNormalFwdRateEuler> evolver_;
        Clone<MarketModelPathwiseMultiProduct> product_;
        ext::shared_ptr<MarketModel> pseudoRootStructure_;
        std::vector<Size> numeraires_;

        Real initialNumeraireValue_;
        Size numberProducts_;
        Size numberRates_;
        Size numberCashFlowTimes_;
        Size numberSteps_;
        Size numberBumps_;

        std::vector<RatePseudoRootJacobian> jacobianComputers_;

        
        bool doDeflation_;


        // workspace
        std::vector<Real> currentForwards_, lastForwards_;
        std::vector<Real> numerairesHeld_;
        std::vector<Size> numberCashFlowsThisStep_;
        std::vector<std::vector<MarketModelPathwiseMultiProduct::CashFlow> >
                                                         cashFlowsGenerated_;
        std::vector<MarketModelPathwiseDiscounter> discounters_;

        std::vector<Matrix> V_;  // one V for each product, with components for each time step and rate

        Matrix LIBORRatios_; // dimensions are step and rate number
        Matrix Discounts_; // dimensions are step and rate number, goes from 0 to n. P(t_0, t_j)

        Matrix StepsDiscountsSquared_; // dimensions are step and rate number
        std::vector<Real> stepsDiscounts_;

        Matrix LIBORRates_; // dimensions are step and rate number
        Matrix partials_; // dimensions are factor and rate

        Matrix vegasThisPath_; // dimensions are product and which vega
        std::vector<Matrix> jacobiansThisPaths_; // dimensions are step, rate and factor

        std::vector<Real> deflatorAndDerivatives_;
        std::vector<Real> fullDerivatives_;
        
        std::vector<std::vector<Size> > numberCashFlowsThisIndex_;
        std::vector<Matrix> totalCashFlowsThisIndex_; // need product cross times cross which sensitivity

        std::vector<std::vector<Size> > cashFlowIndicesThisStep_;

    };

   //! Engine collecting cash flows along a market-model simulation for doing pathwise computation of Deltas and vegas
    // using Giles--Glasserman smoking adjoints method
    // note only works with displaced LMM, 
    // 
    // The method is intimately connected with log-normal Euler evolution 
    // 
    // We must work with discretely compounding MM account
    // To compute a vega means changing the pseudo-square root at each time step
    // So for each vega, we have a vector of matrices. So we need a vector of vectors of matrices to compute all the vegas.
    // We do the outermost vector by time step and inner one by which vega.
    // This implementation is different in that all the 