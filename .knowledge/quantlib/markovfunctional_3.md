Real> yearFractions_;
            Real atm_ = Null<Real>();
            Real annuity_ = Null<Real>();
            ext::shared_ptr<SmileSection> smileSection_;
            ext::shared_ptr<SmileSection> rawSmileSection_;
            Real minRateDigital_ = Null<Real>();
            Real maxRateDigital_ = Null<Real>();
        };

// utility macro to write messages to the model outputs

#define QL_MFMESSAGE(o, message)                                               \
    {                                                                          \
        std::ostringstream os;                                                 \
        os << message;                                                         \
        o.messages_.push_back(os.str());                                       \
    }

        struct ModelOutputs {
            bool dirty_;
            ModelSettings settings_;
            std::vector<Date> expiries_;
            std::vector<Period> tenors_;
            std::vector<Real> atm_;
            std::vector<Real> annuity_;
            std::vector<Real> adjustmentFactors_;
            std::vector<Real> digitalsAdjustmentFactors_;
            std::vector<std::string> messages_;
            std::vector<std::vector<Real> > smileStrikes_;
            std::vector<std::vector<Real> > marketRawCallPremium_;
            std::vector<std::vector<Real> > marketRawPutPremium_;
            std::vector<std::vector<Real> > marketCallPremium_;
            std::vector<std::vector<Real> > marketPutPremium_;
            std::vector<std::vector<Real> > modelCallPremium_;
            std::vector<std::vector<Real> > modelPutPremium_;
            std::vector<std::vector<Real> > marketVega_;
            std::vector<Real> marketZerorate_;
            std::vector<Real> modelZerorate_;
        };

        // Constructor for a swaption smile calibrated model
        MarkovFunctional(const Handle<YieldTermStructure>& termStructure,
                         Real reversion,
                         std::vector<Date> volstepdates,
                         std::vector<Real> volatilities,
                         const Handle<SwaptionVolatilityStructure>& swaptionVol,
                         const std::vector<Date>& swaptionExpiries,
                         const std::vector<Period>& swaptionTenors,
                         const ext::shared_ptr<SwapIndex>& swapIndexBase,
                         MarkovFunctional::ModelSettings modelSettings = ModelSettings());

        // Constructor for a caplet smile calibrated model
        MarkovFunctional(const Handle<YieldTermStructure>& termStructure,
                         Real reversion,
                         std::vector<Date> volstepdates,
                         std::vector<Real> volatilities,
                         const Handle<OptionletVolatilityStructure>& capletVol,
                         const std::vector<Date>& capletExpiries,
                         ext::shared_ptr<IborIndex> iborIndex,
                         MarkovFunctional::ModelSettings modelSettings = ModelSettings());

        const ModelSettings &modelSettings() const { return modelSettings_; }
        const ModelOutputs &modelOutputs() const;

        const Date &numeraireDate() const { return numeraireDate_; }
        const Time &numeraireTime() const { return numeraireTime_; }

        const Array &volatility() const { return sigma_.params(); }

        void calibrate(const std::vector<ext::shared_ptr<CalibrationHelper> >& helpers,
                       OptimizationMethod& method,
                       const EndCriteria& endCriteria,
                       const Constraint& constraint = Constraint(),
                       const std::vector<Real>& weights = std::vector<Real>(),
                       const std::vector<bool>& fixParameters = std::vector<bool>()) override {

            CalibratedModel::calibrate(helpers, method, endCriteria, constraint, weights,
                                       fixParameters.empty() ? 