/
        void resetBasket(const ext::shared_ptr<Basket>& basket) const {
            basket_ = basket;
            // in the future change 'size' to 'liveSize'
            QL_REQUIRE(basket_->size() == factorWeights_.size(),
                "Incompatible new basket and model sizes.");
        }

        /*! Returns the probability of default of a given name conditional on
        the realization of a given set of values of the model independent
        factors. The date at which the probability is given is implicit in the
        probability since theres not other time dependence in this model.
        @param prob Unconditional probability of default.
        @param iName desired name.
        @param mktFactors Value of LM independent factors.
        \warning Most often it is preferred to use the method below avoiding the
        cumulative inversion.
        */
        Probability conditionalDefaultProbability(Probability prob, Size iName,
            const std::vector<Real>& mktFactors) const
        {
            // we can be called from the outside (from an integrable loss model)
            //   but we are called often at integration points. This or
            //   consider a list of friends.
        #if defined(QL_EXTRA_SAFETY_CHECKS)
            QL_REQUIRE(basket_, "No portfolio basket set.");
        #endif
            /*Avoid redundant call to minimum value inversion (might be \infty),
            and this independently of the copula function.
            */
            if (prob < 1.e-10) return 0.;// use library macro...
            return conditionalDefaultProbabilityInvP(
                inverseCumulativeY(prob, iName), iName, mktFactors);
        }
    protected:
      void update() override {
          if (basket_ != nullptr)
              basket_->notifyObservers();
          LatentModel<copulaPolicy>::update();
      }

    public:// open since users access it for performance on joint integrations.

        /*! Returns the probability of default of a given name conditional on
        the realization of a given set of values of the model independent
        factors. The date at which the probability is given is implicit in the
        probability since theres not other time dependent in this model.
        Same intention as above but provides a performance opportunity, if the
        integration is along the market factors (as usually is) avoids computing
        the inverse of the probability on each call.
        @param invCumYProb Inverse cumul of the unconditional probability of
          default, has to follow the same copula law for results to be coherent
        @param iName desired name.
        @param m Value of LM independent factors.
        */
        Probability conditionalDefaultProbabilityInvP(Real invCumYProb,
            Size iName,
            const std::vector<Real>& m) const {
            Real sumMs =
                std::inner_product(factorWeights_[iName].begin(),
                    factorWeights_[iName].end(), m.begin(), Real(0.));
            Real res = cumulativeZ((invCumYProb - sumMs) /
                    idiosyncFctrs_[iName] );
            #if defined(QL_EXTRA_SAFETY_CHECKS)
            QL_REQUIRE (res >= 0. && res <= 1.,
                        "conditional probability " << res << "out of range");
            #endif

            return res;
        }
    protected:
        /*! Returns the probability of default of a given name conditional on
        the realization of a given set of values of the model independent
        factors.
        @param date The date for the probability of default.
        @param iName desired name.
        @param mktFactors Value of LM independent factors.

        Same intention as the above methods. Usage of this one is typically more
        expensive because most often the date we call this method with
        repeats itself and with this one the probability can not be cached
        outside the call.
        */
        Probability conditionalDefau