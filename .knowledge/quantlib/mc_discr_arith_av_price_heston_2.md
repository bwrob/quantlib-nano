on-plain payoff given");

        ext::shared_ptr<EuropeanExercise> exercise =
            ext::dynamic_pointer_cast<EuropeanExercise>(
                this->arguments_.exercise);
        QL_REQUIRE(exercise, "wrong exercise given");

        ext::shared_ptr<P> process =
            ext::dynamic_pointer_cast<P>(this->process_);
        QL_REQUIRE(process, "Heston like process required");

        return ext::shared_ptr<typename
            MCDiscreteArithmeticAPHestonEngine<RNG,S,P>::path_pricer_type>(
                new ArithmeticAPOHestonPathPricer(
                    payoff->optionType(),
                    payoff->strike(),
                    process->riskFreeRate()->discount(exercise->lastDate()),
                    fixingIndexes,
                    this->arguments_.runningAccumulator,
                    this->arguments_.pastFixings));
    }

    template <class RNG, class S, class P>
    inline ext::shared_ptr<
            typename MCDiscreteArithmeticAPHestonEngine<RNG,S,P>::path_pricer_type>
        MCDiscreteArithmeticAPHestonEngine<RNG,S,P>::controlPathPricer() const {

        // Keep track of the fixing indices, the path pricer will need to prod only these
        TimeGrid timeGrid = this->timeGrid();
        std::vector<Time> fixingTimes = timeGrid.mandatoryTimes();
        std::vector<Size> fixingIndexes;
        fixingIndexes.reserve(fixingTimes.size());
        for (Real fixingTime : fixingTimes) {
            fixingIndexes.push_back(timeGrid.closestIndex(fixingTime));
        }

        ext::shared_ptr<PlainVanillaPayoff> payoff =
            ext::dynamic_pointer_cast<PlainVanillaPayoff>(
                this->arguments_.payoff);
        QL_REQUIRE(payoff, "non-plain payoff given");

        ext::shared_ptr<EuropeanExercise> exercise =
            ext::dynamic_pointer_cast<EuropeanExercise>(
                this->arguments_.exercise);
        QL_REQUIRE(exercise, "wrong exercise given");

        ext::shared_ptr<P> process =
            ext::dynamic_pointer_cast<P>(this->process_);
        QL_REQUIRE(process, "Heston like process required");

        // TODO: Currently the analytic pricer does not support seasoned asian
        // options (coming soon). Once that is available, we will be able to
        // pass seasoning details to the path pricer (NB. NEED to pass them to
        // the analytic pricer as well in that case).

        return ext::shared_ptr<typename
            MCDiscreteArithmeticAPHestonEngine<RNG,S,P>::path_pricer_type>(
                new GeometricAPOHestonPathPricer(
                    payoff->optionType(),
                    payoff->strike(),
                    process->riskFreeRate()->discount(exercise->lastDate()),
                    fixingIndexes));
    }

    template <class RNG, class S, class P>
    inline MakeMCDiscreteArithmeticAPHestonEngine<RNG, S, P>::
        MakeMCDiscreteArithmeticAPHestonEngine(ext::shared_ptr<P> process)
    : process_(std::move(process)), samples_(Null<Size>()), maxSamples_(Null<Size>()),
      steps_(Null<Size>()), stepsPerYear_(Null<Size>()), tolerance_(Null<Real>()) {}

    template<class RNG, class S, class P>
    inline MakeMCDiscreteArithmeticAPHestonEngine<RNG,S,P>&
    MakeMCDiscreteArithmeticAPHestonEngine<RNG,S,P>::withSamples(Size samples) {
        QL_REQUIRE(tolerance_ == Null<Real>(),
                   "tolerance already set");
        samples_ = samples;
        return *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCDiscreteArithmeticAPHestonEngine<RNG,S,P>&
    MakeMCDiscreteArithmeticAPHestonEngine<RNG,S,P>::withAbsoluteTolerance(
                                                             Real tolerance) {
        QL_REQUIRE(samples_ == Null<Size>(),
                   "number of samples already set");
        QL_REQUIRE(RNG::allowsErrorEstimate,
                   "chosen random generator policy "
                   "does not allow an error estimate");
        tolerance_ = tolerance;
        retu
