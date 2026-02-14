            GaussianRandomDefaultLM;
    */
    /* Uses BoxMuller for gaussian generation, bypassing copula inversions
    typedef RandomDefaultLM<GaussianCopulaPolicy, RandomSequenceGenerator<
        BoxMullerGaussianRng<MersenneTwisterUniformRng> > >
            GaussianRandomDefaultLM;
    */
    /* Default case, uses the copula inversion directly and sobol sequence */
    typedef RandomDefaultLM<GaussianCopulaPolicy> GaussianRandomDefaultLM;

    // ---------- T default generators options ----------------------------
    /* Uses copula inversion and MT base generation
    typedef RandomDefaultLM<TCopulaPolicy,
      RandomSequenceGenerator<MersenneTwisterUniformRng> > TRandomDefaultLM;
    */
    /* Uses MT and polar direct strudent-T generation
    typedef RandomDefaultLM<TCopulaPolicy,
        RandomSequenceGenerator<PolarStudentTRng<MersenneTwisterUniformRng> > >
            TRandomDefaultLM;
    */
    /* Default case, uses sobol sequence and copula inversion */
    typedef RandomDefaultLM<TCopulaPolicy> TRandomDefaultLM;

}

#endif
