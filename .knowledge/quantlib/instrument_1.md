this attribute and any other that derived
            classes might declare must be set during calculation.
        */
        //@{
        mutable Real NPV_, errorEstimate_;
        mutable Date valuationDate_;
        mutable std::map<std::string, ext::any> additionalResults_;
        //@}
        ext::shared_ptr<PricingEngine> engine_;
    };

    class Instrument::results : public virtual PricingEngine::results {
      public:
        void reset() override {
            value = errorEstimate = Null<Real>();
            valuationDate = Date();
            additionalResults.clear();
        }
        Real value;
        Real errorEstimate;
        Date valuationDate;
        std::map<std::string, ext::any> additionalResults;
    };


    // inline definitions

    inline void Instrument::calculate() const {
        if (!calculated_) {
            if (isExpired()) {
                setupExpired();
                calculated_ = true;
            } else {
                LazyObject::calculate();
            }
        }
    }

    inline void Instrument::setupExpired() const {
        NPV_ = errorEstimate_ = 0.0;
        valuationDate_ = Date();
        additionalResults_.clear();
    }

    inline void Instrument::performCalculations() const {
        QL_REQUIRE(engine_, "null pricing engine");
        engine_->reset();
        setupArguments(engine_->getArguments());
        engine_->getArguments()->validate();
        engine_->calculate();
        fetchResults(engine_->getResults());
    }

    inline void Instrument::fetchResults(
                                      const PricingEngine::results* r) const {
        const auto* results = dynamic_cast<const Instrument::results*>(r);
        QL_ENSURE(results != nullptr, "no results returned from pricing engine");

        NPV_ = results->value;
        errorEstimate_ = results->errorEstimate;
        valuationDate_ = results->valuationDate;

        additionalResults_ = results->additionalResults;
    }

    inline Real Instrument::NPV() const {
        calculate();
        QL_REQUIRE(NPV_ != Null<Real>(), "NPV not provided");
        return NPV_;
    }

    inline Real Instrument::errorEstimate() const {
        calculate();
        QL_REQUIRE(errorEstimate_ != Null<Real>(),
                   "error estimate not provided");
        return errorEstimate_;
    }

    inline const Date& Instrument::valuationDate() const {
        calculate();
        QL_REQUIRE(valuationDate_ != Date(),
                   "valuation date not provided");
        return valuationDate_;
    }

    inline const ext::shared_ptr<PricingEngine>& Instrument::pricingEngine() const {
        return engine_;
    }

    template <class T>
    inline T Instrument::result(const std::string& tag) const {
        calculate();
        auto value =
            additionalResults_.find(tag);
        QL_REQUIRE(value != additionalResults_.end(),
                   tag << " not provided");
        return ext::any_cast<T>(value->second);
    }

    inline const std::map<std::string, ext::any>&
    Instrument::additionalResults() const {
        calculate();
        return additionalResults_;
    }

}

#endif