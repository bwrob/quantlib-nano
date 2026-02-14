tion<Matrix(const Array&, Size, Size)> f,
                              Size matrixSize,
                              Size rank)
        : target_(std::move(target)), f_(std::move(f)), matrixSize_(matrixSize), rank_(rank) {}
        Real value(const Array& x) const override;
        Array values(const Array& x) const override;

      private:
        Matrix target_;
        std::function<Matrix(const Array&, Size, Size)> f_;
        Size matrixSize_;
        Size rank_;
    };
}

#endif
