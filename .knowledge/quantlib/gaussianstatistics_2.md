verse(m, std);
        Real var = gInverse(1.0-percentile);
        NormalDistribution g(m, std);
        Real result = m - std*std*g(var)/(1.0-percentile);
        // expectedShortfall must be a loss
        // this means that it has to be MIN(result, 0.0)
        // expectedShortfall must also be a positive quantity, so -MIN(*)
        return -std::min<Real>(result, 0.0);
    }


    template<class Stat>
    inline Real GenericGaussianStatistics<Stat>::gaussianShortfall(
                                                        Real target) const {
        CumulativeNormalDistribution gIntegral(this->mean(),
                                               this->standardDeviation());
        return gIntegral(target);
    }


    template<class Stat>
    inline Real GenericGaussianStatistics<Stat>::gaussianAverageShortfall(
                                                        Real target) const {
        Real m = this->mean();
        Real std = this->standardDeviation();
        CumulativeNormalDistribution gIntegral(m, std);
        NormalDistribution g(m, std);
        return ( (target-m) + std*std*g(target)/gIntegral(target) );
    }

}


#endif