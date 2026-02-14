psPerYear,
                   bool brownianBridge,
                   bool antitheticVariate,
                   bool controlVariate,
                   Size requiredSamples,
                   Real requiredTolerance,
                   Size maxSamples,
                   BigNatural seed,
                   Size nCalibrationSamples)
        : MCLongstaffSchwartzPathEngine<PathMultiAssetOption::engine,
                                    MultiVariate,RNG>(processes,
                                                      timeSteps,
                                                      timeStepsPerYear,
                                                      brownianBridge,
                                                      antitheticVariate,
                                                      controlVariate,
                                                      requiredSamples,
                                                      requiredTolerance,
                                                      maxSamples,
                                                      seed,
                                                      nCalibrationSamples) {}

    template <class RNG>
    inline ext::shared_ptr<LongstaffSchwartzMultiPathPricer>
    MCAmericanPathEngine<RNG>::lsmPathPricer() const {

        ext::shared_ptr<StochasticProcessArray> processArray =
            ext::dynamic_pointer_cast<StochasticProcessArray>(this->process_);
        QL_REQUIRE(processArray && processArray->size()>0,
                   "Stochastic process array required");

        ext::shared_ptr<GeneralizedBlackScholesProcess> process =
            ext::dynamic_pointer_cast<GeneralizedBlackScholesProcess>(
               processArray->process(0));
        QL_REQUIRE(process, "generalized Black-Scholes process required");

        const TimeGrid theTimeGrid = this->timeGrid();

        const std::vector<Time> & times = theTimeGrid.mandatoryTimes();
        const Size numberOfTimes = times.size();

        const std::vector<Date> & fixings = this->arguments_.fixingDates;

        QL_REQUIRE(fixings.size() == numberOfTimes, "Invalid dates/times");

        std::vector<Size> timePositions(numberOfTimes);
        Array discountFactors(numberOfTimes);
        std::vector<Handle<YieldTermStructure> > forwardTermStructures(numberOfTimes);

        const Handle<YieldTermStructure> & riskFreeRate = process->riskFreeRate();

        for (Size i = 0; i < numberOfTimes; ++i) {
            timePositions[i] = theTimeGrid.index(times[i]);
            discountFactors[i] = riskFreeRate->discount(times[i]);
            forwardTermStructures[i] = Handle<YieldTermStructure>(
                ext::make_shared<ImpliedTermStructure>(riskFreeRate,
                                                         fixings[i]));
        }

        const Size polynomialOrder = 2;
        const LsmBasisSystem::PolynomialType polynomialType = LsmBasisSystem::Monomial;

        return ext::make_shared<LongstaffSchwartzMultiPathPricer> (
                                                 this->arguments_.payoff,
                                                 timePositions,
                                                 forwardTermStructures,
                                                 discountFactors,
                                                 polynomialOrder,
                                                 polynomialType);
    }


    template <class RNG>
    inline MakeMCAmericanPathEngine<RNG>::MakeMCAmericanPathEngine(
        ext::shared_ptr<StochasticProcessArray> process)
    : process_(std::move(process)), brownianBridge_(false), antithetic_(false),
      controlVariate_(false), steps_(Null<Size>()), stepsPerYear_(Null<Size>()),
      samples_(Null<Size>()), maxSamples_(Null<Size>()), calibrationSamples_(Null<Size>()),
      tolerance_(Null<Real>()), seed_(0) {}

    template <class RNG>
    inline MakeMCAmericanPathEngine<RNG>&
    MakeMCAmericanPathEngine<RNG>::withSteps(Si