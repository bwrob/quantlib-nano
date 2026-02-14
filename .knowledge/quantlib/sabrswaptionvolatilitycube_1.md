  const std::vector<Time>& optionTimes() const;
            const std::vector<Time>& swapLengths() const;
            const std::vector<Matrix>& points() const;
            std::vector<Real> operator()(Time optionTime, Time swapLengths) const;
            void updateInterpolators()const;
            Matrix browse() const;
          private:
            std::vector<Time> optionTimes_, swapLengths_;
            std::vector<Date> optionDates_;
            std::vector<Period> swapTenors_;
            Size nLayers_;
            std::vector<Matrix> points_;
            mutable std::vector<Matrix> transposedPoints_;
            bool extrapolation_;
            bool backwardFlat_;
            mutable std::vector< ext::shared_ptr<Interpolation2D> > interpolators_;
         };
      public:
        XabrSwaptionVolatilityCube(
            const Handle<SwaptionVolatilityStructure>& atmVolStructure,
            const std::vector<Period>& optionTenors,
            const std::vector<Period>& swapTenors,
            const std::vector<Spread>& strikeSpreads,
            const std::vector<std::vector<Handle<Quote> > >& volSpreads,
            const ext::shared_ptr<SwapIndex>& swapIndexBase,
            const ext::shared_ptr<SwapIndex>& shortSwapIndexBase,
            bool vegaWeightedSmileFit,
            std::vector<std::vector<Handle<Quote> > > parametersGuess,
            std::vector<bool> isParameterFixed,
            bool isAtmCalibrated,
            ext::shared_ptr<EndCriteria> endCriteria = ext::shared_ptr<EndCriteria>(),
            Real maxErrorTolerance = Null<Real>(),
            ext::shared_ptr<OptimizationMethod> optMethod = ext::shared_ptr<OptimizationMethod>(),
            Real errorAccept = Null<Real>(),
            bool useMaxError = false,
            Size maxGuesses = 50,
            bool backwardFlat = false,
            Real cutoffStrike = 0.0001);
        //! \name LazyObject interface
        //@{
        void performCalculations() const override;
        //@}
        //! \name SwaptionVolatilityCube interface
        //@{
        ext::shared_ptr<SmileSection> smileSectionImpl(Time optionTime,
                                                       Time swapLength) const override;
        //@}
        //! \name Other inspectors
        //@{
        const Matrix& marketVolCube(Size i) const {
            return marketVolCube_.points()[i];
        }
        Matrix sparseSabrParameters()const;
        Matrix denseSabrParameters() const;
        Matrix marketVolCube() const;
        Matrix volCubeAtmCalibrated() const;
        //@}
        void sabrCalibrationSection(const Cube& marketVolCube,
                                    Cube& parametersCube,
                                    const Period& swapTenor) const;
        void recalibration(Real beta,
                           const Period& swapTenor);
        void recalibration(const std::vector<Real> &beta,
                           const Period& swapTenor);
        void recalibration(const std::vector<Period> &swapLengths,
                           const std::vector<Real> &beta,
                           const Period& swapTenor);
        void updateAfterRecalibration();
     protected:
        void registerWithParametersGuess();
        void setParameterGuess() const;
        ext::shared_ptr<SmileSection> smileSection(
                                    Time optionTime,
                                    Time swapLength,
                                    const Cube& sabrParametersCube) const;
        Cube sabrCalibration(const Cube &marketVolCube) const;
        void fillVolatilityCube() const;
        void createSparseSmiles() const;
        std::vector<Real> spreadVolInterpolation(const Date& atmOptionDate,
                                                 const Period& atmSwapTenor) const;
      private:
        Size requiredNumberOfStrikes() const override { return 1; }
        mutable Cube marketVolCube_;
        mutable Cube volCubeAtmCalibrated_;
        mu