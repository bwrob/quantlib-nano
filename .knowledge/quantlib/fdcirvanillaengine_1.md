& withFdmSchemeDesc(
            const FdmSchemeDesc& schemeDesc);

        MakeFdCIRVanillaEngine& withCashDividends(
            const std::vector<Date>& dividendDates,
            const std::vector<Real>& dividendAmounts);

        operator ext::shared_ptr<PricingEngine>() const;

      private:
        ext::shared_ptr<CoxIngersollRossProcess> cirProcess_;
        ext::shared_ptr<GeneralizedBlackScholesProcess> bsProcess_;
        DividendSchedule dividends_;
        const Real rho_;
        Size tGrid_ = 10, xGrid_ = 100, rGrid_ = 100, dampingSteps_ = 0;
        ext::shared_ptr<FdmSchemeDesc> schemeDesc_;
        ext::shared_ptr<FdmQuantoHelper> quantoHelper_;
    };
}

#endif