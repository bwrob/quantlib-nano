_ptr<StrikedTypePayoff>& p);

        //! Member variables
        Real strike_, forward_, stdDev_, discount_, variance_;
        Real d_;  // Single d parameter for Bachelier model
        Real alpha_, beta_, DalphaDd_, DbetaDd_;  // Simplified derivative names
        Real n_d_, cum_d_;  // Single normal distribution values
        Real x_, DxDs_, DxDstrike_;
    };

    // inline
    inline Real BachelierCalculator::thetaPerDay(Real spot,
                                               Time maturity) const {
        return theta(spot, maturity)/365.0;
    }

    inline Real BachelierCalculator::itmCashProbability() const {
        // For Bachelier model:
        // Call ITM probability: P(F > K) = N(d) where d = (F-K)/σ
        // Put ITM probability:  P(F < K) = N(-d) = 1 - N(d) where d = (F-K)/σ

        if (alpha_ >= 0) { // Call option (alpha_ = N(d) >= 0)
            return cum_d_;  // N(d)
        } else { // Put option (alpha_ = N(d) - 1 < 0)
            return 1.0 - cum_d_;  // N(-d) = 1 - N(d)
        }
    }

    inline Real BachelierCalculator::itmAssetProbability() const {
        // In Bachelier model, asset probability is the same as cash probability
        // since there's no drift adjustment like in Black-Scholes
        // Call ITM probability: P(F > K) = N(d) where d = (F-K)/σ
        // Put ITM probability:  P(F < K) = N(-d) = 1 - N(d) where d = (F-K)/σ

        if (alpha_ >= 0) { // Call option
            return cum_d_;  // N(d)
        } else { // Put option
            return 1.0 - cum_d_;  // N(-d) = 1 - N(d)
        }
    }

    inline Real BachelierCalculator::alpha() const {
        return alpha_;
    }

    inline Real BachelierCalculator::beta() const {
        return beta_;
    }

}

#endif
