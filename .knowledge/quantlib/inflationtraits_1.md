per;

        // start of curve data
        static Date initialDate(const YoYInflationTermStructure* t) {
            return t->baseDate();
        }

        // value at reference date
        static Rate initialValue(const YoYInflationTermStructure* t) {
            return t->baseRate();
        }

        // guesses
        template <class C>
        static Rate guess(Size i,
                          const C* c,
                          bool validData,
                          Size) // firstAliveHelper
        {
            if (validData) // previous iteration value
                return c->data()[i];

            return detail::avgInflation;
        }

        // constraints
        template <class C>
        static Rate minValueAfter(Size,
                                  const C* c,
                                  bool validData,
                                  Size) // firstAliveHelper
        {
            if (validData) {
                Rate r = *(std::min_element(c->data().begin(), c->data().end()));
                return r<0.0 ? Real(r*2.0) : r/2.0;
            }
            return -detail::maxInflation;
        }
        template <class C>
        static Rate maxValueAfter(Size,
                                  const C* c,
                                  bool validData,
                                  Size) // firstAliveHelper
        {
            if (validData) {
                Rate r = *(std::max_element(c->data().begin(), c->data().end()));
                return r<0.0 ? Real(r/2.0) : r*2.0;
            }
            // no constraints.
            // We choose as max a value very unlikely to be exceeded.
            return detail::maxInflation;
        }

        // update with new guess
        static void updateGuess(std::vector<Rate>& data,
                                Rate level,
                                Size i) {
            data[i] = level;
        }
        // upper bound for convergence loop
        static Size maxIterations() { return 40; }
    };

}

#endif
