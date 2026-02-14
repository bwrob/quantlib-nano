linear combinations by the bumps are done as late as possible,
    // whereas PathwiseVegasAccountingEngine does them as early as possible. 
    // This is tested in MarketModelTest::testPathwiseVegas

    class PathwiseVegasOuterAccountingEngine 
    {
      public:
        PathwiseVegasOuterAccountingEngine(
            ext::shared_ptr<LogNormalFwdRateEuler> evolver, // method relies heavily on LMM Euler
            const Clone<MarketModelPathwiseMultiProduct>& product,
            ext::shared_ptr<MarketModel>
                pseudoRootStructure, // we need pseudo-roots and displacements
            const std::vector<std::vector<Matrix> >& VegaBumps,
            Real initialNumeraireValue);

        //! Use to get vegas with respect to VegaBumps
        void multiplePathValues(std::vector<Real>& means,
                                std::vector<Real>& errors,
                                Size numberOfPaths);

        //! Use to get vegas with respect to pseudo-root-elements
        void multiplePathValuesElementary(std::vector<Real>& means,
                                std::vector<Real>& errors,
                                Size numberOfPaths);

      private:
          Real singlePathValues(std::vector<Real>& values);

        ext::shared_ptr<LogNormalFwdRateEuler> evolver_;
        Clone<MarketModelPathwiseMultiProduct> product_;
        ext::shared_ptr<MarketModel> pseudoRootStructure_;
        std::vector<std::vector<Matrix> > vegaBumps_; 
        std::vector<Size> numeraires_;

        Real initialNumeraireValue_;
        Size numberProducts_;
        Size numberRates_;
        Size numberCashFlowTimes_;
        Size numberSteps_;
        Size factors_;
        Size numberBumps_;
        Size numberElementaryVegas_;

        std::vector<RatePseudoRootJacobianAllElements> jacobianComputers_;

        
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

        std::vector<std::vector<Matrix>   > elementary_vegas_ThisPath_;  // dimensions are product, step,  rate and factor
        std::vector<std::vector<Matrix> > jacobiansThisPaths_;                      // dimensions are step, rate, rate and factor

        std::vector<Real> deflatorAndDerivatives_;
        std::vector<Real> fullDerivatives_;
        
        std::vector<std::vector<Size> > numberCashFlowsThisIndex_;
        std::vector<Matrix> totalCashFlowsThisIndex_; // need product cross times cross which sensitivity

        std::vector<std::vector<Size> > cashFlowIndicesThisStep_;
/*
        // experimental

        std::vector<std::vector<Real> > gaussians_;
        int distinguishedFactor_;
        int distinguishedRate_;
        int  distinguishedStep_;

*/
    };

}

#endif