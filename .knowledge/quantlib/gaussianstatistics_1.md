sianShortfall(Real target) const;

        //! gaussian-assumption Average Shortfall (averaged shortfallness)
        Real gaussianAverageShortfall(Real target) const;
        //@}
    };

    //! default gaussian statistic tool
    typedef GenericGaussianStatistics<GeneralStatistics> GaussianStatistics;


    //! Helper class for precomputed distributions
    class StatsHolder {
      public:
        typedef Real value_type;
        StatsHolder(Real mean,
                    Real standardDeviation)
                    : mean_(mean), standardDeviation_(standardDeviation) {}
        ~StatsHolder() = default;
        Real mean() const { return mean_; }
        Real standardDeviation() const { return standardDeviation_; }
      private:
        Real mean_, standardDeviation_;
    };


    // inline definitions

    template<class Stat>
    inline
    Real GenericGaussianStatistics<Stat>::gaussianRegret(Real target) const {
        Real m = this->mean();
        Real std = this->standardDeviation();
        Real variance = std*std;
        CumulativeNormalDistribution gIntegral(m, std);
        NormalDistribution g(m, std);
        Real firstTerm = variance + m*m - 2.0*target*m + target*target;
        Real alfa = gIntegral(target);
        Real secondTerm = m - target;
        Real beta = variance*g(target);
        Real result = alfa*firstTerm - beta*secondTerm;
        return result/alfa;
    }

    /*! \pre percentile must be in range (0%-100%) extremes excluded */
    template<class Stat>
    inline Real GenericGaussianStatistics<Stat>::gaussianPercentile(
                                                     Real percentile) const {

        QL_REQUIRE(percentile>0.0,
                   "percentile (" << percentile << ") must be > 0.0");
        QL_REQUIRE(percentile<1.0,
                   "percentile (" << percentile << ") must be < 1.0");

        InverseCumulativeNormal gInverse(Stat::mean(),
                                         Stat::standardDeviation());
        return gInverse(percentile);
    }

    /*! \pre percentile must be in range (0%-100%) extremes excluded */
    template<class Stat>
    inline Real GenericGaussianStatistics<Stat>::gaussianTopPercentile(
                                                     Real percentile) const {

        return gaussianPercentile(1.0-percentile);
    }

    /*! \pre percentile must be in range [90%-100%) */
    template<class Stat>
    inline Real GenericGaussianStatistics<Stat>::gaussianPotentialUpside(
                                                    Real percentile) const {

        QL_REQUIRE(percentile<1.0 && percentile>=0.9,
                   "percentile (" << percentile << ") out of range [0.9, 1)");

        Real result = gaussianPercentile(percentile);
        // potential upside must be a gain, i.e., floored at 0.0
        return std::max<Real>(result, 0.0);
    }


    /*! \pre percentile must be in range [90%-100%) */
    template<class Stat>
    inline Real GenericGaussianStatistics<Stat>::gaussianValueAtRisk(
                                                    Real percentile) const {

        QL_REQUIRE(percentile<1.0 && percentile>=0.9,
                   "percentile (" << percentile << ") out of range [0.9, 1)");

        Real result = gaussianPercentile(1.0-percentile);
        // VAR must be a loss
        // this means that it has to be MIN(dist(1.0-percentile), 0.0)
        // VAR must also be a positive quantity, so -MIN(*)
        return -std::min<Real>(result, 0.0);
    }


    /*! \pre percentile must be in range [90%-100%) */
    template<class Stat>
    inline Real GenericGaussianStatistics<Stat>::gaussianExpectedShortfall(
                                                    Real percentile) const {
        QL_REQUIRE(percentile<1.0 && percentile>=0.9,
                   "percentile (" << percentile << ") out of range [0.9, 1)");

        Real m = this->mean();
        Real std = this->standardDeviation();
        InverseCumulativeNormal gIn
