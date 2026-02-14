lyExercise>(
                this->arguments_.exercise);
        QL_REQUIRE(exercise, "wrong exercise given");
        QL_REQUIRE(!exercise->payoffAtExpiry(),
                   "payoff at expiry not handled");

        ext::shared_ptr<AmericanPathPricer> earlyExercisePathPricer(
            new AmericanPathPricer(this->arguments_.payoff,
                                   polynomialOrder_, polynomialType_));

        return ext::make_shared<LongstaffSchwartzPathPricer<Path> > (

                                      this->timeGrid(),
                                      earlyExercisePathPricer,
                                      *(process->riskFreeRate()));
    }

    template <class RNG, class S, class RNG_Calibration>
    inline ext::shared_ptr<PathPricer<Path> >
    MCAmericanEngine<RNG, S, RNG_Calibration>::controlPathPricer() const {
        ext::shared_ptr<StrikedTypePayoff> payoff =
            ext::dynamic_pointer_cast<StrikedTypePayoff>(
                this->arguments_.payoff);
        QL_REQUIRE(payoff, "StrikedTypePayoff needed for control variate");

        ext::shared_ptr<GeneralizedBlackScholesProcess> process =
            ext::dynamic_pointer_cast<GeneralizedBlackScholesProcess>(
                                                              this->process_);
        QL_REQUIRE(process, "generalized Black-Scholes process required");

        return ext::shared_ptr<PathPricer<Path> >(
            new EuropeanPathPricer(
                payoff->optionType(),
                payoff->strike(),
                process->riskFreeRate()->discount(this->timeGrid().back()))
            );
    }

    template <class RNG, class S, class RNG_Calibration>
    inline ext::shared_ptr<PricingEngine>
    MCAmericanEngine<RNG, S, RNG_Calibration>::controlPricingEngine() const {
        ext::shared_ptr<GeneralizedBlackScholesProcess> process =
            ext::dynamic_pointer_cast<GeneralizedBlackScholesProcess>(
                                                              this->process_);
        QL_REQUIRE(process, "generalized Black-Scholes process required");

        return ext::shared_ptr<PricingEngine>(
                                         new AnalyticEuropeanEngine(process));
    }

    template <class RNG, class S, class RNG_Calibration>
    inline Real
    MCAmericanEngine<RNG, S, RNG_Calibration>::controlVariateValue() const {
        ext::shared_ptr<PricingEngine> controlPE =
            this->controlPricingEngine();

        QL_REQUIRE(controlPE,
                   "engine does not provide "
                   "control variation pricing engine");

        auto* controlArguments = dynamic_cast<VanillaOption::arguments*>(controlPE->getArguments());
        *controlArguments = this->arguments_;
        controlArguments->exercise = ext::shared_ptr<Exercise>(
             new EuropeanExercise(this->arguments_.exercise->lastDate()));

        controlPE->calculate();

        const auto* controlResults =
            dynamic_cast<const VanillaOption::results*>(controlPE->getResults());

        return controlResults->value;
    }

    template <class RNG, class S, class RNG_Calibration>
    inline MakeMCAmericanEngine<RNG, S, RNG_Calibration>::MakeMCAmericanEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process)
    : process_(std::move(process)), steps_(Null<Size>()), stepsPerYear_(Null<Size>()),
      samples_(Null<Size>()), maxSamples_(Null<Size>()), tolerance_(Null<Real>()),
      antitheticCalibration_(ext::nullopt), seedCalibration_(Null<Size>()) {}

    template <class RNG, class S, class RNG_Calibration>
    inline MakeMCAmericanEngine<RNG, S, RNG_Calibration> &
    MakeMCAmericanEngine<RNG, S, RNG_Calibration>::withPolynomialOrder(Size polynomialOrder) {
        polynomialOrder_ = polynomialOrder;
        return *this;
    }

    template <class RNG, class S, class RNG_Calibration>
    inline MakeMCAmericanEngine<RNG, S, RNG_Calibration> &
    MakeMCAmericanEngine<RNG, S, RNG_C
