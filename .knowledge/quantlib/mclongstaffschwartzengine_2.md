cEngine, template <class> class MC, class RNG,
              class S, class RNG_Calibration>
    inline ext::shared_ptr<typename MCLongstaffSchwartzEngine<
        GenericEngine, MC, RNG, S, RNG_Calibration>::path_pricer_type>
    MCLongstaffSchwartzEngine<GenericEngine, MC, RNG, S,
                              RNG_Calibration>::pathPricer() const {

        QL_REQUIRE(pathPricer_, "path pricer unknown");
        return pathPricer_;
    }

    template <class GenericEngine, template <class> class MC, class RNG,
              class S, class RNG_Calibration>
    inline void MCLongstaffSchwartzEngine<GenericEngine, MC, RNG, S,
                                          RNG_Calibration>::calculate() const {
        // calibration
        pathPricer_ = this->lsmPathPricer();
        Size dimensions = process_->factors();
        TimeGrid grid = this->timeGrid();
        typename RNG_Calibration::rsg_type generator =
            RNG_Calibration::make_sequence_generator(
                dimensions * (grid.size() - 1), seedCalibration_);
        ext::shared_ptr<path_generator_type_calibration>
            pathGeneratorCalibration =
                ext::make_shared<path_generator_type_calibration>(
                    process_, grid, generator, brownianBridgeCalibration_);
        mcModelCalibration_ =
            ext::shared_ptr<MonteCarloModel<MC, RNG_Calibration, S> >(
                new MonteCarloModel<MC, RNG_Calibration, S>(
                    pathGeneratorCalibration, pathPricer_, stats_type(),
                    this->antitheticVariateCalibration_));

        mcModelCalibration_->addSamples(nCalibrationSamples_);
        pathPricer_->calibrate();
        // pricing
        McSimulation<MC,RNG,S>::calculate(requiredTolerance_,
                                          requiredSamples_,
                                          maxSamples_);
        this->results_.value = this->mcModel_->sampleAccumulator().mean();
        this->results_.additionalResults["exerciseProbability"] =
            this->pathPricer_->exerciseProbability();
        if constexpr (RNG::allowsErrorEstimate) {
            this->results_.errorEstimate =
                this->mcModel_->sampleAccumulator().errorEstimate();
        }
    }

    template <class GenericEngine, template <class> class MC, class RNG,
              class S, class RNG_Calibration>
    inline TimeGrid
    MCLongstaffSchwartzEngine<GenericEngine, MC, RNG, S,
                              RNG_Calibration>::timeGrid() const {
        std::vector<Time> requiredTimes;
        if (this->arguments_.exercise->type() == Exercise::American) {
            Date lastExerciseDate = this->arguments_.exercise->lastDate();
            requiredTimes.push_back(process_->time(lastExerciseDate));
        } else {
            for (Size i = 0; i < this->arguments_.exercise->dates().size();
                 ++i) {
                Time t = process_->time(this->arguments_.exercise->date(i));
                if (t > 0.0)
                    requiredTimes.push_back(t);
            }
        }
        if (this->timeSteps_ != Null<Size>()) {
            return TimeGrid(requiredTimes.begin(), requiredTimes.end(),
                            this->timeSteps_);
        } else if (this->timeStepsPerYear_ != Null<Size>()) {
            Size steps = static_cast<Size>(this->timeStepsPerYear_ *
                                           requiredTimes.back());
            return TimeGrid(requiredTimes.begin(), requiredTimes.end(),
                            std::max<Size>(steps, 1));
        } else {
            QL_FAIL("time steps not specified");
        }
    }

    template <class GenericEngine, template <class> class MC, class RNG,
              class S, class RNG_Calibration>
    inline ext::shared_ptr<typename MCLongstaffSchwartzEngine<
        GenericEngine, MC, RNG, S, RNG_Calibration>::path_generator_type>
    MCLongstaffSchwartzEngine<GenericEngine, MC, RNG, S,
                              RNG_Calibration>::p
