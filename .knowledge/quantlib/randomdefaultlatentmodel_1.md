ut of the cpu heavily and it
    might be possible to get performance out of that.
    \todo: parallelize the statistics computation, things like Var/ESF splits
    are very expensive.
    \todo: consider another design, taking the statistics outside the models.
    */
    template<template <class, class> class derivedRandomLM, class copulaPolicy,
        class USNG = SobolRsg>
    class RandomLM : public virtual LazyObject,
                     public virtual DefaultLossModel {
    private:
        // Takes the parents type, all children have the same type, the
        // random generation is performed in this class only.
        typedef typename LatentModel<copulaPolicy>::template FactorSampler<USNG>
            copulaRNG_type;
    protected:
      RandomLM(Size numFactors, Size numLMVars, copulaPolicy copula, Size nSims, BigNatural seed)
      : seed_(seed), numFactors_(numFactors), numLMVars_(numLMVars), nSims_(nSims),
        copula_(std::move(copula)) {}

      void update() override {
          simsBuffer_.clear();
          // tell basket to notify instruments, etc, we are invalid
          if (!basket_.empty())
              basket_->notifyObservers();
          LazyObject::update();
        }

        void performCalculations() const override {
            static_cast<const derivedRandomLM<copulaPolicy, USNG>* >(
                this)->initDates();//in update?
            copulasRng_ = ext::make_shared<copulaRNG_type>(copula_, seed_);
            performSimulations();
        }

        void performSimulations() const {
            // Next sequence should determine the event and push it into buffer
            for (Size i = nSims_; i != 0U; i--) {
                const std::vector<Real>& sample =
                    copulasRng_->nextSequence().value;
                static_cast<const derivedRandomLM<copulaPolicy, USNG>* >(
                    this)->nextSample(sample);
            // alternatively make call an explicit local method...
            }
        }

        /* Method to access simulation results and avoiding a copy of
        each thread results buffer. PerformCalculations should have been called.
        Here in the monothread version this method is redundant/trivial but
        serves to detach the statistics access to the way the simulations are
        stored.
        */
        const std::vector<simEvent<derivedRandomLM<copulaPolicy, USNG> > >&
            getSim(const Size iSim) const { return simsBuffer_[iSim]; }

        /* Allows statistics to be written generically for fixed and random
        recovery rates. */
        Real getEventRecovery(
            const simEvent<derivedRandomLM<copulaPolicy, USNG> >& evt) const
        {
            return static_cast<const derivedRandomLM<copulaPolicy, USNG>* >(
                this)->getEventRecovery(evt);
        }

        //! \name Statistics, DefaultLossModel interface.
        // These are virtual and allow for children-specific optimization and
        //   variance reduction. The virtual table is ok, they are not part
        //   of the simulation.
        //@{
        /*! Returns the probaility of having a given or larger number of
        defaults in the basket portfolio at a given time.
        */
        Probability probAtLeastNEvents(Size n, const Date& d) const override;
        /*! Order of results refers to the simulated (super)pool not the
        basket's pool.
        Notice that this statistic suffers from heavy dispersion. To see
        techniques to improve it (not implemented here) see:
        Joshi, M., D. Kainth. 2004. Rapid and accurate development of prices
        and Greeks for nth to default credit swaps in the Li model. Quantitative
        Finance, Vol. 4. Institute of Physics Publishing, London, UK, 266-275
        and:
        Chen, Z., Glasserman, P. 'Fast pricing of basket default swaps' in
        Operations Research Vol. 56, No. 2, March/April 2008, pp. 286-303
        */
        std::vector<Probability> probsBeingN
