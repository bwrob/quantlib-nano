 (timeSteps_ != Null<Size>()) {
            return TimeGrid(t, this->timeSteps_);
        } else if (timeStepsPerYear_ != Null<Size>()) {
            Size steps = static_cast<Size>(timeStepsPerYear_*t);
            return TimeGrid(t, std::max<Size>(steps, 1));
        } else {
            QL_FAIL("time steps not specified");
        }
    }


    template <class RNG, class S>
    inline
    ext::shared_ptr<
        typename MCVarianceSwapEngine<RNG,S>::path_pricer_type>
    MCVarianceSwapEngine<RNG,S>::pathPricer() const {

        return ext::shared_ptr<
            typename MCVarianceSwapEngine<RNG,S>::path_pricer_type>(
                                            new VariancePathPricer(process_));
    }


    template <class RNG, class S>
    inline MakeMCVarianceSwapEngine<RNG, S>::MakeMCVarianceSwapEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process)
    : process_(std::move(process)), steps_(Null<Size>()), stepsPerYear_(Null<Size>()),
      samples_(Null<Size>()), maxSamples_(Null<Size>()), tolerance_(Null<Real>()) {}

    template <class RNG, class S>
    inline MakeMCVarianceSwapEngine<RNG,S>&
    MakeMCVarianceSwapEngine<RNG,S>::withSteps(Size steps) {
        steps_ = steps;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCVarianceSwapEngine<RNG,S>&
    MakeMCVarianceSwapEngine<RNG,S>::withStepsPerYear(Size steps) {
        stepsPerYear_ = steps;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCVarianceSwapEngine<RNG,S>&
    MakeMCVarianceSwapEngine<RNG,S>::withSamples(Size samples) {
        QL_REQUIRE(tolerance_ == Null<Real>(),
                   "tolerance already set");
        samples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCVarianceSwapEngine<RNG,S>&
    MakeMCVarianceSwapEngine<RNG,S>::withAbsoluteTolerance(Real tolerance) {
        QL_REQUIRE(samples_ == Null<Size>(),
                   "number of samples already set");
        QL_REQUIRE(RNG::allowsErrorEstimate,
                   "chosen random generator policy "
                   "does not allow an error estimate");
        tolerance_ = tolerance;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCVarianceSwapEngine<RNG,S>&
    MakeMCVarianceSwapEngine<RNG,S>::withMaxSamples(Size samples) {
        maxSamples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCVarianceSwapEngine<RNG,S>&
    MakeMCVarianceSwapEngine<RNG,S>::withSeed(BigNatural seed) {
        seed_ = seed;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCVarianceSwapEngine<RNG,S>&
    MakeMCVarianceSwapEngine<RNG,S>::withBrownianBridge(bool brownianBridge) {
        brownianBridge_ = brownianBridge;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCVarianceSwapEngine<RNG,S>&
    MakeMCVarianceSwapEngine<RNG,S>::withAntitheticVariate(bool b) {
        antithetic_ = b;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCVarianceSwapEngine<RNG,S>::
    operator ext::shared_ptr<PricingEngine>() const {
        QL_REQUIRE(steps_ != Null<Size>() || stepsPerYear_ != Null<Size>(),
                   "number of steps not given");
        QL_REQUIRE(steps_ == Null<Size>() || stepsPerYear_ == Null<Size>(),
                   "number of steps overspecified");
        return ext::shared_ptr<PricingEngine>(
                         new MCVarianceSwapEngine<RNG,S>(process_,
                                                         steps_,
                                                         stepsPerYear_,
                                                         brownianBridge_,
                                                         antithetic_,
                                                         samples_, tolerance_,
                                                         maxSamples_,

