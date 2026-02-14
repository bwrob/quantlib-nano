   ext::make_shared<LevenbergMarquardt>(),
                                 LocalOptimizeScheme optimizeScheme = EveryBestPoint)
        : sampler_(sampler), probability_(probability), temperature_(std::move(temperature)),
          reannealing_(reannealing), startTemperature_(startTemperature),
          endTemperature_(endTemperature),
          reAnnealSteps_(reAnnealSteps == 0 ? QL_MAX_INTEGER : reAnnealSteps),
          resetScheme_(resetScheme), resetSteps_(resetSteps == 0 ? QL_MAX_INTEGER : resetSteps),
          localOptimizer_(localOptimizer),
          optimizeScheme_(localOptimizer != nullptr ? optimizeScheme : NoLocalOptimize) {}

        EndCriteria::Type minimize(Problem& P, const EndCriteria& endCriteria) override;

      private:
        Sampler sampler_;
        Probability probability_;
        Temperature temperature_;
        Reannealing reannealing_;
        Real startTemperature_;
        Real endTemperature_;
        Size reAnnealSteps_;
        ResetScheme resetScheme_;
        Size resetSteps_;
        ext::shared_ptr<OptimizationMethod> localOptimizer_;
        LocalOptimizeScheme optimizeScheme_;
    };

    template <class Sampler, class Probability, class Temperature, class Reannealing>
    EndCriteria::Type HybridSimulatedAnnealing<Sampler, Probability, Temperature, Reannealing>::minimize(Problem &P, const EndCriteria &endCriteria) {
        EndCriteria::Type ecType = EndCriteria::None;
        P.reset();
        reannealing_.setProblem(P);
        Array x = P.currentValue();
        Size n = x.size();
        Size k = 1;
        Size kStationary = 1;
        Size kReAnneal = 1;
        Size kReset = 1;
        Size maxK = endCriteria.maxIterations();
        Size maxKStationary = endCriteria.maxStationaryStateIterations();
        bool temperatureBreached = false;
        Array currentTemperature(n, startTemperature_);
        Array annealStep(n, 1.0);
        Array bestPoint(x);
        Array currentPoint(x);
        const Array& startingPoint(x);
        Array newPoint(x);
        Real bestValue = P.value(bestPoint);
        Real currentValue = bestValue;
        Real startingValue = bestValue; //to reset to starting point if desired
        while (k <= maxK && kStationary <= maxKStationary && !temperatureBreached)
        {
            //Draw a new sample point
            sampler_(newPoint, currentPoint, currentTemperature);
            try{
                //Evaluate new point
                Real newValue = P.value(newPoint);
				
                //Determine if new point is accepted
                if (probability_(currentValue, newValue, currentTemperature)) {
                    if (optimizeScheme_ == EveryNewPoint) {
                        P.setCurrentValue(newPoint);
                        P.setFunctionValue(newValue);
                        localOptimizer_->minimize(P, endCriteria);
                        newPoint = P.currentValue();
                        newValue = P.functionValue();
                    }
                    currentPoint = newPoint;
                    currentValue = newValue;
                }

                //Check if we have a new best point
                if (newValue < bestValue) {
                    if (optimizeScheme_ == EveryBestPoint) {
                        P.setCurrentValue(newPoint);
                        P.setFunctionValue(newValue);
                        localOptimizer_->minimize(P, endCriteria);
                        newPoint = P.currentValue();
                        newValue = P.functionValue();
                    }
                    kStationary = 0;
                    bestValue = newValue;
                    bestPoint = newPoint;
                }
            } catch(...){
                //Do nothing, move on to new draw
            }
            //Increase steps
            k++;
            kStationary++;
            for (Real& i : annealStep)
                i++;

            //Reanneal if necessary
            if (kReAnnea