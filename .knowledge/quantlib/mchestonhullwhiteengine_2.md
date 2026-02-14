    }

    template <class RNG, class S> inline
    ext::shared_ptr<
        typename MCHestonHullWhiteEngine<RNG,S>::path_generator_type>
    MCHestonHullWhiteEngine<RNG,S>::controlPathGenerator() const {

        Size dimensions = process_->factors();
        TimeGrid grid = this->timeGrid();
        typename RNG::rsg_type generator =
            RNG::make_sequence_generator(dimensions*(grid.size()-1),
                                         this->seed_);

        ext::shared_ptr<HybridHestonHullWhiteProcess> cvProcess(
            new HybridHestonHullWhiteProcess(process_->hestonProcess(),
                                             process_->hullWhiteProcess(),
                                             0.0,
                                             process_->discretization()));

        return ext::shared_ptr<path_generator_type>(
                  new path_generator_type(cvProcess, grid, generator, false));
    }


    template <class RNG, class S>
    inline MakeMCHestonHullWhiteEngine<RNG, S>::MakeMCHestonHullWhiteEngine(
        ext::shared_ptr<HybridHestonHullWhiteProcess> process)
    : process_(std::move(process)), steps_(Null<Size>()), stepsPerYear_(Null<Size>()),
      samples_(Null<Size>()), maxSamples_(Null<Size>()), tolerance_(Null<Real>()) {}

    template <class RNG, class S>
    inline MakeMCHestonHullWhiteEngine<RNG,S>&
    MakeMCHestonHullWhiteEngine<RNG,S>::withSteps(Size steps) {
        steps_ = steps;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCHestonHullWhiteEngine<RNG,S>&
    MakeMCHestonHullWhiteEngine<RNG,S>::withStepsPerYear(Size steps) {
        stepsPerYear_ = steps;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCHestonHullWhiteEngine<RNG,S>&
    MakeMCHestonHullWhiteEngine<RNG,S>::withAntitheticVariate(bool b) {
        antithetic_ = b;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCHestonHullWhiteEngine<RNG,S>&
    MakeMCHestonHullWhiteEngine<RNG,S>::withControlVariate(bool b) {
        controlVariate_ = b;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCHestonHullWhiteEngine<RNG,S>&
    MakeMCHestonHullWhiteEngine<RNG,S>::withSamples(Size samples) {
        QL_REQUIRE(tolerance_ == Null<Real>(),
                   "tolerance already set");
        samples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCHestonHullWhiteEngine<RNG,S>&
    MakeMCHestonHullWhiteEngine<RNG,S>::withAbsoluteTolerance(Real tolerance) {
        QL_REQUIRE(samples_ == Null<Size>(),
                   "number of samples already set");
        QL_REQUIRE(RNG::allowsErrorEstimate,
                   "chosen random generator policy "
                   "does not allow an error estimate");
        tolerance_ = tolerance;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCHestonHullWhiteEngine<RNG,S>&
    MakeMCHestonHullWhiteEngine<RNG,S>::withMaxSamples(Size samples) {
        maxSamples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCHestonHullWhiteEngine<RNG,S>&
    MakeMCHestonHullWhiteEngine<RNG,S>::withSeed(BigNatural seed) {
        seed_ = seed;
        return *this;
    }

    template <class RNG, class S>
    inline
    MakeMCHestonHullWhiteEngine<RNG,S>::operator
    ext::shared_ptr<PricingEngine>() const {
        QL_REQUIRE(steps_ != Null<Size>() || stepsPerYear_ != Null<Size>(),
                   "number of steps not given");
        QL_REQUIRE(steps_ == Null<Size>() || stepsPerYear_ == Null<Size>(),
                   "number of steps overspecified");
        return ext::shared_ptr<PricingEngine>(new
            MCHestonHullWhiteEngine<RNG,S>(process_,
                                           steps_,
                                           stepsPerYear_,
                                           antithetic_,
                                         