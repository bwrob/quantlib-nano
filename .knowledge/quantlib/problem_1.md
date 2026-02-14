        //! number of evaluation of cost function and its gradient
        Integer functionEvaluation_, gradientEvaluation_;
    };

    // inline definitions
    inline Real Problem::value(const Array& x) {
        ++functionEvaluation_;
        return costFunction_.value(x);
    }

    inline Array Problem::values(const Array& x) {
        ++functionEvaluation_;
        return costFunction_.values(x);
    }

    inline void Problem::gradient(Array& grad_f,
                                  const Array& x) {
        ++gradientEvaluation_;
        costFunction_.gradient(grad_f, x);
    }

    inline Real Problem::valueAndGradient(Array& grad_f,
                                          const Array& x) {
        ++functionEvaluation_;
        ++gradientEvaluation_;
        return costFunction_.valueAndGradient(grad_f, x);
    }

    inline void Problem::reset() {
        functionEvaluation_ = gradientEvaluation_ = 0;
        functionValue_ = squaredNorm_ = Null<Real>();
    }

}

#endif