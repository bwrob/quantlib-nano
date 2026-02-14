  //! number of negative samples collected
        Size downsideSamples() const;

        //! sum of data weights for negative samples
        Real downsideWeightSum() const;

        /*! returns the downside variance, defined as
            \f[ \frac{N}{N-1} \times \frac{ \sum_{i=1}^{N}
                \theta \times x_i^{2}}{ \sum_{i=1}^{N} w_i} \f],
            where \f$ \theta \f$ = 0 if x > 0 and
            \f$ \theta \f$ =1 if x <0
        */
        Real downsideVariance() const;

        /*! returns the downside deviation, defined as the
            square root of the downside variance.
        */
        Real downsideDeviation() const;

        //@}

        //! \name Modifiers
        //@{
        //! adds a datum to the set, possibly with a weight
        /*! \pre weight must be positive or null */
        void add(Real value, Real weight = 1.0);
        //! adds a sequence of data to the set, with default weight
        template <class DataIterator>
        void addSequence(DataIterator begin, DataIterator end) {
            for (;begin!=end;++begin)
                add(*begin);
        }
        //! adds a sequence of data to the set, each with its weight
        /*! \pre weights must be positive or null */
        template <class DataIterator, class WeightIterator>
        void addSequence(DataIterator begin, DataIterator end,
                         WeightIterator wbegin) {
            for (;begin!=end;++begin,++wbegin)
                add(*begin, *wbegin);
        }
        //! resets the data to a null set
        void reset();
        //@}
     private:
       typedef boost::accumulators::accumulator_set<
           Real,
           boost::accumulators::stats<
               boost::accumulators::tag::count, boost::accumulators::tag::min,
               boost::accumulators::tag::max,
               boost::accumulators::tag::weighted_mean,
               boost::accumulators::tag::weighted_variance,
               boost::accumulators::tag::weighted_skewness,
               boost::accumulators::tag::weighted_kurtosis,
               boost::accumulators::tag::sum_of_weights>,
           Real> accumulator_set;
        accumulator_set acc_;
        typedef boost::accumulators::accumulator_set<
            Real, boost::accumulators::stats<
                      boost::accumulators::tag::count,
                      boost::accumulators::tag::weighted_moment<2>,
                      boost::accumulators::tag::sum_of_weights>,
            Real> downside_accumulator_set;
        downside_accumulator_set downsideAcc_;
    };

}


#endif
