 QuantoTermStructure(process_->dividendYield(),
                                        process_->riskFreeRate(),
                                        foreignRiskFreeRate_,
                                        process_->blackVolatility(),
                                        strike,
                                        exchangeRateVolatility_,
                                        exchangeRateATMlevel,
                                        correlation_->value())));
        Handle<BlackVolTermStructure> blackVol = process_->blackVolatility();

        ext::shared_ptr<GeneralizedBlackScholesProcess> quantoProcess(
                  new GeneralizedBlackScholesProcess(spot, dividendYield,
                                                     riskFreeRate, blackVol));

        ext::shared_ptr<Engine> originalEngine(new Engine(quantoProcess));
        originalEngine->reset();
        auto* originalArguments =
            dynamic_cast<typename Instr::arguments*>(originalEngine->getArguments());
        QL_REQUIRE(originalArguments, "wrong engine type");

        *originalArguments = this->arguments_;

        originalArguments->validate();
        originalEngine->calculate();

        const auto* originalResults =
            dynamic_cast<const typename Instr::results*>(originalEngine->getResults());
        QL_REQUIRE(originalResults, "wrong engine type");

        this->results_.value = originalResults->value;
        this->results_.delta = originalResults->delta;
        this->results_.gamma = originalResults->gamma;
        this->results_.theta = originalResults->theta;
        if (originalResults->rho != Null<Real>() &&
            originalResults->dividendRho != Null<Real>()) {
            this->results_.rho = originalResults->rho +
                originalResults->dividendRho;
            this->results_.dividendRho = originalResults->dividendRho;
        } else {
            this->results_.rho = this->results_.dividendRho = Null<Real>();
        }
        Volatility exchangeRateFlatVol =
            exchangeRateVolatility_->blackVol(
                                        this->arguments_.exercise->lastDate(),
                                        exchangeRateATMlevel);
        if (originalResults->vega != Null<Real>()
            && originalResults->dividendRho != Null<Real>()) {
            this->results_.vega = originalResults->vega +
                correlation_->value() * exchangeRateFlatVol *
                originalResults->dividendRho;
        } else {
            this->results_.vega = Null<Real>();
        }

        if (originalResults->dividendRho != Null<Real>()) {
            Volatility volatility = process_->blackVolatility()->blackVol(
                                        this->arguments_.exercise->lastDate(),
                                        process_->stateVariable()->value());
            this->results_.qvega = correlation_->value() *
                process_->blackVolatility()->blackVol(
                                        this->arguments_.exercise->lastDate(),
                                        process_->stateVariable()->value()) *
                originalResults->dividendRho;
            this->results_.qrho = - originalResults->dividendRho;
            this->results_.qlambda = exchangeRateFlatVol *
                volatility * originalResults->dividendRho;
        } else {
            this->results_.qvega = this->results_.qrho =
                this->results_.qlambda = Null<Real>();
        }
    }

}


#endif