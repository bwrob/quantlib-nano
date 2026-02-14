   }
        }

      private:
        Real c0_, threshold_;
        Size M_;
        MersenneTwisterUniformRng rng_;
    };

    //! Decreasing Inertia
    /*     Inertia value gets decreased every iteration until it reaches
    a value of threshold when iteration reaches the maximum level
    */
    class DecreasingInertia : public ParticleSwarmOptimization::Inertia {
      public:
        DecreasingInertia(Real threshold = 0.5)
            : threshold_(threshold) {
            QL_REQUIRE(threshold_ >= 0.0 && threshold_ < 1.0, "Threshold must be a Real in [0, 1)");
        }
        void setSize(Size M, Size N, Real c0, const EndCriteria& endCriteria) override {
            N_ = N;
            c0_ = c0;
            iteration_ = 0;
            maxIterations_ = endCriteria.maxIterations();
        }
        void setValues() override {
            Real c0 = c0_*(threshold_ + (1.0 - threshold_)*(maxIterations_ - iteration_) / maxIterations_);
            for (Size i = 0; i < M_; i++) {
                (*V_)[i] *= c0;
            }
        }

      private:
        Real c0_, threshold_;
        Size M_, N_, maxIterations_, iteration_;
    };

    //! AdaptiveInertia
    /*    Alen Lukic, Approximating Kinetic Parameters Using Particle
    Swarm Optimization.
    */
    class AdaptiveInertia : public ParticleSwarmOptimization::Inertia {
      public:
        AdaptiveInertia(Real minInertia, Real maxInertia, Size sh = 5, Size sl = 2)
            :minInertia_(minInertia), maxInertia_(maxInertia),
            sh_(sh), sl_(sl) {};
        void setSize(Size M, Size N, Real c0, const EndCriteria& endCriteria) override {
            M_ = M;
            c0_ = c0;
            adaptiveCounter = 0;
            best_ = QL_MAX_REAL;
            started_ = false;
        }
        void setValues() override;

      private:
        Real c0_, best_;
        Real minInertia_, maxInertia_;
        Size M_;
        Size sh_, sl_;
        Size adaptiveCounter;
        bool started_;
    };

    //! Levy Flight Inertia
    /*    As long as the particle keeps getting frequent updates to its
    personal best value, the inertia behaves like a SimpleRandomInertia,
    but after a number of iterations without improvement, the behaviour
    changes to that of a Levy flight ~ u^{-1/\alpha}
    */
    class LevyFlightInertia : public ParticleSwarmOptimization::Inertia {
      public:
        LevyFlightInertia(Real alpha, Size threshold,
                          unsigned long seed = SeedGenerator::instance().get())
            :rng_(seed), generator_(seed), flight_(generator_, LevyFlightDistribution(1.0, alpha),
                1, Array(1, 1.0), seed),
            threshold_(threshold) {};
        void setSize(Size M, Size N, Real c0, const EndCriteria& endCriteria) override {
            M_ = M;
            N_ = N;
            c0_ = c0;
            adaptiveCounter_ = std::vector<Size>(M_, 0);
        }
        void setValues() override {
            for (Size i = 0; i < M_; i++) {
                if ((*pBF_)[i] < personalBestF_[i]) {
                    personalBestF_[i] = (*pBF_)[i];
                    adaptiveCounter_[i] = 0;
                }
                else {
                    adaptiveCounter_[i]++;
                }
                if (adaptiveCounter_[i] <= threshold_) {
                    //Simple Random Inertia
                    (*V_)[i] *= c0_*(0.5 + 0.5*rng_.nextReal());
                }
                else {
                    //If particle has not found a new personal best after threshold_ iterations
                    //then trigger a Levy flight pattern for the speed
                    flight_.nextReal<Real *>(&(*V_)[i][0]);
                }
            }
        }

      protected:
        void init(ParticleSwarmOptimization* pso) override {
            ParticleSwarmOptimization::Inertia::init(pso);
            personalBestF_ = *pBF_;
            flight_.setDimension(N_, *lX_, *uX_);
        }

      private:
        Mersenne
