        Real maxStrike() const override { return strikes_.back(); }
        Real atmLevel() const override { return atmLevel_->value(); }
        void update() override;

      private:
        Real exerciseTimeSquareRoot_;
        std::vector<Rate> strikes_;
        std::vector<Handle<Quote> > stdDevHandles_;
        Handle<Quote> atmLevel_;
        mutable std::vector<Volatility> vols_;
        mutable Interpolation interpolation_;
    };


    template <class Interpolator>
    InterpolatedSmileSection<Interpolator>::InterpolatedSmileSection(
        Time timeToExpiry,
        std::vector<Rate> strikes,
        const std::vector<Handle<Quote> >& stdDevHandles,
        Handle<Quote> atmLevel,
        const Interpolator& interpolator,
        const DayCounter& dc,
        const VolatilityType type,
        const Real shift)
    : SmileSection(timeToExpiry, dc, type, shift),
      exerciseTimeSquareRoot_(std::sqrt(exerciseTime())), strikes_(std::move(strikes)),
      stdDevHandles_(stdDevHandles), atmLevel_(std::move(atmLevel)), vols_(stdDevHandles.size()) {
        for (auto& stdDevHandle : stdDevHandles_)
            LazyObject::registerWith(stdDevHandle);
        LazyObject::registerWith(atmLevel_);
        // check strikes!!!!!!!!!!!!!!!!!!!!
        interpolation_ = interpolator.interpolate(strikes_.begin(),
                                                  strikes_.end(),
                                                  vols_.begin());
    }

    template <class Interpolator>
    InterpolatedSmileSection<Interpolator>::InterpolatedSmileSection(
        Time timeToExpiry,
        std::vector<Rate> strikes,
        const std::vector<Real>& stdDevs,
        Real atmLevel,
        const Interpolator& interpolator,
        const DayCounter& dc,
        const VolatilityType type,
        const Real shift)
    : SmileSection(timeToExpiry, dc, type, shift),
      exerciseTimeSquareRoot_(std::sqrt(exerciseTime())), strikes_(std::move(strikes)),
      stdDevHandles_(stdDevs.size()), vols_(stdDevs.size()) {
        // fill dummy handles to allow generic handle-based
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
    InterpolatedSmileSection<Interpolator>::InterpolatedSmileSection(
        const Date& d,
        std::vector<Rate> strikes,
        const std::vector<Handle<Quote> >& stdDevHandles,
        Handle<Quote> atmLevel,
        const DayCounter& dc,
        const Interpolator& interpolator,
        const Date& referenceDate,
        const VolatilityType type,
        const Real shift)
    : SmileSection(d, dc, referenceDate, type, shift),
      exerciseTimeSquareRoot_(std::sqrt(exerciseTime())), strikes_(std::move(strikes)),
      stdDevHandles_(stdDevHandles), atmLevel_(std::move(atmLevel)), vols_(stdDevHandles.size()) {
        for (auto& stdDevHandle : stdDevHandles_)
            LazyObject::registerWith(stdDevHandle);
        LazyObject::registerWith(atmLevel_);
        // check strikes!!!!!!!!!!!!!!!!!!!!
        interpolation_ = interpolator.interpolate(strikes_.begin(),
                                                  strikes_.end(),
                                                  vols_.begin());
    }

    template <class Interpolator>
    InterpolatedSmileSection<Interpolator>::InterpolatedSmileSection(
        const Date& d,
        std::vector<Rate> strikes,
        const std::vector<Real>& stdDevs,
        Real atmLevel,
        const DayCounter& dc,
        const Interpolator& interpolato