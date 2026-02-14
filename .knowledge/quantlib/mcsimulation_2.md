  new MonteCarloModel<MC,RNG,S>(
                           pathGenerator(), this->pathPricer(), S(),
                           this->antitheticVariate_));
        }

        if (requiredTolerance != Null<Real>()) {
            if (maxSamples != Null<Size>())
                this->value(requiredTolerance, maxSamples);
            else
                this->value(requiredTolerance);
        } else {
            this->valueWithSamples(requiredSamples);
        }

    }

    template <template <class> class MC, class RNG, class S>
    inline typename McSimulation<MC,RNG,S>::result_type
        McSimulation<MC,RNG,S>::errorEstimate() const {
        return mcModel_->sampleAccumulator().errorEstimate();
    }

    template <template <class> class MC, class RNG, class S>
    inline const typename McSimulation<MC,RNG,S>::stats_type&
    McSimulation<MC,RNG,S>::sampleAccumulator() const {
        return mcModel_->sampleAccumulator();
    }

}


#endif
