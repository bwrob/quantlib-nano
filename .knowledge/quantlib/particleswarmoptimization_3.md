TwisterUniformRng rng_;
        std::mt19937 generator_;
        IsotropicRandomWalk<LevyFlightDistribution, std::mt19937> flight_;
        Array personalBestF_;
        std::vector<Size> adaptiveCounter_;
        Real c0_;
        Size M_, N_;
        Size threshold_;
    };

    //! Base topology class used to determine the personal and global best
    /*! This pure virtual base class provides the access to the PSO state
    which the particular topology algorithm will change upon each iteration.
    */
    class ParticleSwarmOptimization::Topology {
        friend class ParticleSwarmOptimization;
      public:
        virtual ~Topology() = default;
        //! initialize state for current problem
        virtual void setSize(Size M) = 0;
        //! produce changes to PSO state for current iteration
        virtual void findSocialBest() = 0;
      protected:
        ParticleSwarmOptimization *pso_;
        std::vector<Array> *X_, *V_, *pBX_, *gBX_;
        Array *pBF_, *gBF_;
      private:
        void init(ParticleSwarmOptimization *pso) {
            pso_ = pso;
            X_ = &pso_->X_;
            V_ = &pso_->V_;
            pBX_ = &pso_->pBX_;
            gBX_ = &pso_->gBX_;
            pBF_ = &pso_->pBF_;
            gBF_ = &pso_->gBF_;
        }
    };

    //! Global Topology
    /*  The global best as seen by each particle is the best from amongst
    all particles
    */
    class GlobalTopology : public ParticleSwarmOptimization::Topology {
      public:
        void setSize(Size M) override { M_ = M; }
        void findSocialBest() override {
            Real bestF = (*pBF_)[0];
            Size bestP = 0;
            for (Size i = 1; i < M_; i++) {
                if (bestF < (*pBF_)[i]) {
                    bestF = (*pBF_)[i];
                    bestP = i;
                }
            }
            Array& x = (*pBX_)[bestP];
            for (Size i = 0; i < M_; i++) {
                if (i != bestP) {
                    (*gBX_)[i] = x;
                    (*gBF_)[i] = bestF;
                }
            }
        }

      private:
        Size M_;
    };

    //! K-Neighbor Topology
    /*  The global best as seen by each particle is the best from amongst
    the previous K and next K neighbors. For particle I, the best is
    then taken from amongst the [I - K, I + K] particles.
    */
    class KNeighbors : public ParticleSwarmOptimization::Topology {
      public:
        KNeighbors(Size K = 1) :K_(K) {
            QL_REQUIRE(K > 0, "Neighbors need to be larger than 0");
        }
        void setSize(Size M) override {
            M_ = M;
            QL_ENSURE(K_ < M, "Number of neighbors need to be smaller than total particles in swarm");
        }
        void findSocialBest() override;

      private:
        Size K_, M_;
    };

    //! Clubs Topology
    /*  H.M. Emara,  Adaptive Clubs-based Particle Swarm Optimization
    Each particle is originally assigned to a default number of clubs
    from among the total set. The best as seen by each particle is the
    best from amongst the clubs to which the particle belongs.
    Underperforming particles join more clubs randomly (up to a maximum
    number) to widen the particles that influence them, while
    overperforming particles leave clubs randomly (down to a minimum
    number) to avoid early convergence to local minima.
    */
    class ClubsTopology : public ParticleSwarmOptimization::Topology {
      public:
        ClubsTopology(Size defaultClubs, Size totalClubs,
            Size maxClubs, Size minClubs,
            Size resetIteration, unsigned long seed = SeedGenerator::instance().get());
        void setSize(Size M) override;
        void findSocialBest() override;

      private:
        Size totalClubs_, maxClubs_, minClubs_, defaultClubs_;
        Size iteration_ = 0, resetIteration_;
        Size M_;
        std::vector<std::vector<bool> > clubs4particles_;
        std::vector<std::vector<bool> > particles4clubs_;
        std::ve