eneralLinearLeastSquares::calculate(xIterator xBegin, xIterator xEnd,
                                              yIterator yBegin, yIterator yEnd,
                                              vIterator vBegin) {

        const Size n = residuals_.size();
        const Size m = err_.size();

        QL_REQUIRE( n == Size(std::distance(yBegin, yEnd)),
            "sample set need to be of the same size");
        QL_REQUIRE(n >= m, "sample set is too small");

        Size i;

        Matrix A(n, m);
        for (i=0; i<m; ++i)
            std::transform(xBegin, xEnd, A.column_begin(i), *vBegin++);

        const SVD svd(A);
        const Matrix& V = svd.V();
        const Matrix& U = svd.U();
        const Array& w = svd.singularValues();
        const Real threshold = n * QL_EPSILON * svd.singularValues()[0];

        for (i=0; i<m; ++i) {
            if (w[i] > threshold) {
                const Real u = std::inner_product(U.column_begin(i),
                    U.column_end(i),
                    yBegin, Real(0.0))/w[i];

                for (Size j=0; j<m; ++j) {
                    a_[j]  +=u*V[j][i];
                    err_[j]+=V[j][i]*V[j][i]/(w[i]*w[i]);
                }
            }
        }
        err_      = Sqrt(err_);
        Array tmp = A*a_;
        std::transform(tmp.begin(), tmp.end(), yBegin, residuals_.begin(), std::minus<>());

        const Real chiSq
            = std::inner_product(residuals_.begin(), residuals_.end(), residuals_.begin(), Real(0.0));
        const Real multiplier = std::sqrt(chiSq/(n-2));
        std::transform(err_.begin(), err_.end(), standardErrors_.begin(),
                       [=](Real x) -> Real { return x * multiplier; });
    }

}

#endif