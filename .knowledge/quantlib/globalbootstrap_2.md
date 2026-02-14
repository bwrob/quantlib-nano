ditionalPenalties,
    Real accuracy,
    ext::shared_ptr<OptimizationMethod> optimizer,
    ext::shared_ptr<EndCriteria> endCriteria,
    ext::shared_ptr<AdditionalBootstrapVariables> additionalVariables,
    std::vector<Real> instrumentWeights)
: ts_(nullptr), accuracy_(accuracy), optimizer_(std::move(optimizer)),
  endCriteria_(std::move(endCriteria)), additionalHelpers_(std::move(additionalHelpers)),
  additionalDates_(std::move(additionalDates)),
  additionalPenalties_(std::move(additionalPenalties)),
  additionalVariables_(std::move(additionalVariables)),
  instrumentWeights_(std::move(instrumentWeights)) {}

template <class Curve>
GlobalBootstrap<Curve>::GlobalBootstrap(
    std::vector<ext::shared_ptr<typename Traits::helper>> additionalHelpers,
    std::function<std::vector<Date>()> additionalDates,
    std::function<Array()> additionalPenalties,
    Real accuracy,
    ext::shared_ptr<OptimizationMethod> optimizer,
    ext::shared_ptr<EndCriteria> endCriteria,
    ext::shared_ptr<AdditionalBootstrapVariables> additionalVariables,
    std::vector<Real> instrumentWeights)
: GlobalBootstrap(std::move(additionalHelpers),
                  std::move(additionalDates),
                  additionalPenalties ?
                      [f = std::move(additionalPenalties)](
                          const std::vector<Time>&, const std::vector<Real>&) { return f(); } :
                      AdditionalPenalties(),
                  accuracy,
                  std::move(optimizer),
                  std::move(endCriteria),
                  std::move(additionalVariables),
                  std::move(instrumentWeights)) {}

template <class Curve>
void GlobalBootstrap<Curve>::setParentBootstrapper(const ext::shared_ptr<MultiCurveBootstrap>& b) const {
    parentBootstrapper_ = b;
}

template <class Curve> void GlobalBootstrap<Curve>::setToValid() const { validCurve_ = true; }

template <class Curve> void GlobalBootstrap<Curve>::setup(Curve* ts) {
    ts_ = ts;
    for (Size j = 0; j < ts_->instruments_.size(); ++j)
        ts_->registerWithObservables(ts_->instruments_[j]);
    for (Size j = 0; j < additionalHelpers_.size(); ++j)
        ts_->registerWithObservables(additionalHelpers_[j]);

    // setup optimizer and EndCriteria
    Real accuracy = accuracy_ != Null<Real>() ? accuracy_ : ts_->accuracy_;
    if (!optimizer_) {
        optimizer_ = ext::make_shared<LevenbergMarquardt>(accuracy, accuracy, accuracy);
    }
    if (!endCriteria_) {
        endCriteria_ = ext::make_shared<EndCriteria>(1000, 10, accuracy, accuracy, accuracy);
    }

    // check number of instrument weights
    QL_REQUIRE(instrumentWeights_.empty() || instrumentWeights_.size() == ts_->instruments_.size(),
               "GlobalBootstrap: number of instrument weights ("
                   << instrumentWeights_.size() << ") must match number of instruments ("
                   << ts_->instruments_.size() << ")");
    instrumentWeights_.resize(ts_->instruments_.size(), 1.0);

    // do not initialize yet: instruments could be invalid here
    // but valid later when bootstrapping is actually required
}

template <class Curve> void GlobalBootstrap<Curve>::initialize() const {

    const Date firstDate = Traits::initialDate(ts_);

    // set up alive instruments and weights
    aliveInstruments_.clear();
    aliveInstrumentWeights_.clear();
    for(Size i=0;i<ts_->instruments_.size();++i) {
        if(ts_->instruments_[i]->pillarDate() > firstDate) {
            aliveInstruments_.push_back(ts_->instruments_[i]);
            aliveInstrumentWeights_.push_back(instrumentWeights_[i]);
        }
    }

    // set up alive additional helpers
    aliveAdditionalHelpers_.clear();
    std::copy_if(additionalHelpers_.begin(), additionalHelpers_.end(),
                 std::back_inserter(aliveAdditionalHelpers_),
                 [&firstDate](const ext::shared_ptr<typename Traits::helper>& h) {
                     return h->pillarDate() > firstDate;
                 });


