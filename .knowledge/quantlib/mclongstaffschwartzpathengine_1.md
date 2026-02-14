edTolerance,
        Size maxSamples,
        BigNatural seed,
        Size nCalibrationSamples)
    : McSimulation<MC, RNG, S>(antitheticVariate, controlVariate), process_(std::move(process)),
      timeSteps_(timeSteps), timeStepsPerYear_(timeStepsPerYear), brownianBridge_(brownianBridge),
      requiredSamples_(requiredSamples), requiredTolerance_(requiredTolerance),
      maxSamples_(maxSamples), seed_(seed),
      nCalibrationSamples_((nCalibrationSamples == Null<Size>()) ? 2048 : nCalibrationSamples) {
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
                   "timeStepsPerYear must be positive, "
                    << timeStepsPerYear << " not allowed");
        this->registerWith(process_);
    }

    template <class GenericEngine, template <class> class MC,
              class RNG, class S>
    inline
    ext::shared_ptr<typename
        MCLongstaffSchwartzPathEngine<GenericEngine,MC,RNG,S>::path_pricer_type>
        MCLongstaffSchwartzPathEngine<GenericEngine,MC,RNG,S>::pathPricer()
        const {

        QL_REQUIRE(pathPricer_, "path pricer unknown");
        return pathPricer_;
    }

    template <class GenericEngine, template <class> class MC,
              class RNG, class S>
    inline
    void MCLongstaffSchwartzPathEngine<GenericEngine,MC,RNG,S>::calculate()
    const {
        pathPricer_ = this->lsmPathPricer();
        this->mcModel_ = ext::shared_ptr<MonteCarloModel<MC,RNG,S> >(
                          new MonteCarloModel<MC,RNG,S>
                              (pathGenerator(), pathPricer_,
                               stats_type(), this->antitheticVariate_));

        this->mcModel_->addSamples(nCalibrationSamples_);
        this->pathPricer_->calibrate();

        McSimulation<MC,RNG,S>::calculate(requiredTolerance_,
                                          requiredSamples_,
                                          maxSamples_);
        this->results_.value = this->mcModel_->sampleAccumulator().mean();
        if constexpr (RNG::allowsErrorEstimate) {
            this->results_.errorEstimate =
                this->mcModel_->sampleAccumulator().errorEstimate();
        }
    }

    template <class GenericEngine, template <class> class MC,
              class RNG, class S>
    inline
    TimeGrid MCLongstaffSchwartzPathEngine<GenericEngine,MC,RNG,S>::timeGrid()
        const {
        const std::vector<Date> & fixings = this->arguments_.fixingDates;
        const Size numberOfFixings = fixings.size();

        std::vector<Time> fixingTimes(numberOfFixings);
        for (Size i = 0; i < numberOfFixings; ++i) {
            fixingTimes[i] =
                this->process_->time(fixings[i]);
        }

        const Size numberOfTimeSteps = timeSteps_ != Null<Size>() ? timeSteps_ : static_cast<Size>(timeStepsPerYear_ * fixingTimes.back());

        return TimeGrid(fixingTimes.begin(), fixingTimes.end(), numberOfTimeSteps);
     }

    template <class GenericEngine, template <class> class MC,
              class RNG, class S>
    inline
    ext::shared_ptr<typename
    MCLongstaffSchwartzPathEngine<GenericEngine,MC,RNG,S>::path_generator_type>
    MCLongstaffSchwartzPathEngine<GenericEngine,MC,RNG,S>::pathGenerator()
    const {

        Size dimensions = process_->factors();
        TimeGrid grid = this->timeGrid();
        typename RNG::rsg_type generator =
            RNG::make_sequence_generator(dimensions*(grid.size()-1),seed_);
        return ext::shared_ptr<path_generator_type>(
                   new path_generator_type(process_,
       