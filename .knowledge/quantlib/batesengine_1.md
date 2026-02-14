lTolerance, Size maxEvaluations);

      protected:
        std::complex<Real> addOnTerm(Real phi, Time t, Size j) const override;
    };


    class BatesDetJumpEngine : public BatesEngine {
      public:
        explicit BatesDetJumpEngine(const ext::shared_ptr<BatesDetJumpModel>& model,
                                    Size integrationOrder = 144);
        BatesDetJumpEngine(const ext::shared_ptr<BatesDetJumpModel>& model,
                           Real relTolerance, Size maxEvaluations);

      protected:
        std::complex<Real> addOnTerm(Real phi, Time t, Size j) const override;
    };


    class BatesDoubleExpEngine : public AnalyticHestonEngine {
      public:
        explicit BatesDoubleExpEngine(
            const ext::shared_ptr<BatesDoubleExpModel>& model,
            Size integrationOrder = 144);
        BatesDoubleExpEngine(
            const ext::shared_ptr<BatesDoubleExpModel>& model,
            Real relTolerance, Size maxEvaluations);

      protected:
        std::complex<Real> addOnTerm(Real phi, Time t, Size j) const override;
    };


    class BatesDoubleExpDetJumpEngine : public BatesDoubleExpEngine {
      public:
        explicit BatesDoubleExpDetJumpEngine(
            const ext::shared_ptr<BatesDoubleExpDetJumpModel>& model,
            Size integrationOrder = 144);
        BatesDoubleExpDetJumpEngine(
            const ext::shared_ptr<BatesDoubleExpDetJumpModel>& model,
            Real relTolerance, Size maxEvaluations);

      protected:
        std::complex<Real> addOnTerm(Real phi, Time t, Size j) const override;
    };

}

#endif