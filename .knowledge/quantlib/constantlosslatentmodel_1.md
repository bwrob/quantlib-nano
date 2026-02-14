Keys) const {
            return recoveries_[iName];
        }
    };

    typedef ConstantLossLatentmodel<GaussianCopulaPolicy> 
        GaussianConstantLossLM;
    typedef ConstantLossLatentmodel<TCopulaPolicy> TConstantLossLM;


    /*! ConstantLossLatentModel interface for loss models. 
    While it does not provide distribution type losses (e.g. expected tranche 
    losses) because it lacks an integration algorithm it serves to allow 
    pricing of digital type products like NTDs.

    Alternatively fuse with the aboves class.
    */
    template <class copulaPolicy>
    class ConstantLossModel : 
        public virtual ConstantLossLatentmodel<copulaPolicy>, 
        public virtual DefaultLossModel 
    {
    public:
        ConstantLossModel(
            const std::vector<std::vector<Real> >& factorWeights,
            const std::vector<Real>& recoveries,
            LatentModelIntegrationType::LatentModelIntegrationType integralType,
            const typename copulaPolicy::initTraits& ini = 
                copulaPolicy::initTraits()) 
        : ConstantLossLatentmodel<copulaPolicy>(factorWeights, recoveries, 
            integralType, ini) {}

        ConstantLossModel(
            const Handle<Quote>& mktCorrel,
            const std::vector<Real>& recoveries,
            LatentModelIntegrationType::LatentModelIntegrationType integralType,
            Size nVariables,
            const typename copulaPolicy::initTraits& ini = 
                copulaPolicy::initTraits()) 
        : ConstantLossLatentmodel<copulaPolicy>(mktCorrel, recoveries, 
            integralType, nVariables,ini) {}

    protected:
        //std::vector<Probability> probsBeingNthEvent(
        //    Size n, const Date& d) const {
        //    return 
        //      ConstantLossLatentmodel<copulaPolicy>::probsBeingNthEvent(n, d);
        //}
      Real defaultCorrelation(const Date& d, Size iName, Size jName) const override {
          return ConstantLossLatentmodel<copulaPolicy>::defaultCorrelation(d, iName, jName);
      }
      Probability probAtLeastNEvents(Size n, const Date& d) const override {
          return ConstantLossLatentmodel<copulaPolicy>::probAtLeastNEvents(n, d);
      }
      Real expectedRecovery(const Date& d, Size iName, const DefaultProbKey& k) const override {
          return ConstantLossLatentmodel<copulaPolicy>::expectedRecovery(d, iName, k);
      }

    private:
      void resetModel() override {
          // update the default latent model we derive from
          DefaultLatentModel<copulaPolicy>::resetBasket(
              DefaultLossModel::basket_.currentLink()); // forces interface
      }
    };

}

#endif