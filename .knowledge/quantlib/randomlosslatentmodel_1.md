ember fucntions.
        */
        friend class RandomLM< ::QuantLib::RandomLossLM, copulaPolicy, USNG>;
    protected:
        void nextSample(const std::vector<Real>& values) const;

        // see note on randomdefaultlatentmodel
        void initDates() const {
            /* Precalculate horizon time default probabilities (used to
              determine if the default took place and subsequently compute its
              event time)
            */
            Date today = Settings::instance().evaluationDate();
            Date maxHorizonDate = today  + Period(this->maxHorizon_, Days);

            const ext::shared_ptr<Pool>& pool = this->basket_->pool();
            for(Size iName=0; iName < this->basket_->size(); ++iName)//use'live'
                horizonDefaultPs_.push_back(pool->get(pool->names()[iName]).
                    defaultProbability(this->basket_->defaultKeys()[iName])
                        ->defaultProbability(maxHorizonDate, true));
        }
       Real getEventRecovery(const defaultSimEvent& evt) const {
            return evt.recovery();
        }

        Real latentVarValue(const std::vector<Real>& factorsSample,
            Size iVar) const {
                return copula_->latentVarValue(factorsSample, iVar);
        }
        Size basketSize() const { return this->basket_->size(); }
        // conditional to default, defined as spot-recovery.
        Real conditionalRecovery(Real latentVarSample, Size iName,
            const Date& d) const;
    private:
      void resetModel() override {
          /* Explore: might save recalculation if the basket is the same
          (some situations, like BC or control variates) in that case do not
          update, only reset the copula's basket.
          */
          copula_->resetBasket(this->basket_.currentLink());

          QL_REQUIRE(2 * this->basket_->size() == copula_->size(),
                     "Incompatible basket and model sizes.");
          // invalidate current calculations if any and notify observers
          // NOLINTNEXTLINE(bugprone-parent-virtual-call)
          LazyObject::update();
      }
        // Default probabilities for each name at the time of the maximun
        //   horizon date. Cached for perf.
        mutable std::vector<Probability> horizonDefaultPs_;
    };


    // --------------------------------------------------------------


    template<class C, class URNG>
    void RandomLossLM<C, URNG>::nextSample(
        const std::vector<Real>& values) const
    {
        const ext::shared_ptr<Pool>& pool = this->basket_->pool();
        this->simsBuffer_.push_back(std::vector<defaultSimEvent> ());

        // half the model is defaults, the other half are RRs...
        for(Size iName=0; iName<copula_->size()/2; iName++) {
            // ...but samples must be full
            /* This is really a trick, we are passing a longer than
            expected set of values in the sample but the last idiosyncratic
            values corresponding to the RR are not used. They are used below
            only if we are in default. This works due to the way the SpotLossLM
            is split in two almost disjoint latent models and that theres no
            check on the vector size in the LM base class.
            */
            Real latentVarSample =
                copula_->latentVarValue(values, iName);
            Probability simDefaultProb =
                copula_->cumulativeY(latentVarSample, iName);
            // If the default simulated lies before the max date:
            if (horizonDefaultPs_[iName] >= simDefaultProb) {
                const Handle<DefaultProbabilityTermStructure>& dfts =
                    pool->get(pool->names()[iName]).  // use 'live' names
                    defaultProbability(this->basket_->defaultKeys()[iName]);
                // compute and store default time with respect to the
                //  curve ref date:
                Size dateSTride =
                    static_cast<S
