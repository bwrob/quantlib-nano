 factors in the latent model according
            to the given copula as random sequence. The default implementation
            given uses the inversion in the copula policy (which must be
            present).
            USNG is expected to be a uniform sequence generator in the default
            implementation.
        */
        /*
            Several (very different) usages make the spez non trivial
            The final goal is to obtain a sequence generator of the factor
            samples, several routes are possible depending on the algorithms:

            1.- URNG -> Sequence Gen -> CopulaInversion
              e.g.: CopulaInversion(RandomSequenceGenerator<MersenneTwisterRNG>)
            2.- PseudoRSG ------------> CopulaInversion
              e.g.: CopulaInversion(SobolRSG)
            3.- URNG -> SpecificMapping -> Sequence Gen  (bypasses the copula
                for performance)
              e.g.: RandomSequenceGenerator<BoxMullerGaussianRng<
                MersenneTwisterRNG> >

            Notice that the order the three algorithms involved (uniform gen,
            sequence construction, distribution mapping) is not always the same.
            (in fact there could be some other ways to generate but these are
            the ones in the library now.)
            Difficulties arise when wanting to use situation 3.- whith a generic
            RNG, leaving it unspecified

            Derived classes might specialize (on the copula
            type) to another type of generator if a more efficient algorithm
            that the distribution inversion is available; rewritig then the
            nextSequence method for a particular copula implementation.
            Some combinations of generators might make no sense, while it
            could be possible to block template classes corresponding to those
            cases its not done (yet?) (e.g. a BoxMuller under a TCopula.)
            Dimensionality coherence (between the generator and the copula)
            should have been checked by the client code.
            In multithread usage the sequence generator is expect to be already
            in position.
            To sample the latent variable itself users should call
            LatentModel::latentVarValue with these samples.
        */
        // Cant use InverseCumulativeRsg since the inverse there has to return a
        //   real number and here a vector is needed, the function inverted here
        //   is multivalued.
        template <class USNG,
            // dummy template parameter to allow for 'full' specialization of
            // inner class without specialization of the outer.
            bool = true>
        class FactorSampler {
        public:
            typedef Sample<std::vector<Real> > sample_type;
            explicit FactorSampler(const copulaType& copula,
                BigNatural seed = 0)
            : sequenceGen_(copula.numFactors(), seed), // base case construction
              x_(std::vector<Real>(copula.numFactors()), 1.0),
              copula_(copula) { }
            /*! Returns a sample of the factor set \f$ M_k\,Z_i\f$.
            This method has the vocation of being specialized at particular
            types of the copula with a more efficient inversion to generate the
            random variables modelled (e.g. Box-Muller for a gaussian).
            Here a default implementation is provided based directly on the
            inversion of the cumulative distribution from the copula.
            Care has to be taken in potential specializations that the generator
            algorithm is compatible with an eventual concurrence of the
            simulations.
             */
            const sample_type& nextSequence() const {
                typename USNG::sample_type sample =
                    sequenceGen_.nextSequence();
                x_.value = copula_.allFactorCumulInverter(sample.va
