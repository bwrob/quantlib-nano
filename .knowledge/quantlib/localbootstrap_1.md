ate definitions

    template <class Curve>
    LocalBootstrap<Curve>::LocalBootstrap(Size localisation, bool forcePositive, Real accuracy)
    : ts_(nullptr), localisation_(localisation), forcePositive_(forcePositive),
      accuracy_(accuracy) {}

    template <class Curve>
    void LocalBootstrap<Curve>::setup(Curve* ts) {

        ts_ = ts;

        Size n = ts_->instruments_.size();
        QL_REQUIRE(n >= Interpolator::requiredPoints,
                   "not enough instruments: " << n << " provided, " <<
                   Interpolator::requiredPoints << " required");

        QL_REQUIRE(n > localisation_,
                   "not enough instruments: " << n << " provided, " <<
                   localisation_ << " required.");

        for (Size i=0; i<n; ++i){
            ts_->registerWithObservables(ts_->instruments_[i]);
        }
    }

    template <class Curve>
    void LocalBootstrap<Curve>::calculate() const {

        validCurve_ = false;
        Size nInsts = ts_->instruments_.size();

        // ensure rate helpers are sorted
        std::sort(ts_->instruments_.begin(), ts_->instruments_.end(),
                  detail::BootstrapHelperSorter());

        // check that there is no instruments with the same maturity
        for (Size i=1; i<nInsts; ++i) {
            Date m1 = ts_->instruments_[i-1]->pillarDate(),
                 m2 = ts_->instruments_[i]->pillarDate();
            QL_REQUIRE(m1 != m2,
                       "two instruments have the same pillar date ("<<m1<<")");
        }

        // check that there is no instruments with invalid quote
        for (Size i=0; i<nInsts; ++i)
            QL_REQUIRE(ts_->instruments_[i]->quote()->isValid(),
                       io::ordinal(i+1) << " instrument (maturity: " <<
                       ts_->instruments_[i]->maturityDate() << ", pillar: " <<
                       ts_->instruments_[i]->pillarDate() <<
                       ") has an invalid quote");

        // setup instruments
        for (Size i=0; i<nInsts; ++i) {
            // don't try this at home!
            // This call creates instruments, and removes "const".
            // There is a significant interaction with observability.
            ts_->instruments_[i]->setTermStructure(const_cast<Curve*>(ts_));
        }
        // set initial guess only if the current curve cannot be used as guess
        if (validCurve_)
            QL_ENSURE(ts_->data_.size() == nInsts+1,
                      "dimension mismatch: expected " << nInsts+1 <<
                      ", actual " << ts_->data_.size());
        else {
            ts_->data_ = std::vector<Rate>(nInsts+1);
            ts_->data_[0] = Traits::initialValue(ts_);
        }

        // calculate dates and times
        ts_->dates_ = std::vector<Date>(nInsts+1);
        ts_->times_ = std::vector<Time>(nInsts+1);
        ts_->dates_[0] = Traits::initialDate(ts_);
        ts_->times_[0] = ts_->timeFromReference(ts_->dates_[0]);
        for (Size i=0; i<nInsts; ++i) {
            ts_->dates_[i+1] = ts_->instruments_[i]->pillarDate();
            ts_->times_[i+1] = ts_->timeFromReference(ts_->dates_[i+1]);
            if (!validCurve_)
                ts_->data_[i+1] = ts_->data_[i];
        }

        Real accuracy = accuracy_ != Null<Real>() ? accuracy_ : ts_->accuracy_;

        LevenbergMarquardt solver(accuracy,
                                  accuracy,
                                  accuracy);
        EndCriteria endCriteria(100, 10, 0.00, accuracy, 0.00);
        PositiveConstraint posConstraint;
        NoConstraint noConstraint;
        Constraint& solverConstraint = forcePositive_ ?
            static_cast<Constraint&>(posConstraint) :
            static_cast<Constraint&>(noConstraint);

        // now start the bootstrapping.
        Size iInst = localisation_-1;

        Size dataAdjust = Curve::interpolator_type::dataSizeAdjustment;

        do {
            Size initialDataPt = iInst+1-localisation_+dataAdjust;
            