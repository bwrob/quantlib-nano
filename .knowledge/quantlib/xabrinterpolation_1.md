 XABRInterpolationImpl final : public Interpolation::templateImpl<I1, I2>,
                                    public XABRCoeffHolder<Model> {
  public:
    XABRInterpolationImpl(const I1& xBegin,
                          const I1& xEnd,
                          const I2& yBegin,
                          Time t,
                          const Real& forward,
                          const std::vector<Real>& params,
                          const std::vector<bool>& paramIsFixed,
                          bool vegaWeighted,
                          ext::shared_ptr<EndCriteria> endCriteria,
                          ext::shared_ptr<OptimizationMethod> optMethod,
                          const Real errorAccept,
                          const bool useMaxError,
                          const Size maxGuesses,
                          const std::vector<Real>& addParams = std::vector<Real>(),
                          VolatilityType volatilityType = VolatilityType::ShiftedLognormal)
    : Interpolation::templateImpl<I1, I2>(xBegin, xEnd, yBegin, 1),
      XABRCoeffHolder<Model>(t, forward, params, paramIsFixed, addParams),
      endCriteria_(std::move(endCriteria)), optMethod_(std::move(optMethod)),
      errorAccept_(errorAccept), useMaxError_(useMaxError), maxGuesses_(maxGuesses),
      vegaWeighted_(vegaWeighted), volatilityType_(volatilityType) {
        // if no optimization method or endCriteria is provided, we provide one
        if (!optMethod_)
            optMethod_ = ext::shared_ptr<OptimizationMethod>(
                new LevenbergMarquardt(1e-8, 1e-8, 1e-8));
        // optMethod_ = ext::shared_ptr<OptimizationMethod>(new
        //    Simplex(0.01));
        if (!endCriteria_) {
            endCriteria_ = ext::make_shared<EndCriteria>(
                60000, 100, 1e-8, 1e-8, 1e-8);
        }
        this->weights_ =
            std::vector<Real>(xEnd - xBegin, 1.0 / (xEnd - xBegin));
    }

    void update() override {

        this->updateModelInstance();

        // we should also check that y contains positive values only

        // we must update weights if it is vegaWeighted
        if (vegaWeighted_) {
            I1 x = this->xBegin_;
            I2 y = this->yBegin_;
            // std::vector<Real>::iterator w = weights_.begin();
            this->weights_.clear();
            Real weightsSum = 0.0;
            for (; x != this->xEnd_; ++x, ++y) {
                Real stdDev = std::sqrt((*y) * (*y) * this->t_);
                this->weights_.push_back(Model().weight(*x, this->forward_, stdDev,
                                                        this->addParams_));
                weightsSum += this->weights_.back();
            }
            // weight normalization
            auto w = this->weights_.begin();
            for (; w != this->weights_.end(); ++w)
                *w /= weightsSum;
        }

        // there is nothing to optimize
        if (std::accumulate(this->paramIsFixed_.begin(),
                            this->paramIsFixed_.end(), true,
                            std::logical_and<>())) {
            this->error_ = interpolationError();
            this->maxError_ = interpolationMaxError();
            this->XABREndCriteria_ = EndCriteria::None;
            return;
        } else {
            XABRError costFunction(this);

            Array guess(Model().dimension());
            for (Size i = 0; i < guess.size(); ++i)
                guess[i] = this->params_[i];

            Size iterations = 0;
            Size freeParameters = 0;
            Real bestError = QL_MAX_REAL;
            Array bestParameters;
            for (Size i = 0; i < Model().dimension(); ++i)
                if (!this->paramIsFixed_[i])
                    ++freeParameters;
            HaltonRsg halton(freeParameters, 42);
            EndCriteria::Type tmpEndCriteria;
            Real tmpInterpolationError;

            do {

                if (iterations > 0) {
                    const auto& s = halt