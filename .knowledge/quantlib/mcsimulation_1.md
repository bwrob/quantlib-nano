onteCarloModel<MC,RNG,S> > mcModel_;
        bool antitheticVariate_, controlVariate_;
    };


    // inline definitions
    template <template <class> class MC, class RNG, class S>
    inline typename McSimulation<MC,RNG,S>::result_type
        McSimulation<MC,RNG,S>::value(Real tolerance,
                                              Size maxSamples,
                                              Size minSamples) const {
        Size sampleNumber =
            mcModel_->sampleAccumulator().samples();
        if (sampleNumber<minSamples) {
            mcModel_->addSamples(minSamples-sampleNumber);
            sampleNumber = mcModel_->sampleAccumulator().samples();
        }

        Size nextBatch;
        Real order;
        result_type error(mcModel_->sampleAccumulator().errorEstimate());
        while (maxError(error) > tolerance) {
            QL_REQUIRE(sampleNumber<maxSamples,
                       "max number of samples (" << maxSamples
                       << ") reached, while error (" << error
                       << ") is still above tolerance (" << tolerance << ")");

            // conservative estimate of how many samples are needed
            order = maxError(Real(error*error))/tolerance/tolerance;
            nextBatch =
                Size(std::max<Real>(static_cast<Real>(sampleNumber)*order*0.8 - static_cast<Real>(sampleNumber),
                                    static_cast<Real>(minSamples)));

            // do not exceed maxSamples
            nextBatch = std::min(nextBatch, maxSamples-sampleNumber);
            sampleNumber += nextBatch;
            mcModel_->addSamples(nextBatch);
            error = result_type(mcModel_->sampleAccumulator().errorEstimate());
        }

        return result_type(mcModel_->sampleAccumulator().mean());
    }


    template <template <class> class MC, class RNG, class S>
    inline typename McSimulation<MC,RNG,S>::result_type
        McSimulation<MC,RNG,S>::valueWithSamples(Size samples) const {

        Size sampleNumber = mcModel_->sampleAccumulator().samples();

        QL_REQUIRE(samples>=sampleNumber,
                   "number of already simulated samples (" << sampleNumber
                   << ") greater than requested samples (" << samples << ")");

        mcModel_->addSamples(samples-sampleNumber);

        return result_type(mcModel_->sampleAccumulator().mean());
    }


    template <template <class> class MC, class RNG, class S>
    inline void McSimulation<MC,RNG,S>::calculate(Real requiredTolerance,
                                                  Size requiredSamples,
                                                  Size maxSamples) const {

        QL_REQUIRE(requiredTolerance != Null<Real>() ||
                   requiredSamples != Null<Size>(),
                   "neither tolerance nor number of samples set");

        //! Initialize the one-factor Monte Carlo
        if (this->controlVariate_) {

            result_type controlVariateValue = this->controlVariateValue();
            QL_REQUIRE(controlVariateValue != Null<result_type>(),
                       "engine does not provide "
                       "control-variation price");

            ext::shared_ptr<path_pricer_type> controlPP =
                this->controlPathPricer();
            QL_REQUIRE(controlPP,
                       "engine does not provide "
                       "control-variation path pricer");

            ext::shared_ptr<path_generator_type> controlPG = 
                this->controlPathGenerator();

            this->mcModel_ =
                ext::shared_ptr<MonteCarloModel<MC,RNG,S> >(
                    new MonteCarloModel<MC,RNG,S>(
                           pathGenerator(), this->pathPricer(), stats_type(),
                           this->antitheticVariate_, controlPP,
                           controlVariateValue, controlPG));
        } else {
            this->mcModel_ =
                ext::shared_ptr<MonteCarloModel<MC,RNG,S> >(
                  