         const std::vector<Real> &         y,
            const std::vector<std::function<Real(ArgumentType)> > & v)
        : GeneralLinearLeastSquares(x, y, v) {
        }
    };
}
#endif
