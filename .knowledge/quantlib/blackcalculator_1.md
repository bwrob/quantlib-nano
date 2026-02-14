t::shared_ptr<StrikedTypePayoff>& p);
        
        Real strike_, forward_, stdDev_, discount_, variance_;
        Real d1_, d2_;
        Real alpha_, beta_, DalphaDd1_, DbetaDd2_;
        Real n_d1_, cum_d1_, n_d2_, cum_d2_;
        Real x_, DxDs_, DxDstrike_;
    };

    // inline
    inline Real BlackCalculator::thetaPerDay(Real spot,
                                             Time maturity) const {
        return theta(spot, maturity)/365.0;
    }

    inline Real BlackCalculator::itmCashProbability() const {
        return cum_d2_;
    }

    inline Real BlackCalculator::itmAssetProbability() const {
        return cum_d1_;
    }

    inline Real BlackCalculator::alpha() const {
        return alpha_;
    }

    inline Real BlackCalculator::beta() const {
        return beta_;
    }

}

#endif