std::vector<Real> remainingNotionals(const Date&) const;
        /*! Vector of surviving issuers after defaults between the reference
          basket date and the given (or evaluation) date.
        */
        const std::vector<std::string>& remainingNames() const;
        std::vector<std::string> remainingNames(const Date&) const;
        /*! Default keys of non defaulted counterparties
        */
        const std::vector<DefaultProbKey>& remainingDefaultKeys() const;
        std::vector<DefaultProbKey> remainingDefaultKeys(const Date&) const;
        //! Number of counterparties alive on the requested date.
        Size remainingSize() const;
        Size remainingSize(const Date&) const;
        /*! Vector of cumulative default probability to date d for all
            issuers still (at the evaluation date) alive in the basket.
        */
        std::vector<Probability> remainingProbabilities(const Date& d) const;
        /*!
          Attachment amount of the equivalent (after defaults) remaining basket
          The remaining attachment amount is
          RAA = max (0, attachmentAmount - cumulatedLoss())

          The remaining attachment ratio is then
          RAR = RAA / remainingNotional()
        */
        Real remainingAttachmentAmount() const;
        Real remainingAttachmentAmount(const Date& endDate) const;

        /*!
          Detachment amount of the equivalent remaining basket.
          The remaining detachment amount is
          RDA = max (0, detachmentAmount - cumulatedLoss())

          The remaining detachment ratio is then
          RDR = RDA / remainingNotional()
        */
        Real remainingDetachmentAmount() const;
        Real remainingDetachmentAmount(const Date& endDate) const;

        //! Remaining basket tranched notional on calculation date
        Real remainingTrancheNotional() const {
            calculate();
            return evalDateDetachAmmount_ - evalDateAttachAmount_;
        }
        /*! Expected basket tranched notional on the requested date
            according to the basket model. Model should have been assigned.
        */
        Real remainingTrancheNotional(const Date& endDate) const {
            calculate();
            return remainingDetachmentAmount(endDate) -
                remainingAttachmentAmount(endDate);
        }
        //!Indexes of remaining names. Notice these are names and not positions.
        const std::vector<Size>& liveList() const;
        std::vector<Size> liveList(const Date&) const;//?? keep?
        //! Assigns the default loss model to this basket. Resets calculations.
        void setLossModel(
            const ext::shared_ptr<DefaultLossModel>& lossModel);
        /*! \name Basket Loss Statistics
            Methods providing statistical metrics on the loss or value
            distribution of the basket. Most calculations rely on the pressence
            of a model assigned to the basket.
        */
        //@{
        Real expectedTrancheLoss(const Date& d) const;
        /*! The lossFraction is the fraction of losses expressed in
            inception (no losses) tranche units (e.g. 'attach level'=0%,
            'detach level'=100%)
        */
        Probability probOverLoss(const Date& d, Real lossFraction) const;
        /*!
        */
        Real percentile(const Date& d, Probability prob) const;
        /*! ESF
        */
        Real expectedShortfall(const Date& d, Probability prob) const;
        /* Split a portfolio loss along counterparties. Typically loss
        corresponds to some percentile.*/
        std::vector<Real> splitVaRLevel(const Date& date, Real loss) const;
        /*! Full loss distribution
        */
        std::map<Real, Probability> lossDistribution(const Date&) const;
        Real densityTrancheLoss(const Date& d, Real lossFraction) const;
        Real defaultCorrelation(const Date& d, Size iName, Size jName) const;
        /*! Probability vector that each of the remaining live names (
