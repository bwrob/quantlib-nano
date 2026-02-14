ector<Real> expectedShortfall(Real percentile) const;

        std::vector<Real> regret(Real target) const;

        std::vector<Real> gaussianShortfall(Real target) const;
        std::vector<Real> shortfall(Real target) const;

        std::vector<Real> gaussianAverageShortfall(Real target) const;
        std::vector<Real> averageShortfall(Real target) const;

        //@}
        //! \name Modifiers
        //@{
        void reset(Size dimension = 0);
        template <class Sequence>
        void add(const Sequence& sample,
                 Real weight = 1.0) {
            add(sample.begin(), sample.end(), weight);
        }
        template <class Iterator>
        void add(Iterator begin,
                 Iterator end,
                 Real weight = 1.0) {
            if (dimension_ == 0) {
                // stat wasn't initialized yet
                QL_REQUIRE(end>begin, "sample error: end<=begin");
                Size dimension = std::distance(begin, end);
                reset(dimension);
            }

            QL_REQUIRE(std::distance(begin, end) == Integer(dimension_),
                       "sample size mismatch: " << dimension_ <<
                       " required, " << std::distance(begin, end) <<
                       " provided");

            quadraticSum_ += weight * outerProduct(begin, end,
                                                   begin, end);

            for (Size i=0; i<dimension_; ++begin, ++i)
                stats_[i].add(*begin, weight);

        }
        //@}
      protected:
        Size dimension_ = 0;
        std::vector<statistics_type> stats_;
        mutable std::vector<Real> results_;
        Matrix quadraticSum_;
    };

    //! default multi-dimensional statistics tool
    /*! \test the correctness of the returned values is tested by
              checking them against numerical calculations.
    */
    typedef GenericSequenceStatistics<Statistics> SequenceStatistics;
    typedef GenericSequenceStatistics<IncrementalStatistics> SequenceStatisticsInc;

    // inline definitions

    template <class Stat>
    inline GenericSequenceStatistics<Stat>::GenericSequenceStatistics(Size dimension) {
        reset(dimension);
    }

    template <class Stat>
    inline Size GenericSequenceStatistics<Stat>::samples() const {
        return (stats_.empty()) ? 0 : stats_[0].samples();
    }

    template <class Stat>
    inline Real GenericSequenceStatistics<Stat>::weightSum() const {
        return (stats_.empty()) ? 0.0 : stats_[0].weightSum();
    }


    // macros for the implementation of the lifted methods

    // N-D methods' definition with void argument list
    #define DEFINE_SEQUENCE_STAT_CONST_METHOD_VOID(METHOD) \
    template <class Stat> \
    std::vector<Real> \
    GenericSequenceStatistics<Stat>::METHOD() const { \
        for (Size i=0; i<dimension_; i++) \
            results_[i] = stats_[i].METHOD(); \
        return results_; \
    }
    DEFINE_SEQUENCE_STAT_CONST_METHOD_VOID(mean)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_VOID(variance)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_VOID(standardDeviation)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_VOID(downsideVariance)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_VOID(downsideDeviation)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_VOID(semiVariance)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_VOID(semiDeviation)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_VOID(errorEstimate)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_VOID(skewness)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_VOID(kurtosis)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_VOID(min)
    DEFINE_SEQUENCE_STAT_CONST_METHOD_VOID(max)
    #undef DEFINE_SEQUENCE_STAT_CONST_METHOD_VOID


    // N-D methods' definition with single argument
    #define DEFINE_SEQUENCE_STAT_CONST_METHOD_DOUBLE(METHOD) \
    template <class Stat> \
    std::vector<Real> \
    GenericSequenceStatistics<Stat>::METHOD(Real x) const { \
        for (Size i=0; i<dimension_; i++) \
            results_[i] = stats_[i].METHOD(x); \
        return
