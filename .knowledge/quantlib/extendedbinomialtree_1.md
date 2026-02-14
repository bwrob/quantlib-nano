this->x0_*std::exp(j*this->dxStep(stepTime));
        }

        Real probability(Size i, Size, Size branch) const {
            Time stepTime = i*this->dt_;
            Real upProb = this->probUp(stepTime);
            Real downProb = 1 - upProb;
            return (branch == 1 ? upProb : downProb);
        }
      protected:
        //probability of a up move
        virtual Real probUp(Time stepTime) const = 0;
        //time dependent term dx_
        virtual Real dxStep(Time stepTime) const = 0;

        Real dx_, pu_, pd_;
    };


    //! Jarrow-Rudd (multiplicative) equal probabilities binomial tree
    /*! \ingroup lattices */
    class ExtendedJarrowRudd
        : public ExtendedEqualProbabilitiesBinomialTree<ExtendedJarrowRudd> {
      public:
        ExtendedJarrowRudd(const ext::shared_ptr<StochasticProcess1D>&,
                           Time end,
                           Size steps,
                           Real strike);
      protected:
        Real upStep(Time stepTime) const override;
    };


    //! Cox-Ross-Rubinstein (multiplicative) equal jumps binomial tree
    /*! \ingroup lattices */
    class ExtendedCoxRossRubinstein
        : public ExtendedEqualJumpsBinomialTree<ExtendedCoxRossRubinstein> {
      public:
        ExtendedCoxRossRubinstein(const ext::shared_ptr<StochasticProcess1D>&,
                                  Time end,
                                  Size steps,
                                  Real strike);
      protected:
        Real dxStep(Time stepTime) const override;
        Real probUp(Time stepTime) const override;
    };


    //! Additive equal probabilities binomial tree
    /*! \ingroup lattices */
    class ExtendedAdditiveEQPBinomialTree
        : public ExtendedEqualProbabilitiesBinomialTree<
                                            ExtendedAdditiveEQPBinomialTree> {
      public:
        ExtendedAdditiveEQPBinomialTree(
                        const ext::shared_ptr<StochasticProcess1D>&,
                        Time end,
                        Size steps,
                        Real strike);

      protected:
        Real upStep(Time stepTime) const override;
    };


    //! %Trigeorgis (additive equal jumps) binomial tree
    /*! \ingroup lattices */
    class ExtendedTrigeorgis
        : public ExtendedEqualJumpsBinomialTree<ExtendedTrigeorgis> {
      public:
        ExtendedTrigeorgis(const ext::shared_ptr<StochasticProcess1D>&,
                           Time end,
                           Size steps,
                           Real strike);
    protected:
      Real dxStep(Time stepTime) const override;
      Real probUp(Time stepTime) const override;
    };


    //! %Tian tree: third moment matching, multiplicative approach
    /*! \ingroup lattices */
    class ExtendedTian : public ExtendedBinomialTree<ExtendedTian> {
      public:
        ExtendedTian(const ext::shared_ptr<StochasticProcess1D>&,
                     Time end,
                     Size steps,
                     Real strike);

        Real underlying(Size i, Size index) const;
        Real probability(Size, Size, Size branch) const;
      protected:
        Real up_, down_, pu_, pd_;
    };

    //! Leisen & Reimer tree: multiplicative approach
    /*! \ingroup lattices */
    class ExtendedLeisenReimer
        : public ExtendedBinomialTree<ExtendedLeisenReimer> {
      public:
        ExtendedLeisenReimer(const ext::shared_ptr<StochasticProcess1D>&,
                             Time end,
                             Size steps,
                             Real strike);

        Real underlying(Size i, Size index) const;
        Real probability(Size, Size, Size branch) const;
      protected:
        Time end_;
        Size oddSteps_;
        Real strike_, up_, down_, pu_, pd_;
    };


     class ExtendedJoshi4 : public ExtendedBinomialTree<ExtendedJoshi4> {
      public:
        ExtendedJoshi4(const ext::shared_ptr<StochasticProcess1D>&,
                       Time end,
        