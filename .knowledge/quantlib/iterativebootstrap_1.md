er error.
        */
        IterativeBootstrap(Real accuracy = Null<Real>(),
                           Real minValue = Null<Real>(),
                           Real maxValue = Null<Real>(),
                           Size maxAttempts = 1,
                           Real maxFactor = 2.0,
                           Real minFactor = 2.0,
                           bool dontThrow = false,
                           Size dontThrowSteps = 10,
                           Size maxEvaluations = MAX_FUNCTION_EVALUATIONS);
        void setup(Curve* ts);
        void calculate() const;
      private:
        void initialize() const;
        Real accuracy_;
        Real minValue_, maxValue_;
        Size maxAttempts_;
        Real maxFactor_;
        Real minFactor_;
        bool dontThrow_;
        Size dontThrowSteps_;
        Curve* ts_;
        Size n_ = 0;
        Brent firstSolver_;
        FiniteDifferenceNewtonSafe solver_;
        mutable bool initialized_ = false, validCurve_ = false, loopRequired_;
        mutable Size firstAliveHelper_ = 0, alive_ = 0;
    };


    // template definitions

    template <class Curve>
    IterativeBootstrap<Curve>::IterativeBootstrap(Real accuracy,
                                                  Real minValue,
                                                  Real maxValue,
                                                  Size maxAttempts,
                                                  Real maxFactor,
                                                  Real minFactor,
                                                  bool dontThrow,
                                                  Size dontThrowSteps,
                                                  Size maxEvaluations)
    : accuracy_(accuracy), minValue_(minValue), maxValue_(maxValue), maxAttempts_(maxAttempts),
      maxFactor_(maxFactor), minFactor_(minFactor), dontThrow_(dontThrow),
      dontThrowSteps_(dontThrowSteps), ts_(nullptr), loopRequired_(Interpolator::global) {
        QL_REQUIRE(maxFactor_ >= 1.0, "Expected that maxFactor would be at least 1.0 but got " << maxFactor_);
        QL_REQUIRE(minFactor_ >= 1.0, "Expected that minFactor would be at least 1.0 but got " << minFactor_);
        firstSolver_.setMaxEvaluations(maxEvaluations);
        solver_.setMaxEvaluations(maxEvaluations);
    }

    template <class Curve>
    void IterativeBootstrap<Curve>::setup(Curve* ts) {
        ts_ = ts;
        n_ = ts_->instruments_.size();
        QL_REQUIRE(n_ > 0, "no bootstrap helpers given");
        for (Size j=0; j<n_; ++j)
            ts_->registerWithObservables(ts_->instruments_[j]);

        // do not initialize yet: instruments could be invalid here
        // but valid later when bootstrapping is actually required
    }

    template <class Curve>
    void IterativeBootstrap<Curve>::initialize() const {
        // ensure helpers are sorted
        std::sort(ts_->instruments_.begin(), ts_->instruments_.end(),
                  detail::BootstrapHelperSorter());
        // skip expired helpers
        Date firstDate = Traits::initialDate(ts_);
        QL_REQUIRE(ts_->instruments_[n_-1]->pillarDate()>firstDate,
                   "all instruments expired");
        firstAliveHelper_ = 0;
        while (ts_->instruments_[firstAliveHelper_]->pillarDate() <= firstDate)
            ++firstAliveHelper_;
        alive_ = n_-firstAliveHelper_;
        Size nodes = alive_+1;
        QL_REQUIRE(nodes >= Interpolator::requiredPoints,
                   "not enough alive instruments: " << alive_ <<
                   " provided, " << Interpolator::requiredPoints-1 <<
                   " required");

        // calculate dates and times
        std::vector<Date>& dates = ts_->dates_;
        std::vector<Time>& times = ts_->times_;
        dates.resize(alive_+1);
        times.resize(alive_+1);
        dates[0] = firstDate;
        times[0] = ts_->timeFromReference(dates[0]);

        Date maxDate = firstDate;
        // pillar counter: i
 