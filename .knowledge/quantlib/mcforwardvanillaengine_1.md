rwardVanillaEngine(
        ext::shared_ptr<StochasticProcess> process,
        Size timeSteps,
        Size timeStepsPerYear,
        bool brownianBridge,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed,
        bool controlVariate)
    : McSimulation<MC, RNG, S>(antitheticVariate, controlVariate), process_(std::move(process)),
      timeSteps_(timeSteps), timeStepsPerYear_(timeStepsPerYear), requiredSamples_(requiredSamples),
      maxSamples_(maxSamples), requiredTolerance_(requiredTolerance),
      brownianBridge_(brownianBridge), seed_(seed) {
        QL_REQUIRE(timeSteps != Null<Size>() ||
                   timeStepsPerYear != Null<Size>(),
                   "no time steps provided");
        QL_REQUIRE(timeSteps == Null<Size>() ||
                   timeStepsPerYear == Null<Size>(),
                   "both time steps and time steps per year were provided");
        QL_REQUIRE(timeSteps != 0,
                   "timeSteps must be positive, " << timeSteps <<
                   " not allowed");
        QL_REQUIRE(timeStepsPerYear != 0,
                   "timeStepsPerYear must be positive, " << timeStepsPerYear <<
                   " not allowed");
        registerWith(process_);
    }

    template <template <class> class MC, class RNG, class S>
    inline TimeGrid MCForwardVanillaEngine<MC,RNG,S>::timeGrid() const {

        Date resetDate = arguments_.resetDate;
        Date lastExerciseDate = arguments_.exercise->lastDate();

        Time t1 = process_->time(resetDate);
        Time t2 = process_->time(lastExerciseDate);

        Size totalSteps = Null<Size>();
        if (this->timeSteps_ != Null<Size>()) {
            totalSteps = timeSteps_;
        } else if (this->timeStepsPerYear_ != Null<Size>()) {
            totalSteps = static_cast<Size>(this->timeStepsPerYear_*t2);
        }

        std::vector<Time> fixingTimes;
        fixingTimes.push_back(t1);
        fixingTimes.push_back(t2);

        return TimeGrid(fixingTimes.begin(), fixingTimes.end(), totalSteps);
    }

    template <template <class> class MC, class RNG, class S>
    inline Real MCForwardVanillaEngine<MC,RNG,S>::controlVariateValue() const {

        ext::shared_ptr<PricingEngine> controlPE =
                this->controlPricingEngine();
        QL_REQUIRE(controlPE, "engine does not provide "
                              "control variation pricing engine");

        // Create vanilla option arguments with the same payoff and expiry, but with
        // strike-reset equal to initial spot*moneyness, price analytically
        ext::shared_ptr<StrikedTypePayoff> payoff =
            ext::dynamic_pointer_cast<StrikedTypePayoff>(
                this->arguments_.payoff);
        QL_REQUIRE(payoff, "non-plain payoff given");

        Real spot = this->process_->initialValues()[0];
        Real moneyness = this->arguments_.moneyness;
        Real strike = moneyness * spot;

        ext::shared_ptr<StrikedTypePayoff> newPayoff(new
            PlainVanillaPayoff(payoff->optionType(), strike));

        auto* controlArguments = dynamic_cast<VanillaOption::arguments*>(controlPE->getArguments());

        controlArguments->payoff = newPayoff;
        controlArguments->exercise = this->arguments_.exercise;
        controlPE->calculate();

        const auto* controlResults =
            dynamic_cast<const VanillaOption::results*>(controlPE->getResults());

        return controlResults->value;
    }
}


#endif
