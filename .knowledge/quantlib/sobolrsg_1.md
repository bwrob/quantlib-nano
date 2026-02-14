better
        two-dimensional projections, preprint Nov 22 2007

        See http://web.maths.unsw.edu.au/~fkuo/sobol/ for more information.

        The Joe-Kuo numbers are available under a BSD-style license
        available at the above link.

        Note that the Kuo numbers were generated to work with a
        different ordering of primitive polynomials for the first 40
        or so dimensions which is why we have the Alternative
        Primitive Polynomials.

        \test
        - the correctness of the returned values is tested by
          reproducing known good values.
        - the correctness of the returned values is tested by checking
          their discrepancy against known good values.
    */
    class SobolRsg {
      public:
        typedef Sample<std::vector<Real> > sample_type;
        enum DirectionIntegers {
            Unit, Jaeckel, SobolLevitan, SobolLevitanLemieux,
            JoeKuoD5, JoeKuoD6, JoeKuoD7,
            Kuo, Kuo2, Kuo3 };
        /*! The so called generating integer is chosen to be \f$\gamma(n) = n\f$ if useGrayCode is set to false and
            \f$\gamma(n) = G(n)\f$ where \f$G(n)\f$ is the Gray code of \f$n\f$ otherwise. The Sobol integers are then
            constructed using formula 8.20 resp. 8.23, see "Monte Carlo Methods in Finance" by Peter Jäckel. The default
            is to use the Gray code since this allows a faster sequence generation. The Burley2020SobolRsg relies on an
            underlying SobolRsg not using the Gray code on the other hand due to its specific way of constructing the
            integer sequence.

            \pre dimensionality must be <= PPMT_MAX_DIM
         */
        explicit SobolRsg(Size dimensionality,
                          unsigned long seed = 0,
                          DirectionIntegers directionIntegers = Jaeckel,
                          bool useGrayCode = true);
        /*! skip to the n-th sample in the low-discrepancy sequence */
        const std::vector<std::uint32_t>& skipTo(std::uint32_t n) const;
        const std::vector<std::uint32_t>& nextInt32Sequence() const;

        const SobolRsg::sample_type& nextSequence() const {
            const std::vector<std::uint32_t>& v = nextInt32Sequence();
            // normalize to get a double in (0,1)
            for (Size k = 0; k < dimensionality_; ++k)
                sequence_.value[k] = v[k] * (0.5 / (1UL << 31));
            return sequence_;
        }
        const sample_type& lastSequence() const { return sequence_; }
        Size dimension() const { return dimensionality_; }
      private:
        Size dimensionality_;
        mutable std::uint32_t sequenceCounter_ = 0;
        mutable bool firstDraw_ = true;
        mutable sample_type sequence_;
        mutable std::vector<std::uint32_t> integerSequence_;
        std::vector<std::vector<std::uint32_t>> directionIntegers_;
        bool useGrayCode_;
    };

}

#endif
