version 
        problem, the (e.g.) time at which the modeled variable first takes a 
        given value. This problem has solution/sense depending on the transfer 
        function \f$F_i(Y_i)\f$ characteristics.

        To make direct integration and simulation time efficient virtual 
        functions have been avoided in accessing methods in the copula policy 
        and in the sampling of the random factors
    */
    template <class copulaPolicyImpl>
    class LatentModel 
        : public virtual Observer , public virtual Observable 
    {//observer if factors as quotes
    public:
      void update() override;
      //! \name Copula interface.
      //@{
      typedef copulaPolicyImpl copulaType;
      /*! Cumulative probability of the \f$ Y_i \f$ modelled latent random
          variable to take a given value.
      */
      Probability cumulativeY(Real val, Size iVariable) const {
          return copula_.cumulativeY(val, iVariable);
        }
        //! Cumulative distribution of Z, the idiosyncratic/error factors.
        Probability cumulativeZ(Real z) const {
            return copula_.cumulativeZ(z);
        }
        //! Density function of M, the market/systemic factors.
        Probability density(const std::vector<Real>& m) const {
            #if defined(QL_EXTRA_SAFETY_CHECKS)
                QL_REQUIRE(m.size() == nFactors_, 
                    "Factor size must match that of model.");
            #endif
            return copula_.density(m);
        }
        //! Inverse cumulative distribution of the systemic factor iFactor.
        Real inverseCumulativeDensity(Probability p, Size iFactor) const {
            return copula_.inverseCumulativeDensity(p, iFactor);
        }
        /*! Inverse cumulative value of the i-th random latent variable with a 
         given probability. */
        Real inverseCumulativeY(Probability p, Size iVariable) const {
            return copula_.inverseCumulativeY(p, iVariable);
        }
        /*! Inverse cumulative value of the idiosyncratic variable with a given 
        probability. */
        Real inverseCumulativeZ(Probability p) const {
            return copula_.inverseCumulativeZ(p);
        }
        /*! All factor cumulative inversion. Used in integrations and sampling.
            Inverts all the cumulative random factors probabilities in the 
            model. These are all the systemic factors plus all the idiosyncratic
            ones, so the size of the inversion is the number of systemic factors
            plus the number of latent modelled variables*/
        std::vector<Real> allFactorCumulInverter(const std::vector<Real>& probs) const {
            return copula_.allFactorCumulInverter(probs);
        }
        //@}

        /*! The value of the latent variable Y_i conditional to
            (given) a set of values of the factors.

            The passed allFactors vector contains values for all the
            independent factors in the model (systemic and
            idiosyncratic, in that order). A full sample is required,
            i.e. all the idiosyncratic values are expected to be
            present even if only the relevant one is used.
        */
        Real latentVarValue(const std::vector<Real>& allFactors, 
                            Size iVar) const 
        {
            return std::inner_product(factorWeights_[iVar].begin(), 
                // systemic term:
                factorWeights_[iVar].end(), allFactors.begin(),
                // idiosyncratic term:
                Real(allFactors[numFactors()+iVar] * idiosyncFctrs_[iVar]));
        }
        // \to do write variants of the above, although is the most common case

        const copulaType& copula() const {
            return copula_;
        }


    //  protected:
        //! \name Latent model random factor number generator facility.
        //@{
        /*!  Allows generation or random samples of the latent variable. 

            Generates samples of all the