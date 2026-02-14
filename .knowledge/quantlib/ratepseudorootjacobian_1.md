ctor<Time> taus_;
        std::vector<Matrix> pseudoBumps_;
        std::vector<Spread> displacements_;
        Size numberBumps_;
        Size factors_;

        //! workspace variables

        std::vector<Matrix> allDerivatives_;
    //    std::vector<Real> bumpedRates_;
        Matrix e_;
        std::vector<Real> ratios_;

    };


    class RatePseudoRootJacobianAllElements
    {
    public:
      RatePseudoRootJacobianAllElements(const Matrix& pseudoRoot,
                                        Size aliveIndex,
                                        Size numeraire,
                                        const std::vector<Time>& taus,
                                        std::vector<Spread> displacements);

      void getBumps(const std::vector<Rate>& oldRates,
                    const std::vector<Real>& oneStepDFs, // redundant info but saves time to pass in
                                                         // since will have been needed elsewhere
                    const std::vector<Rate>& newRates,   // redundant info but saves time to pass in
                                                         // since will have been needed elsewhere
                    const std::vector<Real>& gaussians,
                    std::vector<Matrix>&
                        B); // one Matrix for each rate, the elements of the matrix are the
                            // derivatives of that rate with respect to each pseudo-root element

    private:

        //! this data does not change after construction
        Matrix pseudoRoot_;
        Size aliveIndex_;
        std::vector<Time> taus_;
        std::vector<Matrix> pseudoBumps_;
        std::vector<Spread> displacements_;
        Size factors_;

        //! workspace

        Matrix e_;
        std::vector<Real> ratios_;

    };

}

#endif
