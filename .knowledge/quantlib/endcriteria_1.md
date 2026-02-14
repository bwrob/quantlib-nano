t;
        /*! Test if the gradient norm value is below gradientNormEpsilon */
        bool checkZeroGradientNorm(Real gNorm, EndCriteria::Type& ecType) const;

        static bool succeeded(EndCriteria::Type ecType);
      protected:
        //! Maximum number of iterations
        Size maxIterations_;
        //! Maximun number of iterations in stationary state
        mutable Size maxStationaryStateIterations_;
        //! root, function and gradient epsilons
        Real rootEpsilon_, functionEpsilon_, gradientNormEpsilon_;

    };

    std::ostream& operator<<(std::ostream& out, EndCriteria::Type ecType);

}

#endif