CarloModel<MC,RNG,S>::addSamples(Size samples) {
        for(Size j = 1; j <= samples; j++) {

            const sample_type& path = pathGenerator_->next();
            result_type price = (*pathPricer_)(path.value);

            if (isControlVariate_) {
                if (!cvPathGenerator_) {
                    price += cvOptionValue_-(*cvPathPricer_)(path.value);
                }
                else {
                    const sample_type& cvPath = cvPathGenerator_->next();
                    price += cvOptionValue_-(*cvPathPricer_)(cvPath.value);
                }
            }

            if (isAntitheticVariate_) {
                const sample_type& atPath = pathGenerator_->antithetic();
                result_type price2 = (*pathPricer_)(atPath.value);
                if (isControlVariate_) {
                    if (!cvPathGenerator_)
                        price2 += cvOptionValue_-(*cvPathPricer_)(atPath.value);
                    else {
                        const sample_type& cvPath = cvPathGenerator_->antithetic();
                        price2 += cvOptionValue_-(*cvPathPricer_)(cvPath.value);
                    }
                }

                sampleAccumulator_.add((price+price2)/2.0, path.weight);
            } else {
                sampleAccumulator_.add(price, path.weight);
            }
        }
    }

    template <template <class> class MC, class RNG, class S>
    inline const typename MonteCarloModel<MC,RNG,S>::stats_type&
    MonteCarloModel<MC,RNG,S>::sampleAccumulator() const {
        return sampleAccumulator_;
    }

}


#endif
