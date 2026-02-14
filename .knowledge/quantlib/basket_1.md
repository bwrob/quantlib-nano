ties.
        Size size() const;
        //! Basket counterparties names at inception.
        const std::vector<std::string>& names() const {return pool_->names();}
        //! Basket counterparties notionals at inception.
        const std::vector<Real>& notionals() const;
        //! Basket total notional at inception.
        Real notional() const;
        //! Returns the total expected exposures for that name.
        Real exposure(const std::string& name, const Date& = Date()) const;
        //! Underlying pool
        const ext::shared_ptr<Pool>& pool() const;
        //! The keys each counterparty enters the basket with (sensitive to)
        std::vector<DefaultProbKey> defaultKeys() const;
        /*! Loss Given Default for all issuers/notionals based on
            expected recovery rates for the respective issuers.
        */
        //! Basket inception date.
        const Date& refDate() const {return refDate_;}
        /*! Attachment point expressed as a fraction of the total inception
          notional.
        */
        Real attachmentRatio() const {return attachmentRatio_;}
        //! Detachment point expressed as a fraction of the total pool notional
        Real detachmentRatio() const {return detachmentRatio_;}
        //! Original basket notional ignoring any losses.
        Real basketNotional() const {return basketNotional_;}
        //! Original tranche notional ignoring any realized losses.
        Real trancheNotional() const {return trancheNotional_;}
        //! Attachment amount = attachmentRatio() * basketNotional()
        Real attachmentAmount() const {return attachmentAmount_;}
        //! Detachment amount = detachmentRatio() * basketNotional()
        Real detachmentAmount() const {return detachmentAmount_;}
        //! default claim, same for all positions and counterparties
        ext::shared_ptr<Claim> claim() const {return claim_;}
        /*! Vector of cumulative default probability to date d for all
            issuers in the basket.
        */
        std::vector<Probability> probabilities(const Date& d) const;
        /*! Realized basket losses between the reference date and the
            calculation date, taking the actual recovery rates of loss events
            into account.
            Only default events that have settled (have a realized RR) are
            accounted for. For contingent losses after a default you need
            to compute the losses through a DefaultLossModel

            Optionally one can pass a date in the future and that will collect
            events stored in the issuers list. This shows the effect of
            'programmed' (after today's) events on top of past ones. The
            intention is to be used in risk analysis (jump to default, etc).
        */
        Real settledLoss() const;
        Real settledLoss(const Date&) const;
        /*! Actual basket losses between the reference date and the calculation
            date, taking the actual recovery rates of loss events into account.
            If the event has not settled yet a model driven recovery is used.

            Returns the realized losses in this portfolio since the portfolio
            default reference date.
            This method relies on an implementation of the loss given default
            since the events have not necessarily settled.
        */
        Real cumulatedLoss() const;
        Real cumulatedLoss(const Date&) const;
        /*! Remaining full basket (untranched) notional after settled losses
          between the reference date and the given date.  The full notional
          for defaulted names is subracted, recovery ignored.
        */
        Real remainingNotional() const;
        Real remainingNotional(const Date&) const;
        /*! Vector of surviving notionals after settled losses between the
          reference date and the given date, recovery ignored.
        */
        const std::vector<Real>& remainingNotionals() const;

