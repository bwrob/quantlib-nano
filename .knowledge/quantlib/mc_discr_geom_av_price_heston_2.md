is->arguments_.pastFixings));
    }

    template <class RNG, class S, class P>
    inline MakeMCDiscreteGeometricAPHestonEngine<RNG, S, P>::MakeMCDiscreteGeometricAPHestonEngine(
        ext::shared_ptr<P> process)
    : process_(std::move(process)), samples_(Null<Size>()), maxSamples_(Null<Size>()),
      steps_(Null<Size>()), stepsPerYear_(Null<Size>()), tolerance_(Null<Real>()) {}

    template<class RNG, class S, class P>
    inline MakeMCDiscreteGeometricAPHestonEngine<RNG,S,P>&
    MakeMCDiscreteGeometricAPHestonEngine<RNG,S,P>::withSamples(Size samples) {
        QL_REQUIRE(tolerance_ == Null<Real>(),
                   "tolerance already set");
        samples_ = samples;
        return *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCDiscreteGeometricAPHestonEngine<RNG,S,P>&
    MakeMCDiscreteGeometricAPHestonEngine<RNG,S,P>::withAbsoluteTolerance(
                                                             Real tolerance) {
        QL_REQUIRE(samples_ == Null<Size>(),
                   "number of samples already set");
        QL_REQUIRE(RNG::allowsErrorEstimate,
                   "chosen random generator policy "
                   "does not allow an error estimate");
        tolerance_ = tolerance;
        return *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCDiscreteGeometricAPHestonEngine<RNG,S,P>&
    MakeMCDiscreteGeometricAPHestonEngine<RNG,S,P>::withMaxSamples(Size samples) {
        maxSamples_ = samples;
        return *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCDiscreteGeometricAPHestonEngine<RNG,S,P>&
    MakeMCDiscreteGeometricAPHestonEngine<RNG,S,P>::withSeed(BigNatural seed) {
        seed_ = seed;
        return *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCDiscreteGeometricAPHestonEngine<RNG,S,P>&
    MakeMCDiscreteGeometricAPHestonEngine<RNG,S,P>::withAntitheticVariate(bool b) {
        antithetic_ = b;
        return *this;
    }

    template<class RNG, class S, class P>
    inline MakeMCDiscreteGeometricAPHestonEngine<RNG,S,P>&
    MakeMCDiscreteGeometricAPHestonEngine<RNG,S,P>::withSteps(Size steps) {
        QL_REQUIRE(stepsPerYear_ == Null<Size>(),
                   "number of steps per year already set");
        steps_ = steps;
        return *this;
    }

    template<class RNG, class S, class P>
    inline MakeMCDiscreteGeometricAPHestonEngine<RNG,S,P>&
    MakeMCDiscreteGeometricAPHestonEngine<RNG,S,P>::withStepsPerYear(Size steps) {
        QL_REQUIRE(steps_ == Null<Size>(),
                   "number of steps already set");
        stepsPerYear_ = steps;
        return *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCDiscreteGeometricAPHestonEngine<RNG,S,P>::operator ext::shared_ptr<PricingEngine>() const {
        return ext::shared_ptr<PricingEngine>(new
            MCDiscreteGeometricAPHestonEngine<RNG,S,P>(process_,
                                                       antithetic_,
                                                       samples_,
                                                       tolerance_,
                                                       maxSamples_,
                                                       seed_,
                                                       steps_,
                                                       stepsPerYear_));
    }
}

#endif
