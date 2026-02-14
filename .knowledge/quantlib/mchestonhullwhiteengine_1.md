  HestonHullWhitePathPricer(Time exerciseTime,
                                  ext::shared_ptr<Payoff> payoff,
                                  ext::shared_ptr<HybridHestonHullWhiteProcess> process);

        Real operator()(const MultiPath& path) const override;

      private:
        Time exerciseTime_;
        ext::shared_ptr<Payoff> payoff_;
        ext::shared_ptr<HybridHestonHullWhiteProcess> process_;
    };


    template<class RNG,class S>
    inline MCHestonHullWhiteEngine<RNG,S>::MCHestonHullWhiteEngine(
              const ext::shared_ptr<HybridHestonHullWhiteProcess> & process,
              Size timeSteps,
              Size timeStepsPerYear,
              bool antitheticVariate,
              bool controlVariate,
              Size requiredSamples,
              Real requiredTolerance,
              Size maxSamples,
              BigNatural seed)
    : base_type(process, timeSteps, timeStepsPerYear,
                false, antitheticVariate,
                controlVariate, requiredSamples,
                requiredTolerance, maxSamples, seed),
      process_(process) {}

    template<class RNG,class S>
    inline void MCHestonHullWhiteEngine<RNG,S>::calculate() const {
        MCVanillaEngine<MultiVariate, RNG, S>::calculate();

        if (this->controlVariate_) {
            // control variate might lead to small negative
            // option values for deep OTM options
            this->results_.value = std::max(0.0, this->results_.value);
        }
    }

    template <class RNG,class S> inline
    ext::shared_ptr<typename MCHestonHullWhiteEngine<RNG,S>::path_pricer_type>
    MCHestonHullWhiteEngine<RNG,S>::pathPricer() const {

        ext::shared_ptr<Exercise> exercise = this->arguments_.exercise;

        QL_REQUIRE(exercise->type() == Exercise::European,
                       "only european exercise is supported");

        const Time exerciseTime = process_->time(exercise->lastDate());

        return ext::shared_ptr<path_pricer_type>(
             new HestonHullWhitePathPricer(exerciseTime,
                                           this->arguments_.payoff,
                                           process_));
    }

    template <class RNG, class S> inline
    ext::shared_ptr<
        typename MCHestonHullWhiteEngine<RNG,S>::path_pricer_type>
    MCHestonHullWhiteEngine<RNG,S>::controlPathPricer() const {

        ext::shared_ptr<HestonProcess> hestonProcess =
            process_->hestonProcess();

        QL_REQUIRE(hestonProcess, "first constituent of the joint stochastic "
                                  "process need to be of type HestonProcess");

        ext::shared_ptr<Exercise> exercise = this->arguments_.exercise;

        QL_REQUIRE(exercise->type() == Exercise::European,
                       "only european exercise is supported");

        const Time exerciseTime = process_->time(exercise->lastDate());

        return ext::shared_ptr<path_pricer_type>(
             new HestonHullWhitePathPricer(
                  exerciseTime,
                  this->arguments_.payoff,
                  process_) );
    }

    template <class RNG, class S> inline
    ext::shared_ptr<PricingEngine>
    MCHestonHullWhiteEngine<RNG,S>::controlPricingEngine() const {

        ext::shared_ptr<HestonProcess> hestonProcess =
            process_->hestonProcess();

        ext::shared_ptr<HullWhiteForwardProcess> hullWhiteProcess =
            process_->hullWhiteProcess();

        ext::shared_ptr<HestonModel> hestonModel(
                                              new HestonModel(hestonProcess));
        ext::shared_ptr<HullWhite> hwModel(
                              new HullWhite(hestonProcess->riskFreeRate(),
                                            hullWhiteProcess->a(),
                                            hullWhiteProcess->sigma()));

        return ext::shared_ptr<PricingEngine>(
                new AnalyticHestonHullWhiteEngine(hestonModel, hwModel, 144));
