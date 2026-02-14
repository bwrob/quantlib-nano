          return step_iterator(i.base_ - n * i.step_, i.step_);
        }

        friend difference_type operator-(const step_iterator& lhs, const step_iterator& rhs) {
#ifdef QL_EXTRA_SAFETY_CHECKS
            QL_REQUIRE(lhs.step_ == rhs.step_, "step_iterators with different step cannot be added or subtracted");
#endif
            return (lhs.base_ - rhs.base_) / lhs.step_;
        }

        friend bool operator==(const step_iterator& lhs, const step_iterator& rhs) {
            return lhs.base_ == rhs.base_ && lhs.step_ == rhs.step_;
        }

        friend bool operator!=(const step_iterator& lhs, const step_iterator& rhs) {
            return lhs.base_ != rhs.base_ || lhs.step_ != rhs.step_;
        }

        friend bool operator<(const step_iterator& lhs, const step_iterator& rhs) {
#ifdef QL_EXTRA_SAFETY_CHECKS
            QL_REQUIRE(lhs.step_ == rhs.step_, "step_iterators with different step cannot be compared");
#endif
            return lhs.base_ < rhs.base_;
        }

        friend bool operator>(const step_iterator& lhs, const step_iterator& rhs) {
#ifdef QL_EXTRA_SAFETY_CHECKS
            QL_REQUIRE(lhs.step_ == rhs.step_, "step_iterators with different step cannot be compared");
#endif
            return lhs.base_ > rhs.base_;
        }

        friend bool operator<=(const step_iterator& lhs, const step_iterator& rhs) {
#ifdef QL_EXTRA_SAFETY_CHECKS
            QL_REQUIRE(lhs.step_ == rhs.step_, "step_iterators with different step cannot be compared");
#endif
            return lhs.base_ <= rhs.base_;
        }

        friend bool operator>=(const step_iterator& lhs, const step_iterator& rhs) {
#ifdef QL_EXTRA_SAFETY_CHECKS
            QL_REQUIRE(lhs.step_ == rhs.step_, "step_iterators with different step cannot be compared");
#endif
            return lhs.base_ >= rhs.base_;
        }
    };

    //! helper function to create step iterators
    /*! \relates step_iterator */
    template <class Iterator>
    step_iterator<Iterator> make_step_iterator(Iterator it, Size step) {
        return step_iterator<Iterator>(it,step);
    }

}


#endif
