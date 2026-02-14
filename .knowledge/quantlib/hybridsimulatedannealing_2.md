l == reAnnealSteps_) {
                kReAnneal = 0;
                reannealing_(annealStep, currentPoint, currentValue, currentTemperature);
            }
            kReAnneal++;

            //Reset if necessary
            if (kReset == resetSteps_) {
                kReset = 0;
                switch (resetScheme_) {
                case NoResetScheme:
                    break;
                case ResetToOrigin:
                    currentPoint = startingPoint;
                    currentValue = startingValue;
                    break;
                case ResetToBestPoint:
                    currentPoint = bestPoint;
                    currentValue = bestValue;
                    break;
                }
            }
            kReset++;

            //Update the current temperature according to current step
            temperature_(currentTemperature, currentTemperature, annealStep);

            //Check if temperature condition is breached
            for (Size i = 0; i < n; i++)
                temperatureBreached = temperatureBreached && currentTemperature[i] < endTemperature_;
        }

        //Change end criteria type if appropriate
        if (k > maxK)
            ecType = EndCriteria::MaxIterations;
        else if (kStationary > maxKStationary)
            ecType = EndCriteria::StationaryPoint;

        //Set result to best point
        P.setCurrentValue(bestPoint);
        P.setFunctionValue(bestValue);
        return ecType;
    }

    typedef HybridSimulatedAnnealing<SamplerGaussian, ProbabilityBoltzmannDownhill, TemperatureExponential, ReannealingTrivial> GaussianSimulatedAnnealing;
    typedef HybridSimulatedAnnealing<SamplerLogNormal, ProbabilityBoltzmannDownhill, TemperatureExponential, ReannealingTrivial> LogNormalSimulatedAnnealing;
    typedef HybridSimulatedAnnealing<SamplerMirrorGaussian, ProbabilityBoltzmannDownhill, TemperatureExponential, ReannealingTrivial> MirrorGaussianSimulatedAnnealing;
    typedef HybridSimulatedAnnealing<SamplerGaussian, ProbabilityBoltzmannDownhill, TemperatureExponential, ReannealingFiniteDifferences> GaussianSimulatedReAnnealing;
    typedef HybridSimulatedAnnealing<SamplerVeryFastAnnealing, ProbabilityBoltzmannDownhill, TemperatureVeryFastAnnealing, ReannealingTrivial> VeryFastSimulatedAnnealing;
    typedef HybridSimulatedAnnealing<SamplerVeryFastAnnealing, ProbabilityBoltzmannDownhill, TemperatureVeryFastAnnealing, ReannealingFiniteDifferences> VeryFastSimulatedReAnnealing;
}

#endif
