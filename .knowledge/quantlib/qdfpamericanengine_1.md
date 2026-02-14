erationScheme: public QdFpIterationScheme {
      public:
        QdFpTanhSinhIterationScheme(Size m, Size n, Real eps);

        Size getNumberOfChebyshevInterpolationNodes() const override;
        Size getNumberOfNaiveFixedPointSteps() const override;
        Size getNumberOfJacobiNewtonFixedPointSteps() const override;

        ext::shared_ptr<Integrator> getFixedPointIntegrator() const override;
        ext::shared_ptr<Integrator> getExerciseBoundaryToPriceIntegrator() const override;
      private:
        const Size m_, n_;
        const ext::shared_ptr<Integrator> integrator_;
    };


    //! High performance/precision American engine based on fixed point iteration for the exercise boundary
    /*! References:
        Leif Andersen, Mark Lake and Dimitri Offengenden (2015)
        "High Performance American Option Pricing",
        https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2547027

        Leif Andersen, Mark Lake (2021)
        "Fast American Option Pricing: The Double-Boundary Case"

        https://onlinelibrary.wiley.com/doi/abs/10.1002/wilm.10969
    */
    class QdFpAmericanEngine : public detail::QdPutCallParityEngine {
      public:
        enum FixedPointEquation { FP_A, FP_B, Auto };

        explicit QdFpAmericanEngine(
          ext::shared_ptr<GeneralizedBlackScholesProcess> bsProcess,
          ext::shared_ptr<QdFpIterationScheme> iterationScheme = accurateScheme(),
          FixedPointEquation fpEquation = Auto);

        static ext::shared_ptr<QdFpIterationScheme> fastScheme();
        static ext::shared_ptr<QdFpIterationScheme> accurateScheme();
        static ext::shared_ptr<QdFpIterationScheme> highPrecisionScheme();

      protected:
        Real calculatePut(
            Real S, Real K, Rate r, Rate q, Volatility vol, Time T) const override;

      private:
        const ext::shared_ptr<QdFpIterationScheme> iterationScheme_;
        const FixedPointEquation fpEquation_;
    };

}

#endif