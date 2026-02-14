opt,
                                  BigNatural seedCalibration = Null<Size>());

        void calculate() const override;

      protected:
        virtual ext::shared_ptr<LongstaffSchwartzPathPricer<path_type> >
                                                   lsmPathPricer() const = 0;

        TimeGrid timeGrid() const override;
        ext::shared_ptr<path_pricer_type> pathPricer() const override;
        ext::shared_ptr<path_generator_type> pathGenerator() const override;

        ext::shared_ptr<StochasticProcess> process_;
        const Size timeSteps_;
        const Size timeStepsPerYear_;
        const bool brownianBridge_;
        const Size requiredSamples_;
        const Real requiredTolerance_;
        const Size maxSamples_;
        const BigNatural seed_;
        const Size nCalibrationSamples_;
        const bool brownianBridgeCalibration_;
        const bool antitheticVariateCalibration_;
        const BigNatural seedCalibration_;

        mutable ext::shared_ptr<LongstaffSchwartzPathPricer<path_type> >
            pathPricer_;
        mutable ext::shared_ptr<MonteCarloModel<MC, RNG_Calibration, S> >
            mcModelCalibration_;
    };

    template <class GenericEngine,
              template <class>
              class MC,
              class RNG,
              class S,
              class RNG_Calibration>
    inline MCLongstaffSchwartzEngine<GenericEngine, MC, RNG, S, RNG_Calibration>::
        MCLongstaffSchwartzEngine(ext::shared_ptr<StochasticProcess> process,
                                  Size timeSteps,
                                  Size timeStepsPerYear,
                                  bool brownianBridge,
                                  bool antitheticVariate,
                                  bool controlVariate,
                                  Size requiredSamples,
                                  Real requiredTolerance,
                                  Size maxSamples,
                                  BigNatural seed,
                                  Size nCalibrationSamples,
                                  ext::optional<bool> brownianBridgeCalibration,
                                  ext::optional<bool> antitheticVariateCalibration,
                                  BigNatural seedCalibration)
    : McSimulation<MC, RNG, S>(antitheticVariate, controlVariate), process_(std::move(process)),
      timeSteps_(timeSteps), timeStepsPerYear_(timeStepsPerYear), brownianBridge_(brownianBridge),
      requiredSamples_(requiredSamples), requiredTolerance_(requiredTolerance),
      maxSamples_(maxSamples), seed_(seed),
      nCalibrationSamples_((nCalibrationSamples == Null<Size>()) ? 2048 : nCalibrationSamples),
      // NOLINTNEXTLINE(readability-implicit-bool-conversion)
      brownianBridgeCalibration_(brownianBridgeCalibration ? *brownianBridgeCalibration :
                                                             brownianBridge),
      antitheticVariateCalibration_(
          // NOLINTNEXTLINE(readability-implicit-bool-conversion)
          antitheticVariateCalibration ? *antitheticVariateCalibration : antitheticVariate),
      seedCalibration_(seedCalibration != Null<Real>() ? seedCalibration :
                                                         (seed == 0 ? 0 : seed + 1768237423L)) {
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

    template <class Generi
