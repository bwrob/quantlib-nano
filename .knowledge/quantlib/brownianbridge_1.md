  and finishes at the same value, the first element of
                  the input sequence must be zero. Conversely, to get
                  a sloped bridge set the first element to a non-zero
                  value. In this case, the final value in the bridge
                  will be sqrt(last time point)*(first element of
                  input sequence).
        */
        template <class RandomAccessIterator1,
                  class RandomAccessIterator2>
        void transform(RandomAccessIterator1 begin,
                       RandomAccessIterator1 end,
                       RandomAccessIterator2 output) const {
            QL_REQUIRE(end >= begin, "invalid sequence");
            QL_REQUIRE(Size(end-begin) == size_,
                       "incompatible sequence size");
            // We use output to store the path...
            output[size_-1] = stdDev_[0] * begin[0];
            for (Size i=1; i<size_; ++i) {
                Size j = leftIndex_[i];
                Size k = rightIndex_[i];
                Size l = bridgeIndex_[i];
                if (j != 0) {
                    output[l] =
                        leftWeight_[i] * output[j-1] +
                        rightWeight_[i] * output[k]   +
                        stdDev_[i] * begin[i];
                } else {
                    output[l] =
                        rightWeight_[i] * output[k]   +
                        stdDev_[i] * begin[i];
                }
            }
            // ...after which, we calculate the variations and
            // normalize to unit times
            for (Size i=size_-1; i>=1; --i) {
                output[i] -= output[i-1];
                output[i] /= sqrtdt_[i];
            }
            output[0] /= sqrtdt_[0];
        }
      private:
        void initialize();
        Size size_;
        std::vector<Time> t_;
        std::vector<Real> sqrtdt_;
        std::vector<Size> bridgeIndex_, leftIndex_, rightIndex_;
        std::vector<Real> leftWeight_, rightWeight_, stdDev_;
    };

}

#endif