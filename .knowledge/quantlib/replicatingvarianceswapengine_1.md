  weights_type& optionWeights) const {
        if (availStrikes.empty())
            return;

        std::vector<Real> strikes = availStrikes;

        // add end-strike for piecewise approximation
        switch (type) {
          case Option::Call:
            std::sort(strikes.begin(), strikes.end());
            strikes.push_back(strikes.back() + dk_);
            break;
          case Option::Put:
            std::sort(strikes.begin(), strikes.end(), std::greater<>());
            strikes.push_back(std::max(strikes.back() - dk_, 0.0));
            break;
          default:
            QL_FAIL("invalid option type");
        }

        // remove duplicate strikes
        auto last = std::unique(strikes.begin(), strikes.end());
        strikes.erase(last, strikes.end());

        // compute weights
        Real f = strikes.front();
        Real slope, prevSlope = 0.0;




        for (auto k=strikes.begin();
             // added end-strike discarded
             k<strikes.end()-1;
             ++k) {
            slope = std::fabs((computeLogPayoff(*(k+1), f) -
                               computeLogPayoff(*k, f))/
                              (*(k+1) - *k));
            ext::shared_ptr<StrikedTypePayoff> payoff(
                                            new PlainVanillaPayoff(type, *k));
            if ( k == strikes.begin() )
                optionWeights.emplace_back(payoff,slope);
            else
                optionWeights.emplace_back(payoff, slope - prevSlope);
            prevSlope = slope;
        }
    }


    inline Real ReplicatingVarianceSwapEngine::computeLogPayoff(
                         const Real strike,
                         const Real callPutStrikeBoundary) const {
        Real f = callPutStrikeBoundary;
        return (2.0/residualTime()) * (((strike - f)/f) - std::log(strike/f));
    }


    inline
    Real ReplicatingVarianceSwapEngine::computeReplicatingPortfolio(
                                    const weights_type& optionWeights) const {

        ext::shared_ptr<Exercise> exercise(
                               new EuropeanExercise(arguments_.maturityDate));
        ext::shared_ptr<PricingEngine> optionEngine(
                                        new AnalyticEuropeanEngine(process_));
        Real optionsValue = 0.0;

        for (auto i = optionWeights.begin(); i < optionWeights.end(); ++i) {
            ext::shared_ptr<StrikedTypePayoff> payoff = i->first;
            EuropeanOption option(payoff, exercise);
            option.setPricingEngine(optionEngine);
            Real weight = i->second;
            optionsValue += option.NPV() * weight;
        }

        Real f = optionWeights.front().first->strike();
        return 2.0 * riskFreeRate() -
            2.0/residualTime() *
            (((underlying()/riskFreeDiscount() - f)/f) +
             std::log(f/underlying())) +
            optionsValue/riskFreeDiscount();
    }


     // calculate variance via replicating portfolio
    inline void ReplicatingVarianceSwapEngine::calculate() const {
        weights_type optionWeigths;
        computeOptionWeights(callStrikes_, Option::Call, optionWeigths);
        computeOptionWeights(putStrikes_, Option::Put, optionWeigths);

        results_.variance = computeReplicatingPortfolio(optionWeigths);

        DiscountFactor riskFreeDiscount =
            process_->riskFreeRate()->discount(arguments_.maturityDate);
        Real multiplier;
        switch (arguments_.position) {
          case Position::Long:
            multiplier = 1.0;
            break;
          case Position::Short:
            multiplier = -1.0;
            break;
          default:
            QL_FAIL("Unknown position");
        }
        results_.value = multiplier * riskFreeDiscount * arguments_.notional *
            (results_.variance - arguments_.strike);

        results_.additionalResults["optionWeights"] = optionWeigths;
    }


    inline Real ReplicatingVarianceSwapEngine::underlying() const {
       