r idea to
             have a different naming when having these two components.
             What is meant here is the deterministic part of a ++model type
            */
            return c->hazardRate(d, true);
        }

        // constraints
        template <class C>
        static Real minValueAfter(Size i,
                                  const C* c,
                                  bool validData,
                                  Size) // firstAliveHelper
        {
            if (validData) {
                Real r = *(std::min_element(c->data().begin(),
                                            c->data().end()));
                return r/2.0;
            }
            return detail::minHazardRateComp;
            ///return QL_EPSILON;
        }
        template <class C>
        static Real maxValueAfter(Size i,
                                  const C* c,
                                  bool validData,
                                  Size) // firstAliveHelper
        {
            if (validData) {
                Real r = *(std::max_element(c->data().begin(),
                                            c->data().end()));
                return r*2.0;
            }
            // no constraints.
            // We choose as max a value very unlikely to be exceeded.
            return detail::maxHazardRate;
        }
        // update with new guess
        static void updateGuess(std::vector<Real>& data,
                                Real rate,
                                Size i) {
            data[i] = rate;
            if (i==1)
                data[0] = rate; // first point is updated as well
        }
        // upper bound for convergence loop
        static Size maxIterations() { return 30; }
    };


    // inline definitions

    template <class T>
    inline Date InterpolatedAffineHazardRateCurve<T>::maxDate() const {
        return dates_.back();
    }

    template <class T>
    inline const std::vector<Time>&
    InterpolatedAffineHazardRateCurve<T>::times() const {
        return this->times_;
    }

    template <class T>
    inline const std::vector<Date>&
    InterpolatedAffineHazardRateCurve<T>::dates() const {
        return dates_;
    }

    template <class T>
    inline const std::vector<Real>&
    InterpolatedAffineHazardRateCurve<T>::data() const {
        return this->data_;
    }

    template <class T>
    inline const std::vector<Rate>&
    InterpolatedAffineHazardRateCurve<T>::hazardRates() const {
        return this->data_;
    }

    template <class T>
    inline std::vector<std::pair<Date, Real> >
    InterpolatedAffineHazardRateCurve<T>::nodes() const {
        std::vector<std::pair<Date, Real> > results(dates_.size());
        for (Size i=0; i<dates_.size(); ++i)
            results[i] = std::make_pair(dates_[i], this->data_[i]);
        return results;
    }

    #ifndef __DOXYGEN__

    // template definitions

    template <class T>
    Real InterpolatedAffineHazardRateCurve<T>::hazardRateImpl(Time t) const {
        if (t <= this->times_.back())
            return this->interpolation_(t, true);

        // deterministic flat hazard rate extrapolation
        return this->data_.back();
    }

    // notice it is rewritten and no call is made to hazardRateImpl
    template <class T>
    Probability
    InterpolatedAffineHazardRateCurve<T>::survivalProbabilityImpl(
        Time t) const
    {
        // the way x0 is defined:
        Real initValHR = std::pow(model_->dynamics()->process()->x0(), 2);

        if (t == 0.0)
            return model_->discountBond(0., t, initValHR);

        Real integral;
        if (t <= this->times_.back()) {
            integral = this->interpolation_.primitive(t, true);
        } else {
            // flat hazard rate extrapolation
            integral =
                this->interpolation_.primitive(this->times_.back(), true)
                     + this->data_.back()*(t - this->times_.back());
        }
        return std::exp
