at eval
          date) is the n-th default by date d.

          The n parameter is the internal index to the name; it should
          be alive at the evaluation date.

        ---------TO DO: Implement with a string passed----------------------
        ---------TO DO: Perform check the name is alive---------------------
        */
        std::vector<Probability> probsBeingNthEvent(
            Size n, const Date& d) const;
        /*! Returns the probaility of having a given or larger number of 
        defaults in the basket portfolio at a given time.
        */
        Probability probAtLeastNEvents(Size n, const Date& d) const;
        /*! Expected recovery rate of the underlying position as a fraction of 
          its exposure value at date d _given_ it has defaulted _on_ that date.
          NOTICE THE ARG IS THE CTPTY....SHOULDNT IT BE THE POSITION/INSTRUMENT?????<<<<<<<<<<<<<<<<<<<<<<<
        */
        Real recoveryRate(const Date& d, Size iName) const;
        //@}
      private:
        // LazyObject interface
        void performCalculations() const override;

        std::vector<Real> notionals_;
        ext::shared_ptr<Pool> pool_;
        //! The claim is the same for all names
        const ext::shared_ptr<Claim> claim_;

        Real attachmentRatio_;
        Real detachmentRatio_;
        Real basketNotional_;
        //! basket tranched inception attachment amount:
        mutable Real attachmentAmount_;
        //! basket tranched inception detachment amount:
        mutable Real detachmentAmount_;
        //! basket tranched notional amount:
        mutable Real trancheNotional_;
        /* Caches. Most of the times one wants statistics on the distribution of
        futures losses at arbitrary dates but some problems (e.g. derivatives 
        pricing) work with todays (evalDate) magnitudes which do not require a 
        loss model and would be too expensive to recompute on every call.
        */
        mutable Real evalDateSettledLoss_,
            evalDateRemainingNot_,
            evalDateAttachAmount_,
            evalDateDetachAmmount_;
        mutable std::vector<Size> evalDateLiveList_;
        mutable std::vector<Real> evalDateLiveNotionals_;
        mutable std::vector<std::string> evalDateLiveNames_;
        mutable std::vector<DefaultProbKey> evalDateLiveKeys_;
        //! Basket inception date.
        const Date refDate_;
        /* It is the basket responsibility to ensure that the model assigned it 
          is properly initialized to the basket current data. 
          This might not be the case for various reasons: the basket data might
          have been updated, the evaluation date has changed or the model has 
          received another request from another basket pointing to it. For
          this last reason we can never be sure between calls that this is the 
          case (and that is true in a single thread environment only).
        */
        ext::shared_ptr<DefaultLossModel> lossModel_;
    };

    // ------------ Inlines -------------------------------------------------

    inline Size Basket::size() const {
        return pool_->size();
    }

    inline const std::vector<Real>& Basket::notionals() const {
        return notionals_;
    }

    inline std::vector<DefaultProbKey> Basket::defaultKeys() const {
        return pool_->defaultKeys();
    }

    inline const ext::shared_ptr<Pool>& Basket::pool() const {
        return pool_;
    }

    inline const std::vector<Size>& Basket::liveList() const {
        return evalDateLiveList_;
    }

    inline Real Basket::remainingDetachmentAmount() const {
        return evalDateDetachAmmount_;
    }

    inline Real Basket::remainingAttachmentAmount() const {
        return evalDateAttachAmount_;
    }

    inline const std::vector<std::string>& Basket::remainingNames() const {
        return evalDateLiveNames_;
    }

    inline const std::vector<Real>& Basket::remainingNotionals() const {
        return evalDateLiveN