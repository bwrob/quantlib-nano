ve {
            typedef InterpolatedHazardRateCurve<Interpolator> type;
        };
        // helper class
        typedef BootstrapHelper<DefaultProbabilityTermStructure> helper;

        // start of curve data
        static Date initialDate(const DefaultProbabilityTermStructure* c) {
            return c->referenceDate();
        }
        // dummy value at reference date
        static Real initialValue(const DefaultProbabilityTermStructure*) {
            return detail::avgHazardRate;
        }

        // guesses
        template <class C>
        static Real guess(Size i,
                          const C* c,
                          bool validData,
                          Size) // firstAliveHelper
        {
            if (validData) // previous iteration value
                return c->data()[i];

            if (i==1) // first pillar
                return detail::avgHazardRate;

            // extrapolate
            Date d = c->dates()[i];
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
                Real r = *(std::min_element(c->data().begin(), c->data().end()));
                return r/2.0;
            }
            return QL_EPSILON;
        }
        template <class C>
        static Real maxValueAfter(Size i,
                                  const C* c,
                                  bool validData,
                                  Size) // firstAliveHelper
        {
            if (validData) {
                Real r = *(std::max_element(c->data().begin(), c->data().end()));
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


    //! Default-density-curve traits
    struct DefaultDensity {
        // interpolated curve type
        template <class Interpolator>
        struct curve {
            typedef InterpolatedDefaultDensityCurve<Interpolator> type;
        };
        // helper class
        typedef BootstrapHelper<DefaultProbabilityTermStructure> helper;
        // start of curve data
        static Date initialDate(const DefaultProbabilityTermStructure* c) {
            return c->referenceDate();
        }
        // value at reference date
        static Real initialValue(const DefaultProbabilityTermStructure*) {
            return detail::avgHazardRate;
        }

        // guesses
        template <class C>
        static Real guess(Size i,
                          const C* c,
                          bool validData,
                          Size) // firstAliveHelper
        {
            if (validData) // previous iteration value
                return c->data()[i];

            if (i==1) // first pillar
                return detail::avgHazardRate;

            // extrapolate
            Date d = c->dates()[i];
            return c->defaultDensity(d, true);
        }

        // constraints
        template <class C>
        static Real minValueAfter(Size i,
                                  const C* c,
                                  bool validData,
                                  Size) // firstAliveHelper
        {
            if (validData) {
                Real r = *(std::min_element(c->data().begin(), c->data().end()));
                return r