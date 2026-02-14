r,
        const Date& referenceDate,
        const VolatilityType type,
        const Real shift)
    : SmileSection(d, dc, referenceDate, type, shift),
      exerciseTimeSquareRoot_(std::sqrt(exerciseTime())), strikes_(std::move(strikes)),
      stdDevHandles_(stdDevs.size()), vols_(stdDevs.size()) {
        //fill dummy handles to allow generic handle-based
        // computations later on
        for (Size i=0; i<stdDevs.size(); ++i)
            stdDevHandles_[i] = Handle<Quote>(ext::shared_ptr<Quote>(new
                SimpleQuote(stdDevs[i])));
        atmLevel_ = Handle<Quote>
           (ext::shared_ptr<Quote>(new SimpleQuote(atmLevel)));
        // check strikes!!!!!!!!!!!!!!!!!!!!
        interpolation_ = interpolator.interpolate(strikes_.begin(),
                                                  strikes_.end(),
                                                  vols_.begin());
    }


    template <class Interpolator>
    inline void InterpolatedSmileSection<Interpolator>::performCalculations()
                                                                      const {
        for (Size i=0; i<stdDevHandles_.size(); ++i)
            vols_[i] = stdDevHandles_[i]->value()/exerciseTimeSquareRoot_;
        interpolation_.update();
    }

    #ifndef __DOXYGEN__
    template <class Interpolator>
    Real InterpolatedSmileSection<Interpolator>::varianceImpl(Real strike) const {
        calculate();
        Real v = interpolation_(strike, true);
        return v*v*exerciseTime();
    }

    template <class Interpolator>
    Real InterpolatedSmileSection<Interpolator>::volatilityImpl(Real strike) const {
        calculate();
        return interpolation_(strike, true);
    }

    template <class Interpolator>
    void InterpolatedSmileSection<Interpolator>::update() {
        LazyObject::update();
        SmileSection::update();
    }
    #endif

}

#endif
