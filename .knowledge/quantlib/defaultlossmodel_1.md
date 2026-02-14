<Real> splitESFLevel(const Date& d, Real loss) const {
            QL_FAIL("splitESFLevel Not implemented for this model.");
        }

        // \todo Add splits by instrument position.

        //! Full loss distribution.
        virtual std::map<Real, Probability> lossDistribution(const Date&) const {
            QL_FAIL("lossDistribution Not implemented for this model.");
        }
        //! Probability density of a given loss fraction of the basket notional.
        virtual Real densityTrancheLoss(
            const Date& d, Real lossFraction) const {
            QL_FAIL("densityTrancheLoss Not implemented for this model.");
        }
        /*! Probabilities for each of the (remaining) basket elements in the
        pool to have defaulted by time d and at the same time be the Nth
        defaulting name to default in the basket. This method is oriented to
        default order dependent portfolio pricing (e.g. NTDs)
            The the probabilities ordering in the vector coincides with the
            pool order.
        */
        virtual std::vector<Probability> probsBeingNthEvent(Size n, const Date& d) const {
            QL_FAIL("probsBeingNthEvent Not implemented for this model.");
        }
        //! Pearsons' default probability correlation.
        virtual Real defaultCorrelation(const Date& d, Size iName,
            Size jName) const {
            QL_FAIL("defaultCorrelation Not implemented for this model.");
        }
        /*! Returns the probaility of having a given or larger number of
        defaults in the basket portfolio at a given time.
        */
        virtual Probability probAtLeastNEvents(Size n, const Date& d) const {
            QL_FAIL("probAtLeastNEvents Not implemented for this model.");
        }
        /*! Expected RR for name conditinal to default by that date.
        */
        virtual Real expectedRecovery(const Date&, Size iName,
            const DefaultProbKey&) const {
            QL_FAIL("expected recovery Not implemented for this model.");
        }
        //@}

        /*! Send a reference to the basket to allow the model to read the
        problem arguments (contained in the basket)
        */
    private: //can only be called from Basket
        void setBasket(Basket* bskt) {
            /* After this; if the model modifies its internal status/caches (if
            any) it should notify the  prior basket to recognise that basket is
            not in a calculated=true state. Since we dont know at this level if
            the model keeps caches it is the children responsibility. Typically
            this is done at the first call to calculate to the loss model, there
            it notifies the basket. The old basket is still registered with us
            until the basket takes in a new model....
            ..alternatively both old basket and model could be forced reset here
            */
            basket_.linkTo(ext::shared_ptr<Basket>(bskt, null_deleter()),
                           false);
            resetModel();// or rename to setBasketImpl(...)
        }
        // the call order matters, which is the reason for the parent to be the
        //   sole caller.
        //! Concrete models do now any updates/inits they need on basket reset
        virtual void resetModel() = 0;
    };

}

#endif
