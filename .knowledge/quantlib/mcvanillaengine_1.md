  Size timeStepsPerYear,
        bool brownianBridge,
        bool antitheticVariate,
        bool controlVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed)
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
        this->registerWith(process_);
    }

    template <template <class> class MC, class RNG, class S, class Inst>
    inline typename MCVanillaEngine<MC,RNG,S,Inst>::result_type
    MCVanillaEngine<MC,RNG,S,Inst>::controlVariateValue() const {

        ext::shared_ptr<PricingEngine> controlPE =
            this->controlPricingEngine();
        QL_REQUIRE(controlPE,
                   "engine does not provide "
                   "control variation pricing engine");

        auto* controlArguments = dynamic_cast<typename Inst::arguments*>(controlPE->getArguments());

        QL_REQUIRE(controlArguments, "engine is using inconsistent arguments");

        *controlArguments = this->arguments_;
        controlPE->calculate();

        const auto* controlResults =
            dynamic_cast<const typename Inst::results*>(controlPE->getResults());
        QL_REQUIRE(controlResults,
                   "engine returns an inconsistent result type");

        return result_type(controlResults->value);
    }


    template <template <class> class MC, class RNG, class S, class Inst>
    inline TimeGrid MCVanillaEngine<MC,RNG,S,Inst>::timeGrid() const {
        Date lastExerciseDate = this->arguments_.exercise->lastDate();
        Time t = process_->time(lastExerciseDate);
        if (this->timeSteps_ != Null<Size>()) {
            return TimeGrid(t, this->timeSteps_);
        } else if (this->timeStepsPerYear_ != Null<Size>()) {
            Size steps = static_cast<Size>(this->timeStepsPerYear_*t);
            return TimeGrid(t, std::max<Size>(steps, 1));
        } else {
            QL_FAIL("time steps not specified");
        }
    }

}


#endif