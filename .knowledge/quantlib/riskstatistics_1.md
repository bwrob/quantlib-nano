onst;
    };


    //! default risk measures tool
    /*! \test the correctness of the returned values is tested by
              checking them against numerical calculations.
    */
    typedef GenericRiskStatistics<GaussianStatistics> RiskStatistics;



    // inline definitions

    template <class S>
    inline Real GenericRiskStatistics<S>::semiVariance() const {
        return regret(this->mean());
    }

    template <class S>
    inline Real GenericRiskStatistics<S>::semiDeviation() const {
        return std::sqrt(semiVariance());
    }

    template <class S>
    inline Real GenericRiskStatistics<S>::downsideVariance() const {
        return regret(0.0);
    }

    template <class S>
    inline Real GenericRiskStatistics<S>::downsideDeviation() const {
        return std::sqrt(downsideVariance());
    }

    // template definitions

    template <class S>
    Real GenericRiskStatistics<S>::regret(Real target) const {
        // average over the range below the target
        std::pair<Real, Size> result = this->expectationValue(
            [=](Real xi) -> Real {
                Real d = (xi - target);
                return d * d;
            },
            [=](Real xi) -> bool { return xi < target; });
        Real x = result.first;
        Size N = result.second;
        QL_REQUIRE(N > 1,
                   "samples under target <= 1, unsufficient");
        return (N/(N-1.0))*x;
    }

    /*! \pre percentile must be in range [90%-100%) */
    template <class S>
    Real GenericRiskStatistics<S>::potentialUpside(Real centile)
        const {
        QL_REQUIRE(centile>=0.9 && centile<1.0,
                   "percentile (" << centile << ") out of range [0.9, 1.0)");

        // potential upside must be a gain, i.e., floored at 0.0
        return std::max<Real>(this->percentile(centile), 0.0);
    }

    /*! \pre percentile must be in range [90%-100%) */
    template <class S>
    Real GenericRiskStatistics<S>::valueAtRisk(Real centile) const {

        QL_REQUIRE(centile>=0.9 && centile<1.0,
                   "percentile (" << centile << ") out of range [0.9, 1.0)");

        // must be a loss, i.e., capped at 0.0 and negated
        return -std::min<Real>(this->percentile(1.0-centile), 0.0);
    }

    /*! \pre percentile must be in range [90%-100%) */
    template <class S>
    Real GenericRiskStatistics<S>::expectedShortfall(Real centile) const {
        QL_REQUIRE(centile>=0.9 && centile<1.0,
                   "percentile (" << centile << ") out of range [0.9, 1.0)");

        QL_ENSURE(this->samples() != 0, "empty sample set");
        Real target = -valueAtRisk(centile);
        std::pair<Real,Size> result =
            this->expectationValue([ ](Real xi) { return xi; },
                                   [=](Real xi) { return xi < target; });
        Real x = result.first;
        Size N = result.second;
        QL_ENSURE(N != 0, "no data below the target");
        // must be a loss, i.e., capped at 0.0 and negated
        return -std::min<Real>(x, 0.0);
    }

    template <class S>
    Real GenericRiskStatistics<S>::shortfall(Real target) const {
        QL_ENSURE(this->samples() != 0, "empty sample set");
        return this->expectationValue([=](Real x) -> Real { return x < target ? 1.0 : 0.0; }).first;
    }

    template <class S>
    Real GenericRiskStatistics<S>::averageShortfall(Real target)
        const {
        std::pair<Real,Size> result = this->expectationValue(
            [=](Real xi) -> Real { return target - xi; },
                                   [=](Real xi) { return xi < target; });
        Real x = result.first;
        Size N = result.second;
        QL_ENSURE(N != 0, "no data below the target");
        return x;
    }

}


#endif
