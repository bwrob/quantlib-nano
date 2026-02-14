MCHimalayaEngine& withSamples(Size samples);
        MakeMCHimalayaEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCHimalayaEngine& withMaxSamples(Size samples);
        MakeMCHimalayaEngine& withSeed(BigNatural seed);
        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<StochasticProcessArray> process_;
        bool brownianBridge_ = false, antithetic_ = false;
        Size samples_, maxSamples_;
        Real tolerance_;
        BigNatural seed_ = 0;
    };


    class HimalayaMultiPathPricer : public PathPricer<MultiPath> {
      public:
        HimalayaMultiPathPricer(ext::shared_ptr<Payoff> payoff, DiscountFactor discount);
        Real operator()(const MultiPath& multiPath) const override;

      private:
        ext::shared_ptr<Payoff> payoff_;
        DiscountFactor discount_;
    };

    // template definitions

    template <class RNG, class S>
    inline MCHimalayaEngine<RNG, S>::MCHimalayaEngine(
        ext::shared_ptr<StochasticProcessArray> processes,
        bool brownianBridge,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed)
    : McSimulation<MultiVariate, RNG, S>(antitheticVariate, false),
      processes_(std::move(processes)), requiredSamples_(requiredSamples), maxSamples_(maxSamples),
      requiredTolerance_(requiredTolerance), brownianBridge_(brownianBridge), seed_(seed) {
        registerWith(processes_);
    }

    template <class RNG, class S>
    inline TimeGrid MCHimalayaEngine<RNG,S>::timeGrid() const {

        std::vector<Time> fixingTimes;
        for (Size i=0; i<arguments_.fixingDates.size(); i++) {
            Time t = processes_->time(arguments_.fixingDates[i]);
            QL_REQUIRE(t >= 0.0, "seasoned options are not handled");
            if (i > 0) {
                QL_REQUIRE(t > fixingTimes.back(), "fixing dates not sorted");
            }
            fixingTimes.push_back(t);
        }

        return TimeGrid(fixingTimes.begin(), fixingTimes.end());
    }

    template <class RNG, class S>
    inline
    ext::shared_ptr<typename MCHimalayaEngine<RNG,S>::path_pricer_type>
    MCHimalayaEngine<RNG,S>::pathPricer() const {

        ext::shared_ptr<GeneralizedBlackScholesProcess> process =
            ext::dynamic_pointer_cast<GeneralizedBlackScholesProcess>(
                                                      processes_->process(0));
        QL_REQUIRE(process, "Black-Scholes process required");

        return ext::shared_ptr<
                         typename MCHimalayaEngine<RNG,S>::path_pricer_type>(
            new HimalayaMultiPathPricer(arguments_.payoff,
                                        process->riskFreeRate()->discount(
                                           arguments_.exercise->lastDate())));
    }


    template <class RNG, class S>
    inline MakeMCHimalayaEngine<RNG, S>::MakeMCHimalayaEngine(
        ext::shared_ptr<StochasticProcessArray> process)
    : process_(std::move(process)), samples_(Null<Size>()), maxSamples_(Null<Size>()),
      tolerance_(Null<Real>()) {}

    template <class RNG, class S>
    inline MakeMCHimalayaEngine<RNG,S>&
    MakeMCHimalayaEngine<RNG,S>::withBrownianBridge(bool brownianBridge) {
        brownianBridge_ = brownianBridge;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCHimalayaEngine<RNG,S>&
    MakeMCHimalayaEngine<RNG,S>::withAntitheticVariate(bool b) {
        antithetic_ = b;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCHimalayaEngine<RNG,S>&
    MakeMCHimalayaEngine<RNG,S>::withSamples(Size samples) {
        QL_REQUIRE(tolerance_ == Null<Real>(),
                   "tolerance already set");
        samples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCHimalayaEngine<RNG,S>&
    MakeMCHimalayaEngine<RNG,S>::withAbsoluteTole