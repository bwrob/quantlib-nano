ardTermStructures,
                                    Array discounts);
        Real operator()(const MultiPath& multiPath) const override;

      private:
        ext::shared_ptr<PathPayoff> payoff_;
        std::vector<Size> timePositions_;
        std::vector<Handle<YieldTermStructure> > forwardTermStructures_;
        Array discounts_;
    };


    // template definitions

    template <class RNG, class S>
    inline MCPathBasketEngine<RNG, S>::MCPathBasketEngine(
        ext::shared_ptr<StochasticProcessArray> process,
        Size timeSteps,
        Size timeStepsPerYear,
        bool brownianBridge,
        bool antitheticVariate,
        bool controlVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed)
    : McSimulation<MultiVariate, RNG, S>(antitheticVariate, controlVariate),
      process_(std::move(process)), timeSteps_(timeSteps), timeStepsPerYear_(timeStepsPerYear),
      requiredSamples_(requiredSamples), maxSamples_(maxSamples),
      requiredTolerance_(requiredTolerance), brownianBridge_(brownianBridge), seed_(seed) {
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


    template<class RNG, class S>
    inline
    ext::shared_ptr<typename MCPathBasketEngine<RNG,S>::path_generator_type>
    MCPathBasketEngine<RNG,S>::pathGenerator() const {

        ext::shared_ptr<PathPayoff> payoff = arguments_.payoff;
        QL_REQUIRE(payoff, "non-basket payoff given");

        Size numAssets = process_->size();

        TimeGrid grid = timeGrid();

        typename RNG::rsg_type gen =
            RNG::make_sequence_generator(numAssets * (grid.size() - 1), seed_);

        return ext::shared_ptr<path_generator_type>(
                         new path_generator_type(process_,
                                                 grid, gen, brownianBridge_));
    }

    template <class RNG, class S>
    inline TimeGrid MCPathBasketEngine<RNG,S>::timeGrid() const {
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

    template <class RNG, class S>
    inline
    ext::shared_ptr<typename MCPathBasketEngine<RNG,S>::path_pricer_type>
    MCPathBasketEngine<RNG,S>::pathPricer() const {

        ext::shared_ptr<PathPayoff> payoff = arguments_.payoff;
        QL_REQUIRE(payoff, "non-basket payoff given");

        ext::shared_ptr<GeneralizedBlackScholesProcess> process =
            ext::dynamic_pointer_cast<GeneralizedBlackScholesProcess>(
                                                       process_->process(0));
        QL_REQUIRE(process, "Black-Scholes process required");

        const TimeGrid theTimeGrid = timeGrid();

        const std::vector<Time> & times = theTimeGrid.mandatoryTimes();
        const Size numberOfTimes = times.size();

        const std::vector<Date> & fixings = this->arguments_.fixingDates;

        QL_REQUIRE(fixings.size() == numberO