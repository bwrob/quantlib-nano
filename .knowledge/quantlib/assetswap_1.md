td::vector<Real> fixedCoupons;
        std::vector<Time> floatingAccrualTimes;
        std::vector<Date> floatingResetDates;
        std::vector<Date> floatingFixingDates;
        std::vector<Date> floatingPayDates;
        std::vector<Spread> floatingSpreads;
        void validate() const override;
    };

    //! %Results from simple swap calculation
    class AssetSwap::results : public Swap::results {
      public:
        Spread fairSpread;
        Real fairCleanPrice, fairNonParRepayment;
        void reset() override;
    };

}

#endif
