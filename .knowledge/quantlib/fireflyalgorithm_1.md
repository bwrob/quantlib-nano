> > values_;
        Array lX_, uX_;
        Real mutation_, crossover_;
        Size M_, N_, Mde_, Mfa_;
        ext::shared_ptr<Intensity> intensity_;
        ext::shared_ptr<RandomWalk> randomWalk_;
        std::mt19937 generator_;
        std::uniform_int_distribution<QuantLib::Size> distribution_;
        MersenneTwisterUniformRng rng_;
    };

    //! Base intensity class
    /*! Derived classes need to implement only intensityImpl
    */
    class FireflyAlgorithm::Intensity {
        friend class FireflyAlgorithm;
    public:
      virtual ~Intensity() = default;
      //! find brightest firefly for each firefly
      void findBrightest();
    protected:
        Size Mfa_, N_;
        const std::vector<Array> *x_;
        const std::vector<std::pair<Real, Size> > *values_;
        std::vector<Array> *xI_;

        virtual Real intensityImpl(Real valueX, Real valueY, Real distance) = 0;
        Real distance(const Array& x, const Array& y) const {
            Real d = 0.0;
            for (Size i = 0; i < N_; i++) {
                Real diff = x[i] - y[i];
                d += diff*diff;
            }
            return d;
        }

    private:
        void init(FireflyAlgorithm *fa) {
            x_ = &fa->x_;
            xI_ = &fa->xI_;
            values_ = &fa->values_;
            Mfa_ = fa->Mfa_;
            N_ = fa->N_;
        }
    };

    //! Exponential Intensity
    /*  Exponentially decreasing intensity
    */
    class ExponentialIntensity : public FireflyAlgorithm::Intensity {
      public:
          ExponentialIntensity(Real beta0, Real betaMin, Real gamma)
              : beta0_(beta0), betaMin_(betaMin), gamma_(gamma) {}
      protected:
        Real intensityImpl(Real valueX, Real valueY, Real d) override {
            return (beta0_ - betaMin_) * std::exp(-gamma_ * d) + betaMin_;
        }
          Real beta0_, betaMin_, gamma_;
    };

    //! Inverse Square Intensity
    /*  Inverse law square
    */
    class InverseLawSquareIntensity : public FireflyAlgorithm::Intensity {
    public:
        InverseLawSquareIntensity(Real beta0, Real betaMin)
            : beta0_(beta0), betaMin_(betaMin) {}
    protected:
      Real intensityImpl(Real valueX, Real valueY, Real d) override {
          return (beta0_ - betaMin_) / (d + QL_EPSILON) + betaMin_;
      }
        Real beta0_, betaMin_;
    };

    //! Base Random Walk class
    /*! Derived classes need to implement only walkImpl
    */
    class FireflyAlgorithm::RandomWalk {
        friend class FireflyAlgorithm;
    public:
      virtual ~RandomWalk() = default;
      //! perform random walk
      void walk() {
          for (Size i = 0; i < Mfa_; i++) {
              walkImpl((*xRW_)[(*values_)[i].second]);
          }
        }
    protected:
        Size Mfa_, N_;
        const std::vector<Array> *x_;
        const std::vector<std::pair<Real, Size> > *values_;
        std::vector<Array> *xRW_;
        Array *lX_, *uX_;

        virtual void walkImpl(Array & xRW) = 0;
        virtual void init(FireflyAlgorithm *fa) {
            x_ = &fa->x_;
            xRW_ = &fa->xRW_;
            values_ = &fa->values_;
            Mfa_ = fa->Mfa_;
            N_ = fa->N_;
            lX_ = &fa->lX_;
            uX_ = &fa->uX_;
        }
    };

    //! Distribution Walk
    /*  Random walk given by distribution template parameter. The
        distribution must be compatible with std::mt19937.
    */
    template <class Distribution>
    class DistributionRandomWalk : public FireflyAlgorithm::RandomWalk {
      public:
        explicit DistributionRandomWalk(Distribution dist,
                                        Real delta = 0.9,
                                        unsigned long seed = SeedGenerator::instance().get())
        : walkRandom_(std::mt19937(seed), std::move(dist), 1, Array(1, 1.0), seed),
          delta_(delta) {}
      protected:
        void walkImpl(Array& xRW) override {
            walkRandom_.nextReal(&xRW[0]);
            xRW *=
