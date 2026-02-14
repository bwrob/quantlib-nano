 excessProbability_; }
    private:
        Size nBuckets_;
        Real maximum_;
        mutable Real volume_;
        mutable Size n_;
        mutable std::vector<Real> probability_;
        mutable std::vector<Real> excessProbability_;
    };

    //! Loss Distribution for Homogeneous Pool
    /*! Loss Distribution for Homogeneous Pool

      Loss distribution for equal volumes but varying probabilities of 
      default.

      The method builds the exact loss distribution for a homogeneous pool
      of underlyings iteratively by computing the convolution of the given
      loss distribution with the "loss distribution" of an additional credit
      following 
      
      Xiaofong Ma, "Numerical Methods for the Valuation of Synthetic
      Collateralized Debt Obligations", PhD Thesis, 
      Graduate Department of Computer Science, University of Toronto, 2007  
      http://www.cs.toronto.edu/pub/reports/na/ma-07-phd.pdf (formula 2.1)

      avoiding numerical instability of the algorithm by

      John Hull and Alan White, "Valuation of a CDO and nth to default CDS 
      without Monte Carlo simulation", Journal of Derivatives 12, 2, 2004 
     */
    class LossDistHomogeneous : public LossDist {
    public:
      LossDistHomogeneous(Size nBuckets, Real maximum) : nBuckets_(nBuckets), maximum_(maximum) {}
      Distribution operator()(Real volume, const std::vector<Real>& probabilities) const;
      Distribution operator()(const std::vector<Real>& volumes,
                              const std::vector<Real>& probabilities) const override;
      Size buckets() const override { return nBuckets_; }
      Real maximum() const override { return maximum_; }
      Size size() const { return n_; }
      Real volume() const { return volume_; }
      std::vector<Real> probability() const { return probability_; }
      std::vector<Real> excessProbability() const { return excessProbability_; }
    private:
        Size nBuckets_;
        Real maximum_;
        mutable Size n_ = 0;
        mutable Real volume_ = 0.0;
        mutable std::vector<Real> probability_;
        mutable std::vector<Real> excessProbability_;
    };

    //! Loss distribution with Hull-White bucketing 
    /*! Loss distribution with Hull-White bucketing 

      Loss distribution for varying volumes and probabilities of default, 
      independence assumed.

      The implementation of the loss distribution follows 

      John Hull and Alan White, "Valuation of a CDO and nth to default CDS 
      without Monte Carlo simulation", Journal of Derivatives 12, 2, 2004. 
    */
    class LossDistBucketing : public LossDist {
    public:
        LossDistBucketing (Size nBuckets, Real maximum, 
                           Real epsilon = 1e-6)
            : nBuckets_(nBuckets), maximum_(maximum), epsilon_(epsilon) {}
        Distribution operator()(const std::vector<Real>& volumes,
                                const std::vector<Real>& probabilities) const override;
        Size buckets() const override { return nBuckets_; }
        Real maximum() const override { return maximum_; }

      private:
        int locateTargetBucket (Real loss, Size i0 = 0) const;

        Size nBuckets_;
        Real maximum_;
        Real epsilon_;
    };

    //! Loss distribution with Monte Carlo simulation
    /*!
      Loss distribution for varying volumes and probabilities of default
      via Monte Carlo simulation of independent default events.
    */
    class LossDistMonteCarlo : public LossDist {
    public:
        LossDistMonteCarlo (Size nBuckets, Real maximum, Size simulations,
                            long seed = 42, Real epsilon = 1e-6)
            : nBuckets_(nBuckets), maximum_(maximum), 
              simulations_(simulations), seed_(seed), epsilon_(epsilon) {}
        Distribution operator()(const std::vector<Real>& volumes,
                                const std::vector<Real>& probabilities) const override;
        Size buckets() const override { return n