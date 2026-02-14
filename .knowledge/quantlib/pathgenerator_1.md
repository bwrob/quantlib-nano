inter_cast<StochasticProcess1D>(process)),
      next_(Path(timeGrid_), 1.0), temp_(dimension_), bb_(timeGrid_) {
        QL_REQUIRE(dimension_==timeGrid_.size()-1,
                   "sequence generator dimensionality (" << dimension_
                   << ") != timeSteps (" << timeGrid_.size()-1 << ")");
    }

    template <class GSG>
    const typename PathGenerator<GSG>::sample_type&
    PathGenerator<GSG>::next() const {
        return next(false);
    }

    template <class GSG>
    const typename PathGenerator<GSG>::sample_type&
    PathGenerator<GSG>::antithetic() const {
        return next(true);
    }

    template <class GSG>
    const typename PathGenerator<GSG>::sample_type&
    PathGenerator<GSG>::next(bool antithetic) const {

        typedef typename GSG::sample_type sequence_type;
        const sequence_type& sequence_ =
            antithetic ? generator_.lastSequence()
                       : generator_.nextSequence();

        if (brownianBridge_) {
            bb_.transform(sequence_.value.begin(),
                          sequence_.value.end(),
                          temp_.begin());
        } else {
            std::copy(sequence_.value.begin(),
                      sequence_.value.end(),
                      temp_.begin());
        }

        next_.weight = sequence_.weight;

        Path& path = next_.value;
        path.front() = process_->x0();

        for (Size i=1; i<path.length(); i++) {
            Time t = timeGrid_[i-1];
            Time dt = timeGrid_.dt(i-1);
            path[i] = process_->evolve(t, path[i-1], dt,
                                       antithetic ? -temp_[i-1] :
                                                     temp_[i-1]);
        }

        return next_;
    }

}


#endif
