k();
            Time dtMax;
            // The resulting timegrid have points at times listed in the input
            // list. Between these points, there are inner-points which are
            // regularly spaced.
            if (steps == 0) {
                std::vector<Time> diff;
                std::adjacent_difference(mandatoryTimes_.begin(),
                                         mandatoryTimes_.end(),
                                         std::back_inserter(diff));
                QL_REQUIRE(!diff.empty(), "at least two distinct points required in time grid");

                if (diff.front()==0.0)
                    diff.erase(diff.begin());

                auto i = std::min_element(diff.begin(), diff.end());
                QL_REQUIRE(i != diff.end(), "not enough distinct points in time grid");
                dtMax = *i;
            } else {
                dtMax = last/steps;
            }

            Time periodBegin = 0.0;
            times_.push_back(periodBegin);
            for (auto t=mandatoryTimes_.begin();
                                                   t<mandatoryTimes_.end();
                                                   ++t) {
                Time periodEnd = *t;
                if (periodEnd != 0.0) {
                    // the nearest integer, at least 1
                    Size nSteps = std::max(Size(std::lround((periodEnd - periodBegin)/dtMax)), Size(1));
                    Time dt = (periodEnd - periodBegin)/nSteps;
                    for (Size n=1; n<=nSteps; ++n)
                        times_.push_back(periodBegin + n*dt);
                }
                periodBegin = periodEnd;
            }

            dt_.reserve(times_.size()-1);
            std::adjacent_difference(times_.begin()+1,times_.end(),
                                     std::back_inserter(dt_));
        }
        TimeGrid(std::initializer_list<Time> times)
        : TimeGrid(times.begin(), times.end()) {}
        TimeGrid(std::initializer_list<Time> times, Size steps)
        : TimeGrid(times.begin(), times.end(), steps) {}
        //@}
        //! \name Time grid interface
        //@{
        //! returns the index i such that grid[i] = t
        Size index(Time t) const;
        //! returns the index i such that grid[i] is closest to t
        Size closestIndex(Time t) const;
        //! returns the time on the grid closest to the given t
        Time closestTime(Time t) const {
            return times_[closestIndex(t)];
        }
        const std::vector<Time>& mandatoryTimes() const {
            return mandatoryTimes_;
        }
        Time dt(Size i) const { return dt_[i]; }
        //@}
        //! \name sequence interface
        //@{
        typedef std::vector<Time>::const_iterator const_iterator;
        typedef std::vector<Time>::const_reverse_iterator
                                          const_reverse_iterator;

        Time operator[](Size i) const { return times_[i]; }
        Time at(Size i) const { return times_.at(i); }
        Size size() const { return times_.size(); }
        bool empty() const { return times_.empty(); }
        const_iterator begin() const { return times_.begin(); }
        const_iterator end() const { return times_.end(); }
        const_reverse_iterator rbegin() const { return times_.rbegin(); }
        const_reverse_iterator rend() const { return times_.rend(); }
        Time front() const { return times_.front(); }
        Time back() const { return times_.back(); }
        //@}
      private:
        std::vector<Time> times_;
        std::vector<Time> dt_;
        std::vector<Time> mandatoryTimes_;
    };

}


#endif
