  // skip expired additional dates
    std::vector<Date> additionalDates;
    if (additionalDates_)
        additionalDates = additionalDates_();
    if (!additionalDates.empty()) {
        additionalDates.erase(
            std::remove_if(additionalDates.begin(), additionalDates.end(),
                           [=](const Date& date) { return date <= firstDate; }),
            additionalDates.end()
        );
    }

    // calculate dates and times
    std::vector<Date> &dates = ts_->dates_;
    std::vector<Time> &times = ts_->times_;

    // first populate the dates vector and make sure they are sorted and unique
    dates.clear();
    dates.push_back(firstDate);
    std::transform(
        aliveInstruments_.begin(), aliveInstruments_.end(), std::back_inserter(dates),
        [](const ext::shared_ptr<typename Traits::helper>& h) { return h->pillarDate(); });
    dates.insert(dates.end(), additionalDates.begin(), additionalDates.end());
    std::sort(dates.begin(), dates.end());
    dates.erase(std::unique(dates.begin(), dates.end()), dates.end());

    // check if there are enough interpolation points
    QL_REQUIRE(dates.size() >= Interpolator::requiredPoints,
               "GlobalBootstrap: not enough curve points ("
                   << dates.size() << ") for interpolation requiring at least "
                   << Interpolator::requiredPoints);

    // build times vector
    times.clear();
    std::transform(dates.begin(), dates.end(), std::back_inserter(times),
                   [this](const Date& d) { return ts_->timeFromReference(d); });

    // determine maxDate ensuring all instruments and additional helpers are covered
    ts_->maxDate_ = dates.back();
    for (auto const& h : aliveInstruments_)
        ts_->maxDate_ = std::max(ts_->maxDate_, h->latestRelevantDate());
    for (auto const& h : aliveAdditionalHelpers_)
        ts_->maxDate_ = std::max(ts_->maxDate_, h->latestRelevantDate());

    // set initial guess only if the current curve cannot be used as guess
    if (!validCurve_ || ts_->data_.size() != dates.size()) {
        // ts_->data_[0] is the only relevant item,
        // but reasonable numbers might be needed for the whole data vector
        // because, e.g., of interpolation's early checks
        ts_->data_ = std::vector<Real>(dates.size(), Traits::initialValue(ts_));
        validCurve_ = false;
    }
    initialized_ = true;
}

template <class Curve> Array GlobalBootstrap<Curve>::setupCostFunction() const {

    // for single-curve boostrap, this was done in LazyObject::calculate() already, but for
    // multi-curve boostrap we have to do this manually for all contributing curves except
    // the main one, because calculate() is never triggered for them
    ts_->setCalculated(true);

    // we might have to call initialize even if the curve is initialized
    // and not moving, just because helpers might be date relative and change
    // with evaluation date change.
    // anyway it makes little sense to use date relative helpers with a
    // non-moving curve if the evaluation date changes
    if (!initialized_ || ts_->moving_)
        initialize();

    // setup helpers
    for (auto const& helper : aliveInstruments_) {
        // check for valid quote
        QL_REQUIRE(helper->quote()->isValid(),
                   "instrument (maturity: " << helper->maturityDate() << ", pillar: "
                                            << helper->pillarDate() << ") has an invalid quote");
        // don't try this at home!
        // This call creates helpers, and removes "const".
        // There is a significant interaction with observability.
        helper->setTermStructure(const_cast<Curve*>(ts_));
    }

    // setup additional helpers
    for (auto const& helper : aliveAdditionalHelpers_) {
        QL_REQUIRE(helper->quote()->isValid(),
                   "additional instrument (maturity: " << helper->maturityDate()
                                                       << ") has an invalid
