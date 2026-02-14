        // McSimulation implementation
        ext::shared_ptr<path_pricer_type> pathPricer() const override;
        TimeGrid timeGrid() const override;

        ext::shared_ptr<path_generator_type> pathGenerator() const override {

            Size dimensions = process_->factors();

            TimeGrid grid = timeGrid();
            typename RNG::rsg_type gen =
                RNG::make_sequence_generator(dimensions*(grid.size()-1),seed_);

            return ext::shared_ptr<path_generator_type>(
                         new path_generator_type(process_, grid, gen,
                                                 brownianBridge_));
        }
        // data members
        ext::shared_ptr<GeneralizedBlackScholesProcess> process_;
        Size timeSteps_, timeStepsPerYear_;
        Size requiredSamples_, maxSamples_;
        Real requiredTolerance_;
        bool brownianBridge_;
        BigNatural seed_;
    };


    //! Monte Carlo variance-swap engine factory
    template <class RNG = PseudoRandom, class S = Statistics>
    class MakeMCVarianceSwapEngine {
      public:
        MakeMCVarianceSwapEngine(ext::shared_ptr<GeneralizedBlackScholesProcess> process);
        // named parameters
        MakeMCVarianceSwapEngine& withSteps(Size steps);
        MakeMCVarianceSwapEngine& withStepsPerYear(Size steps);
        MakeMCVarianceSwapEngine& withBrownianBridge(bool b = true);
        MakeMCVarianceSwapEngine& withSamples(Size samples);
        MakeMCVarianceSwapEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCVarianceSwapEngine& withMaxSamples(Size samples);
        MakeMCVarianceSwapEngine& withSeed(BigNatural seed);
        MakeMCVarianceSwapEngine& withAntitheticVariate(bool b = true);
        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<GeneralizedBlackScholesProcess> process_;
        bool antithetic_ = false;
        Size steps_, stepsPerYear_, samples_, maxSamples_;
        Real tolerance_;
        bool brownianBridge_ = false;
        BigNatural seed_ = 0;
    };

    class VariancePathPricer : public PathPricer<Path> {
      public:
        VariancePathPricer(ext::shared_ptr<GeneralizedBlackScholesProcess> process)
        : process_(std::move(process)) {}
        Real operator()(const Path& path) const override;

      private:
        ext::shared_ptr<GeneralizedBlackScholesProcess> process_;
    };

    // inline definitions

    template <class RNG, class S>
    inline MCVarianceSwapEngine<RNG, S>::MCVarianceSwapEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Size timeSteps,
        Size timeStepsPerYear,
        bool brownianBridge,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed)
    : McSimulation<SingleVariate, RNG, S>(antitheticVariate, false), process_(std::move(process)),
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
    }


    template <class RNG, class S>
    inline TimeGrid MCVarianceSwapEngine<RNG,S>::timeGrid() const {

        Time t = this->process_->time(this->arguments_.maturityDate);

        if