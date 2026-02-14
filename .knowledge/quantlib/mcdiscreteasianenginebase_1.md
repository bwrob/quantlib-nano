      results_.errorEstimate =
                    this->mcModel_->sampleAccumulator().errorEstimate();

            // Allow inspection of the timeGrid via additional results
            this->results_.additionalResults["TimeGrid"] = this->timeGrid();
        }

      protected:
        // McSimulation implementation
        TimeGrid timeGrid() const override;
        ext::shared_ptr<path_generator_type> pathGenerator() const override {

            Size dimensions = process_->factors();
            TimeGrid grid = this->timeGrid();
            typename RNG::rsg_type gen =
                RNG::make_sequence_generator(dimensions*(grid.size()-1),seed_);
            return ext::shared_ptr<path_generator_type>(
                         new path_generator_type(process_, grid,
                                                 gen, brownianBridge_));
        }
        Real controlVariateValue() const override;
        // data members
        ext::shared_ptr<StochasticProcess> process_;
        Size requiredSamples_, maxSamples_, timeSteps_, timeStepsPerYear_;
        Real requiredTolerance_;
        bool brownianBridge_;
        BigNatural seed_;
    };


    // template definitions

    template <template <class> class MC, class RNG, class S>
    inline MCDiscreteAveragingAsianEngineBase<MC, RNG, S>::MCDiscreteAveragingAsianEngineBase(
        ext::shared_ptr<StochasticProcess> process,
        bool brownianBridge,
        bool antitheticVariate,
        bool controlVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed,
        Size timeSteps,
        Size timeStepsPerYear)
    : McSimulation<MC, RNG, S>(antitheticVariate, controlVariate), process_(std::move(process)),
      requiredSamples_(requiredSamples), maxSamples_(maxSamples), timeSteps_(timeSteps),
      timeStepsPerYear_(timeStepsPerYear), requiredTolerance_(requiredTolerance),
      brownianBridge_(brownianBridge), seed_(seed) {
        registerWith(process_);
    }

    template <template <class> class MC, class RNG, class S>
    inline TimeGrid MCDiscreteAveragingAsianEngineBase<MC,RNG,S>::timeGrid() const {

        std::vector<Time> fixingTimes;
        Size i;
        for (i=0; i<arguments_.fixingDates.size(); i++) {
            Time t = process_->time(arguments_.fixingDates[i]);
            if (t>=0) {
                fixingTimes.push_back(t);
            }
        }

        if (fixingTimes.empty() ||
            (fixingTimes.size() == 1 && fixingTimes.front() == 0.0))
            throw detail::PastFixingsOnly();

        // Some models (eg. Heston) might request additional points in
        // the time grid to improve the accuracy of the discretization
        Date lastExerciseDate = this->arguments_.exercise->lastDate();
        Time t = process_->time(lastExerciseDate);

        if (this->timeSteps_ != Null<Size>()) {
            return TimeGrid(fixingTimes.begin(), fixingTimes.end(), timeSteps_);
        } else if (this->timeStepsPerYear_ != Null<Size>()) {
            return TimeGrid(fixingTimes.begin(), fixingTimes.end(),
                static_cast<Size>(this->timeStepsPerYear_*t));
        }

        return TimeGrid(fixingTimes.begin(), fixingTimes.end());
    }

    template<template <class> class MC, class RNG, class S>
    inline
    Real MCDiscreteAveragingAsianEngineBase<MC,RNG,S>::controlVariateValue() const {

        ext::shared_ptr<PricingEngine> controlPE =
                this->controlPricingEngine();
            QL_REQUIRE(controlPE,
                       "engine does not provide "
                       "control variation pricing engine");

            auto* controlArguments =
                dynamic_cast<DiscreteAveragingAsianOption::arguments*>(controlPE->getArguments());
            *controlArguments = arguments_;
            controlPE->calculate();

            const auto* controlResults =
                dynamic_cast<const DiscreteAveragingAsianOption::results*>(controlPE->g
