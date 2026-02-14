s
        template <class C>
        static Real guess(Size i,
                          const C* c,
                          bool validData,
                          Size) // firstAliveHelper
        {
            if (validData) // previous iteration value
                return c->data()[i];

            if (i==1) // first pillar
                return detail::avgRate;

            // extrapolate
            Date d = c->dates()[i];
            return c->forwardRate(d, d, c->dayCounter(),
                                  Continuous, Annual, true);
        }

        // possible constraints based on previous values
        template <class C>
        static Real minValueAfter(Size,
                                  const C* c,
                                  bool validData,
                                  Size) // firstAliveHelper
        {
            if (validData) {
                Real r = *(std::min_element(c->data().begin(), c->data().end()));
                return r<0.0 ? Real(r*2.0) : Real(r/2.0);
            }
            // no constraints.
            // We choose as min a value very unlikely to be exceeded.
            return -detail::maxRate;
        }
        template <class C>
        static Real maxValueAfter(Size,
                                  const C* c,
                                  bool validData,
                                  Size) // firstAliveHelper
        {
            if (validData) {
                Real r = *(std::max_element(c->data().begin(), c->data().end()));
                return r<0.0 ? Real(r/2.0) : Real(r*2.0);
            }
            // no constraints.
            // We choose as max a value very unlikely to be exceeded.
            return detail::maxRate;
        }

        // transformation to add constraints to an unconstrained optimization
        template <class C>
        static Real transformDirect(Real x, Size i, const C* c)
        {
            return x;
        }
        template <class C>
        static Real transformInverse(Real x, Size i, const C* c)
        {
            return x;
        }

        // root-finding update
        static void updateGuess(std::vector<Real>& data,
                                Real forward,
                                Size i) {
            data[i] = forward;
            if (i==1)
                data[0] = forward; // first point is updated as well
        }
        // upper bound for convergence loop
        static Size maxIterations() { return 100; }
    };

    //! Simple Zero-curve traits
    struct SimpleZeroYield {
        // interpolated curve type
        template <class Interpolator>
        struct curve {
            typedef InterpolatedSimpleZeroCurve<Interpolator> type;
        };
        // helper class
        typedef BootstrapHelper<YieldTermStructure> helper;

        // start of curve data
        static Date initialDate(const YieldTermStructure* c) {
            return c->referenceDate();
        }
        // dummy value at reference date
        static Real initialValue(const YieldTermStructure*) {
            return detail::avgRate;
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
                return detail::avgRate;

            // extrapolate
            Date d = c->dates()[i];
            return c->zeroRate(d, c->dayCounter(),
                               Simple, Annual, true);
        }

        // possible constraints based on previous values
        template <class C>
        static Real minValueAfter(Size i,
                                  const C* c,
                                  bool validData,
                                  Size) // firstAliveHelper
        {
        