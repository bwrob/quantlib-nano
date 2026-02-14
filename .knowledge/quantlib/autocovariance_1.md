ariances must be less than data size");
        const std::vector<std::complex<Real> >& ft = double_ft(begin, end);
        Real w1 = 1.0 / (Real)ft.size(), w2 = (Real)nData;
        for (std::size_t k = 0; k <= maxLag; ++k, w2 -= 1.0) {
            *out++ = ft[k].real() * w1 / w2;
        }
    }

    //! Unbiased auto-covariances
    /*! Results are calculated via FFT.

        This overload accepts non-centered data, removes the mean and
        returns it as a result.  The centered sequence is written back
        into the input sequence if the reuse parameter is true.

        \pre The size of the output sequence must be maxLag + 1
    */
    template <typename ForwardIterator, typename OutputIterator>
    Real autocovariances(ForwardIterator begin, ForwardIterator end,
                         OutputIterator out,
                         std::size_t maxLag, bool reuse) {
        using namespace detail;
        Real mean = 0.0;
        if (reuse) {
            mean = remove_mean(begin, end, begin);
            autocovariances(begin, end, out, maxLag);
        } else {
            Array tmp(std::distance(begin, end));
            mean = remove_mean(begin, end, tmp.begin());
            autocovariances(tmp.begin(), tmp.end(), out, maxLag);
        }
        return mean;
    }


    //! Unbiased auto-correlations.
    /*! Results are calculated via FFT.
        The first element of the output is the unbiased sample variance.

        \pre Input data are supposed to be centered (i.e., zero mean).
        \pre The size of the output sequence must be maxLag + 1
    */
    template <typename ForwardIterator, typename OutputIterator>
    void autocorrelations(ForwardIterator begin, ForwardIterator end,
                          OutputIterator out, std::size_t maxLag) {
        using namespace detail;
        std::size_t nData = std::distance(begin, end);
        QL_REQUIRE(maxLag < nData,
                   "number of correlations must be less than data size");
        const std::vector<std::complex<Real> >& ft = double_ft(begin, end);
        Real w1 = 1.0 / (Real)ft.size(), w2 = (Real)nData;
        Real variance = ft[0].real() * w1 / w2;
        *out++ = variance * w2 / (w2-1.0);
        w2 -= 1.0;
        for (std::size_t k = 1; k <= maxLag; ++k, w2 -= 1.0)
            *out++ = ft[k].real() * w1 / (variance * w2);
    }

    //! Unbiased auto-correlations.
    /*! Results are calculated via FFT.
        The first element of the output is the unbiased sample variance.

        This overload accepts non-centered data, removes the mean and
        returns it as a result.  The centered sequence is written back
        into the input sequence if the reuse parameter is true.

        \pre The size of the output sequence must be maxLag + 1
    */
    template <typename ForwardIterator, typename OutputIterator>
    Real autocorrelations(ForwardIterator begin, ForwardIterator end,
                          OutputIterator out,
                          std::size_t maxLag, bool reuse) {
        using namespace detail;
        Real mean = 0.0;
        if (reuse) {
            mean = remove_mean(begin, end, begin);
            autocorrelations(begin, end, out, maxLag);
        } else {
            Array tmp(std::distance(begin, end));
            mean = remove_mean(begin, end, tmp.begin());
            autocorrelations(tmp.begin(), tmp.end(), out, maxLag);
        }
        return mean;
    }

}

#endif
