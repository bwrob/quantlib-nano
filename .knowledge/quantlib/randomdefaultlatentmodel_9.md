 recovery
        amounts.
    */
    template<class copulaPolicy, class USNG = SobolRsg>
    class RandomDefaultLM : public RandomLM<RandomDefaultLM, copulaPolicy, USNG>
    {
    private:
        typedef simEvent<RandomDefaultLM> defaultSimEvent;

        // \todo Consider this to be only a ConstantLossLM instead
        const ext::shared_ptr<DefaultLatentModel<copulaPolicy> > model_;
        const std::vector<Real> recoveries_;
        // for time inversion:
        Real accuracy_;
    public:
        // \todo: Allow a constructor building its own default latent model.
      explicit RandomDefaultLM(const ext::shared_ptr<DefaultLatentModel<copulaPolicy> >& model,
                               const std::vector<Real>& recoveries = std::vector<Real>(),
                               Size nSims = 0, // stats will crash on div by zero, FIX ME.
                               Real accuracy = 1.e-6,
                               BigNatural seed = 2863311530UL)
      : RandomLM< ::QuantLib::RandomDefaultLM, copulaPolicy, USNG>(
            model->numFactors(), model->size(), model->copula(), nSims, seed),
        model_(model),
        recoveries_(recoveries.empty() ? std::vector<Real>(model->size(), 0.) : recoveries),
        accuracy_(accuracy) {
          // redundant through basket?
          this->registerWith(Settings::instance().evaluationDate());
          this->registerWith(model_);
        }
        explicit RandomDefaultLM(
            const ext::shared_ptr<ConstantLossLatentmodel<copulaPolicy> >& model,
            Size nSims = 0,// stats will crash on div by zero, FIX ME.
            Real accuracy = 1.e-6,
            BigNatural seed = 2863311530UL)
        : RandomLM< ::QuantLib::RandomDefaultLM, copulaPolicy, USNG>
            (model->numFactors(), model->size(), model->copula(),
                nSims, seed ),
          model_(model),
          recoveries_(model->recoveries()),
          accuracy_(accuracy)
        {
            // redundant through basket?
            this->registerWith(Settings::instance().evaluationDate());
            this->registerWith(model_);
        }

        // grant access to static polymorphism:
        /* While this works on g++, VC9 refuses to compile it.
        Not completely sure whos right; individually making friends of the
        calling members or writing explicitly the derived class T parameters
        throws the same errors.
        The access is then open to the member fucntions.
        Another solution is to use this http://accu.org/index.php/journals/296

        It might well be that gcc is allowing some c11 features silently, which
        wont pass on a lower gcc version.
        */
        friend class RandomLM< ::QuantLib::RandomDefaultLM, copulaPolicy, USNG>;
    protected:
        void nextSample(const std::vector<Real>& values) const;
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
            return recoveries_[evt.nameIdx];
        }
        Real expectedRecovery(const Date&, Size iName, const DefaultProbKey&) const override {
            // deterministic
            return recoveries_[iName];
        }

        Real latentVarValue(const std::vector<Real>& factorsSample,
            Size iVar) const {

