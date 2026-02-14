                           Size dampingSteps = 0,
                              const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Hundsdorfer(),
                              ext::shared_ptr<LocalVolTermStructure> leverageFct = {},
                              Real mixingFactor = 1.0);

        void calculate() const override;

        // multiple strikes caching engine
        void update() override;
        void enableMultipleStrikesCaching(const std::vector<Real>& strikes);

        // helper method for Heston like engines
        FdmSolverDesc getSolverDesc(Real equityScaleFactor) const;

      private:
        DividendSchedule dividends_;
        const Size tGrid_, xGrid_, vGrid_, dampingSteps_;
        const FdmSchemeDesc schemeDesc_;
        const ext::shared_ptr<LocalVolTermStructure> leverageFct_;
        const ext::shared_ptr<FdmQuantoHelper> quantoHelper_;
        const Real mixingFactor_;

        std::vector<Real> strikes_;
        mutable std::vector<std::pair<VanillaOption::arguments,
                                      VanillaOption::results> >
                                                            cachedArgs2results_;
    };

    class MakeFdHestonVanillaEngine {
      public:
        explicit MakeFdHestonVanillaEngine(ext::shared_ptr<HestonModel> hestonModel);

        MakeFdHestonVanillaEngine& withQuantoHelper(
            const ext::shared_ptr<FdmQuantoHelper>& quantoHelper);

        MakeFdHestonVanillaEngine& withTGrid(Size tGrid);
        MakeFdHestonVanillaEngine& withXGrid(Size xGrid);
        MakeFdHestonVanillaEngine& withVGrid(Size vGrid);
        MakeFdHestonVanillaEngine& withDampingSteps(
            Size dampingSteps);

        MakeFdHestonVanillaEngine& withFdmSchemeDesc(
            const FdmSchemeDesc& schemeDesc);

        MakeFdHestonVanillaEngine& withLeverageFunction(
            ext::shared_ptr<LocalVolTermStructure>& leverageFct);

        MakeFdHestonVanillaEngine& withCashDividends(
            const std::vector<Date>& dividendDates,
            const std::vector<Real>& dividendAmounts);

        operator ext::shared_ptr<PricingEngine>() const;

      private:
        ext::shared_ptr<HestonModel> hestonModel_;
        DividendSchedule dividends_;
        Size tGrid_ = 100, xGrid_ = 100, vGrid_ = 50, dampingSteps_ = 0;
        ext::shared_ptr<FdmSchemeDesc> schemeDesc_;
        ext::shared_ptr<LocalVolTermStructure> leverageFct_;
        ext::shared_ptr<FdmQuantoHelper> quantoHelper_;
    };

}

#endif