The optimization stops either because the number of iterations has been reached
    or because the stationary function value limit has been reached.
    */
    class ParticleSwarmOptimization : public OptimizationMethod {
      public:
        class Inertia;
        class Topology;
        ParticleSwarmOptimization(Size M,
                                  ext::shared_ptr<Topology> topology,
                                  ext::shared_ptr<Inertia> inertia,
                                  Real c1 = 2.05,
                                  Real c2 = 2.05,
                                  unsigned long seed = SeedGenerator::instance().get());
        explicit ParticleSwarmOptimization(Size M,
                                           ext::shared_ptr<Topology> topology,
                                           ext::shared_ptr<Inertia> inertia,
                                           Real omega,
                                           Real c1,
                                           Real c2,
                                           unsigned long seed = SeedGenerator::instance().get());
        void startState(Problem &P, const EndCriteria &endCriteria);
        EndCriteria::Type minimize(Problem& P, const EndCriteria& endCriteria) override;

      protected:
        std::vector<Array> X_, V_, pBX_, gBX_;
        Array pBF_, gBF_;
        Array lX_, uX_;
        Size M_, N_;
        Real c0_, c1_, c2_;
        MersenneTwisterUniformRng rng_;
        ext::shared_ptr<Topology> topology_;
        ext::shared_ptr<Inertia> inertia_;
    };

    //! Base inertia class used to alter the PSO state
    /*! This pure virtual base class provides the access to the PSO state
    which the particular inertia algorithm will change upon each iteration.
    */
    class ParticleSwarmOptimization::Inertia {
        friend class ParticleSwarmOptimization;
      public:
        virtual ~Inertia() = default;
        //! initialize state for current problem
        virtual void setSize(Size M, Size N, Real c0, const EndCriteria &endCriteria) = 0;
        //! produce changes to PSO state for current iteration
        virtual void setValues() = 0;
      protected:
        ParticleSwarmOptimization *pso_;
        std::vector<Array> *X_, *V_, *pBX_, *gBX_;
        Array *pBF_, *gBF_;
        Array *lX_, *uX_;

        virtual void init(ParticleSwarmOptimization *pso) {
            pso_ = pso;
            X_ = &pso_->X_;
            V_ = &pso_->V_;
            pBX_ = &pso_->pBX_;
            gBX_ = &pso_->gBX_;
            pBF_ = &pso_->pBF_;
            gBF_ = &pso_->gBF_;
            lX_ = &pso_->lX_;
            uX_ = &pso_->uX_;
        }
    };

    //! Trivial Inertia
    /*     Inertia is a static value
    */
    class TrivialInertia : public ParticleSwarmOptimization::Inertia {
      public:
        void setSize(Size M, Size N, Real c0, const EndCriteria& endCriteria) override {
            c0_ = c0;
            M_ = M;
        }
        void setValues() override {
            for (Size i = 0; i < M_; i++) {
                (*V_)[i] *= c0_;
            }
        }

      private:
        Real c0_;
        Size M_;
    };

    //! Simple Random Inertia
    /*     Inertia value gets multiplied with a random number
    between (threshold, 1)
    */
    class SimpleRandomInertia : public ParticleSwarmOptimization::Inertia {
      public:
        SimpleRandomInertia(Real threshold = 0.5, unsigned long seed = SeedGenerator::instance().get())
            : threshold_(threshold), rng_(seed) {
            QL_REQUIRE(threshold_ >= 0.0 && threshold_ < 1.0, "Threshold must be a Real in [0, 1)");
        }
        void setSize(Size M, Size N, Real c0, const EndCriteria& endCriteria) override {
            M_ = M;
            c0_ = c0;
        }
        void setValues() override {
            for (Size i = 0; i < M_; i++) {
                Real val = c0_*(threshold_ + (1.0 - threshold_)*rng_.nextReal());
                (*V_)[i] *= val;
         