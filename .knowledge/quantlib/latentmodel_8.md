Variables),
      copula_(factorWeights_, ini)
    { }

    template <class Impl>
    LatentModel<Impl>::LatentModel(
        const Handle<Quote>& singleFactorCorrel,
        Size nVariables,
        const typename Impl::initTraits& ini)
    : factorWeights_(nVariables, std::vector<Real>(1,
        std::sqrt(singleFactorCorrel->value()))),
      cachedMktFactor_(singleFactorCorrel),
      idiosyncFctrs_(nVariables,
        std::sqrt(1.-singleFactorCorrel->value())),
      nFactors_(1),
      nVariables_(nVariables),
      copula_(factorWeights_, ini)
    {
        registerWith(cachedMktFactor_);
    }

#endif

    template <class Impl>
    void LatentModel<Impl>::update() {
        /* only registration with the single market correl quote. If we get
        register with something else remember that the quote stores correlation
        and the model need factor values; which for one factor models are the
        square root of the correlation.
        */
        factorWeights_ = std::vector<std::vector<Real> >(nVariables_,
            std::vector<Real>(1, std::sqrt(cachedMktFactor_->value())));
        idiosyncFctrs_ = std::vector<Real>(nVariables_,
            std::sqrt(1.-cachedMktFactor_->value()));
        copula_ = copulaType(factorWeights_, copula_.getInitTraits());
        notifyObservers();
    }

#ifndef __DOXYGEN__

    //----Template partial specializations of the random FactorSampler--------
    /*
    Notice that while the default template needs a sequence generator the
    specializations need a number generator. This is forced at the time the
    concrete policy class is used in the template parameter, if it has been
    specialized it needs the sample type typedef to match at compilation.

    Notice here the outer class template is specialized only, leaving the inner
    generator still a class template. Apparently old versions of gcc (3.x) bug
    on this one not recognizing the specialization.
    */
    /*! \brief  Specialization for direct Gaussian Box-Muller generation.\par
    The implementation of Box-Muller in the library is the rejection variant so
    do not use it within a multithreaded simulation.
    */
    template<class TC> template<class URNG, bool dummy>
    class LatentModel<TC>
        ::FactorSampler <RandomSequenceGenerator<BoxMullerGaussianRng<URNG> > ,
            dummy> {
        typedef URNG urng_type;
    public:
        //Size below must be == to the numb of factors idiosy + systemi
        typedef Sample<std::vector<Real> > sample_type;
        explicit FactorSampler(const GaussianCopulaPolicy& copula,
                               BigNatural seed = 0)
        : boxMullRng_(copula.numFactors(),
            BoxMullerGaussianRng<urng_type>(urng_type(seed))){ }
        const sample_type& nextSequence() const {
                return boxMullRng_.nextSequence();
        }
    private:
        RandomSequenceGenerator<BoxMullerGaussianRng<urng_type> > boxMullRng_;
    };

    /*! \brief Specialization for direct T samples generation.\par
    The PolarT is a rejection algorithm so do not use it within a
    multithreaded simulation.
    The RandomSequenceGenerator class does not admit heterogeneous
    distribution samples so theres a trick here since the template parameter is
    not what it is used internally.
    */
    template<class TC> template<class URNG, bool dummy>//uniform number expected
    class LatentModel<TC>
        ::FactorSampler<RandomSequenceGenerator<PolarStudentTRng<URNG> > ,
            dummy> {
        typedef URNG urng_type;
    public:
        typedef Sample<std::vector<Real> > sample_type;
        explicit FactorSampler(const TCopulaPolicy& copula, BigNatural seed = 0)
        : sequence_(std::vector<Real> (copula.numFactors()), 1.0),
          urng_(seed) {
            // 1 == urng.dimension() is enforced by the sample type
            const std::vector<Real>& varF = copula.varianceFactors();
            for (Real i : varF) // ...use back ins
