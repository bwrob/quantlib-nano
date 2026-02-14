ber of observations in the given range.
        */
        template <class Func, class Predicate>
        std::pair<Real,Size> expectationValue(const Func& f,
                                              const Predicate& inRange) const {
            Real num = 0.0, den = 0.0;
            Size N = 0;
            std::vector<std::pair<Real,Real> >::const_iterator i;
            for (i=samples_.begin(); i!=samples_.end(); ++i) {
                Real x = i->first, w = i->second;
                if (inRange(x)) {
                    num += f(x)*w;
                    den += w;
                    N += 1;
                }
            }
            if (N == 0)
                return std::make_pair<Real,Size>(Null<Real>(),0);
            else
                return std::make_pair(num/den,N);
        }

        /*! Expectation value of a function \f$ f \f$ over the whole
            set of samples; equivalent to passing the other overload
            a range function always returning <tt>true</tt>.
        */
        template <class Func>
        std::pair<Real,Size> expectationValue(const Func& f) const {
            return expectationValue(f, [](Real x) { return true; });
        }

        /*! \f$ y \f$-th percentile, defined as the value \f$ \bar{x} \f$
            such that
            \f[ y = \frac{\sum_{x_i < \bar{x}} w_i}{
                          \sum_i w_i} \f]

            \pre \f$ y \f$ must be in the range \f$ (0-1]. \f$
        */
        Real percentile(Real y) const;

        /*! \f$ y \f$-th top percentile, defined as the value
            \f$ \bar{x} \f$ such that
            \f[ y = \frac{\sum_{x_i > \bar{x}} w_i}{
                          \sum_i w_i} \f]

            \pre \f$ y \f$ must be in the range \f$ (0-1]. \f$
        */
        Real topPercentile(Real y) const;
        //@}

        //! \name Modifiers
        //@{
        //! adds a datum to the set, possibly with a weight
        void add(Real value, Real weight = 1.0);
        //! adds a sequence of data to the set, with default weight
        template <class DataIterator>
        void addSequence(DataIterator begin, DataIterator end) {
            for (;begin!=end;++begin)
                add(*begin);
        }
        //! adds a sequence of data to the set, each with its weight
        template <class DataIterator, class WeightIterator>
        void addSequence(DataIterator begin, DataIterator end,
                         WeightIterator wbegin) {
            for (;begin!=end;++begin,++wbegin)
                add(*begin, *wbegin);
        }

        //! resets the data to a null set
        void reset();

        //! informs the internal storage of a planned increase in size
        void reserve(Size n) const;

        //! sort the data set in increasing order
        void sort() const;
        //@}
      private:
        mutable std::vector<std::pair<Real,Real> > samples_;
        mutable bool sorted_;
    };


    // inline definitions

    inline GeneralStatistics::GeneralStatistics() {
        reset();
    }

    inline Size GeneralStatistics::samples() const {
        return samples_.size();
    }

    inline const std::vector<std::pair<Real,Real> >&
    GeneralStatistics::data() const {
        return samples_;
    }

    inline Real GeneralStatistics::standardDeviation() const {
        return std::sqrt(variance());
    }

    inline Real GeneralStatistics::errorEstimate() const {
        return std::sqrt(variance()/samples());
    }

    inline Real GeneralStatistics::min() const {
        QL_REQUIRE(samples() > 0, "empty sample set");
        return std::min_element(samples_.begin(),
                                samples_.end())->first;
    }

    inline Real GeneralStatistics::max() const {
        QL_REQUIRE(samples() > 0, "empty sample set");
        return std::max_element(samples_.begin(),
                                samples_.end())->first;
    }

    /*! \pre weights must be positive or null */
    inline void GeneralSta
