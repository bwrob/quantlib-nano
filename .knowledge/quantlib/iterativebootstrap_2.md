       // helper counter: j
        for (Size i=1, j=firstAliveHelper_; j<n_; ++i, ++j) {
            const auto& helper = ts_->instruments_[j];
            dates[i] = helper->pillarDate();
            times[i] = ts_->timeFromReference(dates[i]);
            // check for duplicated pillars
            QL_REQUIRE(dates[i-1]!=dates[i],
                       "more than one instrument with pillar " << dates[i]);

            Date latestRelevantDate = helper->latestRelevantDate();
            // check that the helper is really extending the curve, i.e. that
            // pillar-sorted helpers are also sorted by latestRelevantDate
            QL_REQUIRE(latestRelevantDate > maxDate,
                       io::ordinal(j+1) << " instrument (pillar: " <<
                       dates[i] << ") has latestRelevantDate (" <<
                       latestRelevantDate << ") before or equal to "
                       "previous instrument's latestRelevantDate (" <<
                       maxDate << ")");
            maxDate = std::max(dates[i], latestRelevantDate);

            // when a pillar date is before the last relevant date the
            // convergence loop is required even if the Interpolator is local
            if (dates[i] < latestRelevantDate)
                loopRequired_ = true;
        }
        ts_->maxDate_ = maxDate;

        // set initial guess only if the current curve cannot be used as guess
        if (!validCurve_ || ts_->data_.size()!=alive_+1) {
            // ts_->data_[0] is the only relevant item,
            // but reasonable numbers might be needed for the whole data vector
            // because, e.g., of interpolation's early checks
            ts_->data_ = std::vector<Real>(alive_+1, Traits::initialValue(ts_));
            validCurve_ = false;
        }
        initialized_ = true;
    }

    template <class Curve>
    void IterativeBootstrap<Curve>::calculate() const {

        // we might have to call initialize even if the curve is initialized
        // and not moving, just because helpers might be date relative and change
        // with evaluation date change.
        // anyway it makes little sense to use date relative helpers with a
        // non-moving curve if the evaluation date changes
        if (!initialized_ || ts_->moving_)
            initialize();

        // setup helpers
        for (Size j=firstAliveHelper_; j<n_; ++j) {
            const auto& helper = ts_->instruments_[j];
            // check for valid quote
            QL_REQUIRE(helper->quote()->isValid(),
                       io::ordinal(j + 1) << " instrument (maturity: " <<
                       helper->maturityDate() << ", pillar: " <<
                       helper->pillarDate() << ") has an invalid quote");
            // don't try this at home!
            // This call creates helpers, and removes "const".
            // There is a significant interaction with observability.
            helper->setTermStructure(const_cast<Curve*>(ts_));
        }

        const std::vector<Time>& times = ts_->times_;
        const std::vector<Real>& data = ts_->data_;
        Real accuracy = accuracy_ != Null<Real>() ? accuracy_ : ts_->accuracy_;

        Size maxIterations = Traits::maxIterations()-1;

        // there might be a valid curve state to use as guess
        bool validData = validCurve_;
        std::vector<Real> previousData;

        for (Size iteration=0; ; ++iteration) {
            if (loopRequired_ && validData)
                previousData = ts_->data_;

            // Store min value and max value at each pillar so that we can expand search if necessary.
            std::vector<Real> minValues(alive_+1, Null<Real>());
            std::vector<Real> maxValues(alive_+1, Null<Real>());
            std::vector<Size> attempts(alive_+1, 1);

            for (Size i=1, j=firstAliveHelper_; j<n_; ++i, ++j) { // pillar loop

                // shorter aliases for readability and to avoid duplication
                Real& min