        bool localVol_;
        Real illegalLocalVolOverwrite_;
        ext::shared_ptr<FdmQuantoHelper> quantoHelper_;
        CashDividendModel cashDividendModel_;
    };


    class MakeFdBlackScholesVanillaEngine {
      public:
        explicit MakeFdBlackScholesVanillaEngine(
            ext::shared_ptr<GeneralizedBlackScholesProcess> process);

        MakeFdBlackScholesVanillaEngine& withQuantoHelper(
            const ext::shared_ptr<FdmQuantoHelper>& quantoHelper);

        MakeFdBlackScholesVanillaEngine& withTGrid(Size tGrid);
        MakeFdBlackScholesVanillaEngine& withXGrid(Size xGrid);
        MakeFdBlackScholesVanillaEngine& withDampingSteps(
            Size dampingSteps);

        MakeFdBlackScholesVanillaEngine& withFdmSchemeDesc(
            const FdmSchemeDesc& schemeDesc);

        MakeFdBlackScholesVanillaEngine& withLocalVol(bool localVol);
        MakeFdBlackScholesVanillaEngine& withIllegalLocalVolOverwrite(
            Real illegalLocalVolOverwrite);

        MakeFdBlackScholesVanillaEngine& withCashDividends(
            const std::vector<Date>& dividendDates,
            const std::vector<Real>& dividendAmounts);

        MakeFdBlackScholesVanillaEngine& withCashDividendModel(
            FdBlackScholesVanillaEngine::CashDividendModel cashDividendModel);

        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<GeneralizedBlackScholesProcess> process_;
        DividendSchedule dividends_;
        Size tGrid_ = 100, xGrid_ = 100, dampingSteps_ = 0;
        ext::shared_ptr<FdmSchemeDesc> schemeDesc_;
        bool localVol_ = false;
        Real illegalLocalVolOverwrite_;
        ext::shared_ptr<FdmQuantoHelper> quantoHelper_;
        FdBlackScholesVanillaEngine::CashDividendModel cashDividendModel_ = FdBlackScholesVanillaEngine::Spot;
    };

}

#endif
