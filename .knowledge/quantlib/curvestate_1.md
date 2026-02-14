:vector<Time>& taus,
                                      std::vector<Rate>& cotSwapRates,
                                      std::vector<Real>& cotSwapAnnuities);

    void constantMaturityFromDiscountRatios( // Size i, // to be added later
        Size spanningForwards,
        Size firstValidIndex,
        const std::vector<DiscountFactor>& ds,
        const std::vector<Time>& taus,
        std::vector<Rate>& cotSwapRates,
        std::vector<Real>& cotSwapAnnuities);
}

#endif
