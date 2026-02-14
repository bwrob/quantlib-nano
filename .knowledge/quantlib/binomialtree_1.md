alJumpsBinomialTree<CoxRossRubinstein> {
      public:
        CoxRossRubinstein(const ext::shared_ptr<StochasticProcess1D>&,
                          Time end,
                          Size steps,
                          Real strike);
    };


    //! Additive equal probabilities binomial tree
    /*! \ingroup lattices */
    class AdditiveEQPBinomialTree
        : public EqualProbabilitiesBinomialTree<AdditiveEQPBinomialTree> {
      public:
        AdditiveEQPBinomialTree(
                        const ext::shared_ptr<StochasticProcess1D>&,
                        Time end,
                        Size steps,
                        Real strike);
    };


    //! %Trigeorgis (additive equal jumps) binomial tree
    /*! \ingroup lattices */
    class Trigeorgis : public EqualJumpsBinomialTree<Trigeorgis> {
      public:
        Trigeorgis(const ext::shared_ptr<StochasticProcess1D>&,
                   Time end,
                   Size steps,
                   Real strike);
    };


    //! %Tian tree: third moment matching, multiplicative approach
    /*! \ingroup lattices */
    class Tian : public BinomialTree<Tian> {
      public:
        Tian(const ext::shared_ptr<StochasticProcess1D>&,
             Time end,
             Size steps,
             Real strike);
        Real underlying(Size i, Size index) const {
            return x0_ * std::pow(down_, Real(BigInteger(i)-BigInteger(index)))
                       * std::pow(up_, Real(index));
        };
        Real probability(Size, Size, Size branch) const {
            return (branch == 1 ? pu_ : pd_);
        }
      protected:
        Real up_, down_, pu_, pd_;
    };

    //! Leisen & Reimer tree: multiplicative approach
    /*! \ingroup lattices */
    class LeisenReimer : public BinomialTree<LeisenReimer> {
      public:
        LeisenReimer(const ext::shared_ptr<StochasticProcess1D>&,
                     Time end,
                     Size steps,
                     Real strike);
        Real underlying(Size i, Size index) const {
            return x0_ * std::pow(down_, Real(BigInteger(i)-BigInteger(index)))
                       * std::pow(up_, Real(index));
        }
        Real probability(Size, Size, Size branch) const {
            return (branch == 1 ? pu_ : pd_);
        }
      protected:
        Real up_, down_, pu_, pd_;
    };


     class Joshi4 : public BinomialTree<Joshi4> {
      public:
        Joshi4(const ext::shared_ptr<StochasticProcess1D>&,
               Time end,
               Size steps,
               Real strike);
        Real underlying(Size i, Size index) const {
            return x0_ * std::pow(down_, Real(BigInteger(i)-BigInteger(index)))
                       * std::pow(up_, Real(index));
        }
        Real probability(Size, Size, Size branch) const {
            return (branch == 1 ? pu_ : pd_);
        }
      protected:
        Real computeUpProb(Real k, Real dj) const;
        Real up_, down_, pu_, pd_;
    };


}


#endif
