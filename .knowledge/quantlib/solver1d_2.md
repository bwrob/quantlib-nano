");
            QL_REQUIRE(guess < xMax_,
                       "guess (" << guess << ") > xMax_ (" << xMax_ << ")");

            root_ = guess;

            return this->impl().solveImpl(f, accuracy);
        }

        /*! This method sets the maximum number of function
            evaluations for the bracketing routine. An error is thrown
            if a bracket is not found after this number of
            evaluations.
        */
        void setMaxEvaluations(Size evaluations);
        //! sets the lower bound for the function domain
        void setLowerBound(Real lowerBound);
        //! sets the upper bound for the function domain
        void setUpperBound(Real upperBound);
        //@}
      protected:
        mutable Real root_, xMin_, xMax_, fxMin_, fxMax_;
        Size maxEvaluations_ = MAX_FUNCTION_EVALUATIONS;
        mutable Size evaluationNumber_;
      private:
        Real enforceBounds_(Real x) const;
        Real lowerBound_{}, upperBound_{};
        bool lowerBoundEnforced_ = false, upperBoundEnforced_ = false;
    };


    // inline definitions

    template <class T>
    inline void Solver1D<T>::setMaxEvaluations(Size evaluations) {
        maxEvaluations_ = evaluations;
    }

    template <class T>
    inline void Solver1D<T>::setLowerBound(Real lowerBound) {
        lowerBound_ = lowerBound;
        lowerBoundEnforced_ = true;
    }

    template <class T>
    inline void Solver1D<T>::setUpperBound(Real upperBound) {
        upperBound_ = upperBound;
        upperBoundEnforced_ = true;
    }

    template <class T>
    inline Real Solver1D<T>::enforceBounds_(Real x) const {
        if (lowerBoundEnforced_ && x < lowerBound_)
            return lowerBound_;
        if (upperBoundEnforced_ && x > upperBound_)
            return upperBound_;
        return x;
    }

}

#endif