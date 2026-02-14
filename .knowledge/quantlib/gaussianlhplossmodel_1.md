rageRecovery(d);
          Probability prob = averageProb(d);
          Real remainingAttachAmount = basket_->remainingAttachmentAmount();
          Real remainingDetachAmount = basket_->remainingDetachmentAmount();


          // const Real attach = std::min(remainingAttachAmount
          //    / remainingfullNot, 1.);
          // const Real detach = std::min(remainingDetachAmount
          //    / remainingfullNot, 1.);
          const Real attach = remainingAttachAmount / remainingfullNot;
          const Real detach = remainingDetachAmount / remainingfullNot;

          return expectedTrancheLossImpl(remainingfullNot, prob, averageRR, attach, detach);
      }

        /*! The passed remainingLossFraction is in live tranche units,
            not portfolio as a fraction of the remaining(live) tranche
            (i.e. a_remaining=0% and det_remaining=100%)
        */
      Real probOverLoss(const Date& d, Real remainingLossFraction) const override;

      //! Returns the ESF as an absolute amount (rather than a fraction)
      /* The way it is implemented here is a transformation from ETL to ESF
      is a generic algorithm, not specific to this model so it should be moved
      to the Basket/DefaultLossModel class.
      TO DO: Implement the inverse transformation
      */
      Real expectedShortfall(const Date& d, Probability perctl) const override;

    protected:
        // This is wrong, it is not accounting for the current defaults ....
        // returns the loss value in actual loss units, returns the loss value 
        // for the underlying portfolio, untranched
        Real percentilePortfolioLossFraction(const Date& d, Real perctl) const;
        Real expectedRecovery(const Date& d, Size iName, const DefaultProbKey& ik) const override {
            return rrQuotes_[iName].currentLink()->value();
        }

    public:
        // same as percentilePortfolio but tranched
      Real percentile(const Date& d, Real perctl) const override {
          const Real remainingNot = basket_->remainingNotional(d);
          Real remainingAttachAmount = basket_->remainingAttachmentAmount();
          Real remainingDetachAmount = basket_->remainingDetachmentAmount();
          const Real attach = std::min(remainingAttachAmount / remainingNot, 1.);
          const Real detach = std::min(remainingDetachAmount / remainingNot, 1.);
          return remainingNot *
                 std::min(std::max(percentilePortfolioLossFraction(d, perctl) - attach, 0.),
                          detach - attach);
      }

        Probability averageProb(const Date& d) const {// not an overload of Deflossmodel ???<<<<<???
            // weighted average by programmed exposure.
            const std::vector<Probability> probs = 
                basket_->remainingProbabilities(d);//use remaining basket
            const std::vector<Real> remainingNots = 
                basket_->remainingNotionals(d);
            return std::inner_product(probs.begin(), probs.end(), 
                remainingNots.begin(), Real(0.)) / basket_->remainingNotional(d);
        }

        /* One could define the average recovery without the probability
        factor, weighting only by notional instead, but that way the expected 
        loss of the average/aggregated and the original portfolio would not 
        coincide. This introduces however a time dependence in the recovery 
        value.
        Weighting by notional implies time dependent weighting since the basket 
        might amortize.
        */
        Real averageRecovery(
            const Date& d) const //no explicit time dependence in this model
        {
            const std::vector<Probability> probs = 
                basket_->remainingProbabilities(d);
            std::vector<Real> recoveries;
            recoveries.reserve(basket_->remainingSize());
            for(Size i=0; i<basket_->remainingSize(); i++)
                recoveries.push_back(rrQuotes_[i]->value());
            std::vector<Real