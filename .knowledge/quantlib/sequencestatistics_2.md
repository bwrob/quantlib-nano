results_; \
    }

    DEFINE_SEQUENCE_STAT_CONST_METHOD_DOUBLE(gaussianPercentile)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_DOUBLE(gaussianPotentialUpside)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_DOUBLE(gaussianValueAtRisk)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_DOUBLE(gaussianExpectedShortfall)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_DOUBLE(gaussianShortfall)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_DOUBLE(gaussianAverageShortfall)

    DEFINE_SEQUENCE_STAT_CONST_METHOD_DOUBLE(percentile)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_DOUBLE(potentialUpside)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_DOUBLE(valueAtRisk)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_DOUBLE(expectedShortfall)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_DOUBLE(regret)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_DOUBLE(shortfall)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_DOUBLE(averageShortfall)
    #undef DEFINE_SEQUENCE_STAT_CONST_METHOD_DOUBLE


    template <class Stat>
    void GenericSequenceStatistics<Stat>::reset(Size dimension) {
        // (re-)initialize
        if (dimension > 0) {
            if (dimension == dimension_) {
                for (Size i=0; i<dimension_; ++i)
                    stats_[i].reset();
            } else {
                dimension_ = dimension;
                stats_ = std::vector<Stat>(dimension);
                results_ = std::vector<Real>(dimension);
            }
            quadraticSum_ = Matrix(dimension_, dimension_, 0.0);
        } else {
            dimension_ = dimension;
        }
    }

    template <class Stat>
    Matrix GenericSequenceStatistics<Stat>::covariance() const {
        Real sampleWeight = weightSum();
        QL_REQUIRE(sampleWeight > 0.0,
                   "sampleWeight=0, unsufficient");

        Real sampleNumber = static_cast<Real>(samples());
        QL_REQUIRE(sampleNumber > 1.0,
                   "sample number <=1, unsufficient");

        std::vector<Real> m = mean();
        Real inv = 1.0/sampleWeight;

        Matrix result = inv*quadraticSum_;
        result -= outerProduct(m.begin(), m.end(),
                               m.begin(), m.end());

        result *= (sampleNumber/(sampleNumber-1.0));
        return result;
    }


    template <class Stat>
    Matrix GenericSequenceStatistics<Stat>::correlation() const {
        Matrix correlation = covariance();
        Array variances = correlation.diagonal();
        for (Size i=0; i<dimension_; i++){
            for (Size j=0; j<dimension_; j++){
                if (i==j) {
                    if (variances[i]==0.0) {
                        correlation[i][j] = 1.0;
                    } else {
                        correlation[i][j] *=
                            1.0/std::sqrt(variances[i]*variances[j]);
                    }
                } else {
                    if (variances[i]==0.0 && variances[j]==0) {
                        correlation[i][j] = 1.0;
                    } else if (variances[i]==0.0 || variances[j]==0.0) {
                        correlation[i][j] = 0.0;
                    } else {
                        correlation[i][j] *=
                            1.0/std::sqrt(variances[i]*variances[j]);
                    }
                }
            } // j for
        } // i for

        return correlation;
    }

}


#endif
