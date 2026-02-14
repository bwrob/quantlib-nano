CLookbackEngine& withStepsPerYear(Size steps);
        MakeMCLookbackEngine& withBrownianBridge(bool b = true);
        MakeMCLookbackEngine& withAntitheticVariate(bool b = true);
        MakeMCLookbackEngine& withSamples(Size samples);
        MakeMCLookbackEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCLookbackEngine& withMaxSamples(Size samples);
        MakeMCLookbackEngine& withSeed(BigNatural seed);
        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<GeneralizedBlackScholesProcess> process_;
        bool brownianBridge_ = false, antithetic_ = false;
        Size steps_, stepsPerYear_, samples_, maxSamples_;
        Real tolerance_;
        BigNatural seed_ = 0;
    };


    // template definitions

    template <class I, class RNG, class S>
    inline MCLookbackEngine<I, RNG, S>::MCLookbackEngine(
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
        this->registerWith(process_);
    }


    template <class I, class RNG, class S>
    inline TimeGrid MCLookbackEngine<I,RNG,S>::timeGrid() const {

        Time residualTime = process_->time(this->arguments_.exercise->lastDate());
        if (timeSteps_ != Null<Size>()) {
            return TimeGrid(residualTime, timeSteps_);
        } else if (timeStepsPerYear_ != Null<Size>()) {
            Size steps = static_cast<Size>(timeStepsPerYear_*residualTime);
            return TimeGrid(residualTime, std::max<Size>(steps, 1));
        } else {
            QL_FAIL("time steps not specified");
        }
    }


    namespace detail {

        // these functions are specialized for each of the instruments.

        ext::shared_ptr<PathPricer<Path> >
        mc_lookback_path_pricer(
               const ContinuousFixedLookbackOption::arguments& args,
               const GeneralizedBlackScholesProcess& process,
               DiscountFactor discount);

        ext::shared_ptr<PathPricer<Path> >
        mc_lookback_path_pricer(
               const ContinuousPartialFixedLookbackOption::arguments& args,
               const GeneralizedBlackScholesProcess& process,
               DiscountFactor discount);

        ext::shared_ptr<PathPricer<Path> >
        mc_lookback_path_pricer(
               const ContinuousFloatingLookbackOption::arguments& args,
               const GeneralizedBlackScholesProcess& process,
               DiscountFactor discount);

        ext::shared_ptr<PathPricer<Path> >
        mc_lookback_path_pricer(
               const ContinuousPartialFloatingLookbackOption::arguments& args,
               const GeneralizedBlackScholesProcess& process,
               DiscountFactor discount);

    }


    template <class I, class RNG, class S>
    inline ext::shared_ptr<typename MCLookbackEngine<I,RNG,S>::pat
