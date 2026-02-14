g approach is ok if the vol is at most
        // time-dependent. It is plain wrong if it is asset-dependent.
        // In the latter case the right solution would be stochastic
        // volatility or at least local volatility (which unfortunately
        // implies an unrealistic time-decreasing smile)
        Handle<BlackVolTermStructure> blackVolatility(
            ext::shared_ptr<BlackVolTermStructure>(
                new ImpliedVolTermStructure(process_->blackVolatility(),
                                            this->arguments_.resetDate)));

        ext::shared_ptr<GeneralizedBlackScholesProcess> fwdProcess(
                       new GeneralizedBlackScholesProcess(spot, dividendYield,
                                                          riskFreeRate,
                                                          blackVolatility));

        originalEngine_ = ext::shared_ptr<Engine>(new Engine(fwdProcess));
        originalEngine_->reset();

        originalArguments_ =
            dynamic_cast<VanillaOption::arguments*>(
                                             originalEngine_->getArguments());
        QL_REQUIRE(originalArguments_, "wrong engine type");
        originalResults_ =
            dynamic_cast<const VanillaOption::results*>(
                                               originalEngine_->getResults());
        QL_REQUIRE(originalResults_, "wrong engine type");

        originalArguments_->payoff = payoff;
        originalArguments_->exercise = this->arguments_.exercise;

        originalArguments_->validate();
    }

    template <class Engine>
    void ForwardVanillaEngine<Engine>::calculate() const {
        setup();
        originalEngine_->calculate();
        getOriginalResults();
    }

    template <class Engine>
    void ForwardVanillaEngine<Engine>::getOriginalResults() const {

        DayCounter rfdc = process_->riskFreeRate()->dayCounter();
        DayCounter divdc = process_->dividendYield()->dayCounter();
        Time resetTime = rfdc.yearFraction(
                                     process_->riskFreeRate()->referenceDate(),
                                     this->arguments_.resetDate);
        DiscountFactor discQ = process_->dividendYield()->discount(
                                                  this->arguments_.resetDate);

        this->results_.value = discQ * originalResults_->value;
        // I need the strike derivative here ...
        if (originalResults_->delta != Null<Real>() &&
            originalResults_->strikeSensitivity != Null<Real>()) {
            this->results_.delta = discQ * (originalResults_->delta +
                  this->arguments_.moneyness * 
                        originalResults_->strikeSensitivity);
        }
        this->results_.gamma = 0.0;
        this->results_.theta = process_->dividendYield()->
            zeroRate(this->arguments_.resetDate, divdc, Continuous, NoFrequency)
            * this->results_.value;
        if (originalResults_->vega != Null<Real>())
            this->results_.vega  = discQ * originalResults_->vega;
        if (originalResults_->rho != Null<Real>())
            this->results_.rho   = discQ *  originalResults_->rho;
        if (originalResults_->dividendRho != Null<Real>()) {
            this->results_.dividendRho = - resetTime * this->results_.value
               + discQ * originalResults_->dividendRho;
        }
    }

}


#endif