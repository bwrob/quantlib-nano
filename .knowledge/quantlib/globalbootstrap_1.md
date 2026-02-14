Forward,
  i.e. the usual IR curves traits in QL. It requires Traits::transformDirect()
  and Traits::transformInverse() to be implemented. Also, check the usage of
  Traits::updateGuess(), Traits::guess() in this class.
*/
template <class Curve> class GlobalBootstrap final : public MultiCurveBootstrapContributor {
    typedef typename Curve::traits_type Traits;             // ZeroYield, Discount, ForwardRate
    typedef typename Curve::interpolator_type Interpolator; // Linear, LogLinear, ...
    typedef std::function<Array(const std::vector<Time>&, const std::vector<Real>&)>
        AdditionalPenalties;

  public:
    GlobalBootstrap(Real accuracy = Null<Real>(),
                    ext::shared_ptr<OptimizationMethod> optimizer = nullptr,
                    ext::shared_ptr<EndCriteria> endCriteria = nullptr,
                    std::vector<Real> instrumentWeights = {});
    GlobalBootstrap(std::vector<ext::shared_ptr<typename Traits::helper>> additionalHelpers,
                    std::function<std::vector<Date>()> additionalDates,
                    AdditionalPenalties additionalPenalties,
                    Real accuracy = Null<Real>(),
                    ext::shared_ptr<OptimizationMethod> optimizer = nullptr,
                    ext::shared_ptr<EndCriteria> endCriteria = nullptr,
                    ext::shared_ptr<AdditionalBootstrapVariables> additionalVariables = nullptr,
                    std::vector<Real> instrumentWeights = {});
    GlobalBootstrap(std::vector<ext::shared_ptr<typename Traits::helper>> additionalHelpers,
                    std::function<std::vector<Date>()> additionalDates,
                    std::function<Array()> additionalPenalties,
                    Real accuracy = Null<Real>(),
                    ext::shared_ptr<OptimizationMethod> optimizer = nullptr,
                    ext::shared_ptr<EndCriteria> endCriteria = nullptr,
                    ext::shared_ptr<AdditionalBootstrapVariables> additionalVariables = nullptr,
                    std::vector<Real> instrumentWeights = {});
    void setup(Curve *ts);
    void calculate() const;

  private:
    void initialize() const;
    void
    setParentBootstrapper(const ext::shared_ptr<MultiCurveBootstrap>& b) const override;
    Array setupCostFunction() const override;
    void setCostFunctionArgument(const Array& v) const override;
    Array evaluateCostFunction() const override;
    void setToValid() const override;
    Curve* ts_;
    Real accuracy_;
    ext::shared_ptr<OptimizationMethod> optimizer_;
    ext::shared_ptr<EndCriteria> endCriteria_;
    std::vector<ext::shared_ptr<typename Traits::helper>> additionalHelpers_;
    mutable std::vector<ext::shared_ptr<typename Traits::helper>> aliveInstruments_;
    mutable std::vector<ext::shared_ptr<typename Traits::helper>> aliveAdditionalHelpers_;
    std::function<std::vector<Date>()> additionalDates_;
    AdditionalPenalties additionalPenalties_;
    ext::shared_ptr<AdditionalBootstrapVariables> additionalVariables_;
    mutable std::vector<Real> instrumentWeights_;
    mutable std::vector<Real> aliveInstrumentWeights_;
    mutable bool initialized_ = false, validCurve_ = false;
    mutable ext::shared_ptr<MultiCurveBootstrap> parentBootstrapper_ = nullptr;
};

// template definitions

template <class Curve>
GlobalBootstrap<Curve>::GlobalBootstrap(Real accuracy,
                                        ext::shared_ptr<OptimizationMethod> optimizer,
                                        ext::shared_ptr<EndCriteria> endCriteria,
                                        std::vector<Real> instrumentWeights)
: ts_(nullptr), accuracy_(accuracy), optimizer_(std::move(optimizer)),
  endCriteria_(std::move(endCriteria)), instrumentWeights_(std::move(instrumentWeights)) {}

template <class Curve>
GlobalBootstrap<Curve>::GlobalBootstrap(
    std::vector<ext::shared_ptr<typename Traits::helper>> additionalHelpers,
    std::function<std::vector<Date>()> additionalDates,
    AdditionalPenalties ad
