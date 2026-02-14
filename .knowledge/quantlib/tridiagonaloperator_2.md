lOperator operator-(const TridiagonalOperator& D1,
                                         const TridiagonalOperator& D2) {
        Array low = D1.lowerDiagonal_ - D2.lowerDiagonal_,
            mid = D1.diagonal_ - D2.diagonal_,
            high = D1.upperDiagonal_ - D2.upperDiagonal_;
        TridiagonalOperator result(low, mid, high);
        return result;
    }

    inline TridiagonalOperator operator*(Real a,
                                         const TridiagonalOperator& D) {
        Array low = D.lowerDiagonal_ * a,
            mid = D.diagonal_ * a,
            high = D.upperDiagonal_ * a;
        TridiagonalOperator result(low, mid, high);
        return result;
    }

    inline TridiagonalOperator operator*(const TridiagonalOperator& D,
                                         Real a) {
        Array low = D.lowerDiagonal_ * a,
            mid = D.diagonal_ * a,
            high = D.upperDiagonal_ * a;
        TridiagonalOperator result(low, mid, high);
        return result;
    }

    inline TridiagonalOperator operator/(const TridiagonalOperator& D,
                                         Real a) {
        Array low = D.lowerDiagonal_ / a,
            mid = D.diagonal_ / a,
            high = D.upperDiagonal_ / a;
        TridiagonalOperator result(low, mid, high);
        return result;
    }

    inline void swap(TridiagonalOperator& L1,
                     TridiagonalOperator& L2) noexcept {
        L1.swap(L2);
    }

}

#endif
