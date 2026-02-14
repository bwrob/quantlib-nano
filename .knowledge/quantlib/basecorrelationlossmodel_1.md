ng model to be of a latent type. This link is due to the copula 
    initialization traits which have to be present for non trivial copula 
    policies initialization (e.g. Student-T base correl models)

    Maybe a possibility is to pass copiable instances of the model and relinking
    to the correlation in two internal copies.
    */
    template <class BaseModel_T, class Corr2DInt_T>
    class BaseCorrelationLossModel : public DefaultLossModel, 
        public virtual Observer {
    private:
        typedef typename BaseModel_T::copulaType::initTraits initTraits;
    public:
      BaseCorrelationLossModel(const Handle<BaseCorrelationTermStructure<Corr2DInt_T> >& correlTS,
                               std::vector<Real> recoveries,
                               const initTraits& traits = initTraits())
      : localCorrelationAttach_(ext::make_shared<SimpleQuote>(0.)),
        localCorrelationDetach_(ext::make_shared<SimpleQuote>(0.)),
        recoveries_(std::move(recoveries)), correlTS_(correlTS), copulaTraits_(traits) {
          registerWith(correlTS);
          registerWith(Settings::instance().evaluationDate());
      }

    private:
        // react to base correl surface notifications (quotes or reference date)
      void update() override {
          setupModels();
          // tell basket to notify instruments, etc, we are invalid
          if (!basket_.empty())
              basket_->notifyObservers();
      }

        /* Update model caches after basket assignement. */
      void resetModel() override {
          remainingNotional_ = basket_->remainingNotional();
          attachRatio_ = basket_->remainingAttachmentAmount() / remainingNotional_;
          detachRatio_ = basket_->remainingDetachmentAmount() / remainingNotional_;

          basketAttach_ = ext::make_shared<Basket>(basket_->refDate(), basket_->remainingNames(),
                                                   basket_->remainingNotionals(), basket_->pool(),
                                                   0.0, attachRatio_, basket_->claim());
          basketDetach_ = ext::make_shared<Basket>(basket_->refDate(), basket_->remainingNames(),
                                                   basket_->remainingNotionals(), basket_->pool(),
                                                   0.0, detachRatio_, basket_->claim());
          setupModels();
      }
        /* Most of the statistics are not implemented, not impossible but
        the model is intended for pricing rather than ptfolio risk management.
        */
      Real expectedTrancheLoss(const Date& d) const override;

    protected:
        /*! Sets up attach/detach models. Gets called on basket update. 
        To be specialized on the spacific model type.
        */
        void setupModels() const;
    private:
        mutable Real attachRatio_, detachRatio_;
        mutable Real remainingNotional_;

        //! Correlation buffer to pick up values from the surface and 
        //  trigger calculation.
        ext::shared_ptr<SimpleQuote> localCorrelationAttach_, 
            localCorrelationDetach_;
        mutable ext::shared_ptr<Basket> basketAttach_,
            basketDetach_;
        // just cached for the update method
        mutable std::vector<Real> recoveries_;
        Handle<BaseCorrelationTermStructure<Corr2DInt_T> > correlTS_;
        // Initialization parameters for models copula
        mutable typename BaseModel_T::copulaType::initTraits copulaTraits_;
        // Models of equity baskets.
        mutable ext::shared_ptr<BaseModel_T> scalarCorrelModelAttach_;
        mutable ext::shared_ptr<BaseModel_T> scalarCorrelModelDetach_;
    };


    // Remember ETL returns the EL on the live part of the basket. 
    template<class LM, class I>
    Real BaseCorrelationLossModel<LM, I>::expectedTrancheLoss(
        const Date& d) const 
    {
        Real correlK1 = correlTS_->correlation(d, attachRatio_);
        Real correlK2 = correlTS_->correlation(d, detachRatio_);

    