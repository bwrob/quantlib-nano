/2.0;
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
                                Real density,
                                Size i) {
            data[i] = density;
            if (i==1)
                data[0] = density; // first point is updated as well
        }
        // upper bound for convergence loop
        static Size maxIterations() { return 30; }
    };

}

#endif
