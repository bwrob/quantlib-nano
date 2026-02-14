& withAntitheticVariate(bool b = true);
        MakeMCPagodaEngine& withSamples(Size samples);
        MakeMCPagodaEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCPagodaEngine& withMaxSamples(Size samples);
        MakeMCPagodaEngine& withSeed(BigNatural seed);
        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<StochasticProcessArray> process_;
        bool brownianBridge_ = false, antithetic_ = false;
        Size samples_, maxSamples_;
        Real tolerance_;
        BigNatural seed_ = 0;
    };


    class PagodaMultiPathPricer : public PathPricer<MultiPath> {
      public:
        PagodaMultiPathPricer(Real roof, Real fraction,
                              DiscountFactor discount);
        Real operator()(const MultiPath& multiPath) const override;

      private:
        DiscountFactor discount_;
        Real roof_, fraction_;
    };


    // template definitions

    template <class RNG, class S>
    inline MCPagodaEngine<RNG, S>::MCPagodaEngine(ext::shared_ptr<StochasticProcessArray> processes,
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
    inline TimeGrid MCPagodaEngine<RNG,S>::timeGrid() const {

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
    ext::shared_ptr<typename MCPagodaEngine<RNG,S>::path_pricer_type>
    MCPagodaEngine<RNG,S>::pathPricer() const {

        ext::shared_ptr<GeneralizedBlackScholesProcess> process =
            ext::dynamic_pointer_cast<GeneralizedBlackScholesProcess>(
                                                      processes_->process(0));
        QL_REQUIRE(process, "Black-Scholes process required");

        return ext::shared_ptr<
                         typename MCPagodaEngine<RNG,S>::path_pricer_type>(
            new PagodaMultiPathPricer(arguments_.roof, arguments_.fraction,
                                      process->riskFreeRate()->discount(
                                           arguments_.exercise->lastDate())));
    }


    template <class RNG, class S>
    inline MakeMCPagodaEngine<RNG, S>::MakeMCPagodaEngine(
        ext::shared_ptr<StochasticProcessArray> process)
    : process_(std::move(process)), samples_(Null<Size>()), maxSamples_(Null<Size>()),
      tolerance_(Null<Real>()) {}

    template <class RNG, class S>
    inline MakeMCPagodaEngine<RNG,S>&
    MakeMCPagodaEngine<RNG,S>::withBrownianBridge(bool brownianBridge) {
        brownianBridge_ = brownianBridge;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCPagodaEngine<RNG,S>&
    MakeMCPagodaEngine<RNG,S>::withAntitheticVariate(bool b) {
        antithetic_ = b;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCPagodaEngine<RNG,S>&
    MakeMCPagodaEngine<RNG,S>::withSamples(Si