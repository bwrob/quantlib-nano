ion_), 1.0) {

        randomizer_ = prsg_.nextSequence();

    }

    template <class LDS, class PRS>
    RandomizedLDS<LDS, PRS>::RandomizedLDS(Size dimensionality,
                                           BigNatural ldsSeed,
                                           BigNatural prsSeed)
    : ldsg_(dimensionality, ldsSeed), pristineldsg_(dimensionality, ldsSeed),
      prsg_(dimensionality, prsSeed), dimension_(dimensionality),
      x(std::vector<Real> (dimensionality), 1.0), randomizer_(std::vector<Real> (dimensionality), 1.0) {

        randomizer_ = prsg_.nextSequence();
    }

    template <class LDS, class PRS>
    inline const typename RandomizedLDS<LDS, PRS>::sample_type&
    RandomizedLDS<LDS, PRS>::nextSequence() const {
    typename LDS::sample_type sample =
        ldsg_.nextSequence();
    x.weight = randomizer_.weight * sample.weight;
    for (Size i = 0; i < dimension_; i++) {
        x.value[i] =  randomizer_.value[i] + sample.value[i];
        if (x.value[i]>1.0)
            x.value[i] -= 1.0;
    }
    return x;
    }

}


#endif