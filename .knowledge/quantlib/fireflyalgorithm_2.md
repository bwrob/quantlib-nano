 delta_;
        }
        void init(FireflyAlgorithm* fa) override {
            FireflyAlgorithm::RandomWalk::init(fa);
            walkRandom_.setDimension(N_, *lX_, *uX_);
        }
        IsotropicRandomWalk<Distribution, std::mt19937> walkRandom_;
        Real delta_;
    };
    
    //! Gaussian Walk
    /*  Gaussian random walk
    */
    class GaussianWalk : public DistributionRandomWalk<std::normal_distribution<QuantLib::Real>> {
      public:
        explicit GaussianWalk(Real sigma, 
                              Real delta = 0.9, 
                              unsigned long seed = SeedGenerator::instance().get())
        : DistributionRandomWalk<std::normal_distribution<QuantLib::Real>>(
                           std::normal_distribution<QuantLib::Real>(0.0, sigma), delta, seed){}
    };

    //! Levy Flight Random Walk
    /*  Levy flight random walk
    */
    class LevyFlightWalk : public DistributionRandomWalk<LevyFlightDistribution> {
      public:
        explicit LevyFlightWalk(Real alpha, 
                                Real xm = 0.5, 
                                Real delta = 0.9,
                                unsigned long seed = SeedGenerator::instance().get())
        : DistributionRandomWalk<LevyFlightDistribution>(
                            LevyFlightDistribution(xm, alpha), delta, seed) {}
    };

    //! Decreasing Random Walk
    /*  Gaussian random walk, but size of step decreases with each iteration step
    */
    class DecreasingGaussianWalk : public GaussianWalk {
      public:
        explicit DecreasingGaussianWalk(
            Real sigma,
            Real delta = 0.9,
            unsigned long seed = SeedGenerator::instance().get())
        : GaussianWalk(sigma, delta, seed), delta0_(delta) {}
      protected:
        void walkImpl(Array& xRW) override {
            iteration_++;
            if (iteration_ > Mfa_) {
                //Every time all the fireflies have been processed
                //multiply delta by itself
                iteration_ = 0;
                delta_ *= delta_;
            }
            GaussianWalk::walkImpl(xRW);
        }
        void init(FireflyAlgorithm* fa) override {
            GaussianWalk::init(fa);
            iteration_ = 0;
            delta_ = delta0_;
        }

      private:
        Real delta0_;
        Size iteration_;
    };
}

#endif