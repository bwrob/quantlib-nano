t::shared_ptr<BondHelper> > bonds,
                                const DayCounter& dayCounter,
                                const FittingMethod& fittingMethod,
                                Real accuracy = 1.0e-10,
                                Size maxEvaluations = 10000,
                                Array guess = Array(),
                                Real simplexLambda = 1.0,
                                Size maxStationaryStateIterations = 100);

        //! curve reference date fixed for life of curve
        FittedBondDiscountCurve(const Date& referenceDate,
                                std::vector<ext::shared_ptr<BondHelper> > bonds,
                                const DayCounter& dayCounter,
                                const FittingMethod& fittingMethod,
                                Real accuracy = 1.0e-10,
                                Size maxEvaluations = 10000,
                                Array guess = Array(),
                                Real simplexLambda = 1.0,
                                Size maxStationaryStateIterations = 100);

        //! don't fit, use precalculated parameters
        FittedBondDiscountCurve(Natural settlementDays,
                                const Calendar& calendar,
                                const FittingMethod& fittingMethod,
                                Array parameters,
                                Date maxDate,
                                const DayCounter& dayCounter);

        //! don't fit, use precalculated parameters
        FittedBondDiscountCurve(const Date& referenceDate,
                                const FittingMethod& fittingMethod,
                                Array parameters,
                                Date maxDate,
                                const DayCounter& dayCounter);
        //@}

        //! \name Inspectors
        //@{
        //! total number of bonds used to fit the yield curve
        Size numberOfBonds() const;
        //! the latest date for which the curve can return values
        Date maxDate() const override;
        //! class holding the results of the fit
        const FittingMethod& fitResults() const;
        //@}

        //! \name Other utilities
        //@{
        /*! This allows to try out multiple guesses and avoid local minima */
        void resetGuess(const Array& guess);
        //@}

        //! \name Observer interface
        //@{
        void update() override;
        //@}

      private:
        void setup();
        void performCalculations() const override;
        DiscountFactor discountImpl(Time) const override;
        // target accuracy level to be used in the optimization routine
        Real accuracy_;
        // max number of evaluations to be used in the optimization routine
        Size maxEvaluations_;
        // sets the scale in the (Simplex) optimization routine
        Real simplexLambda_;
        // max number of evaluations where no improvement to solution is made
        Size maxStationaryStateIterations_;
        // a guess solution may be passed into the constructor to speed calcs
        Array guessSolution_;
        mutable Date maxDate_;
        std::vector<ext::shared_ptr<BondHelper> > bondHelpers_;
        Clone<FittingMethod> fittingMethod_;
    };


    //! Base fitting method used to construct a fitted bond discount curve
    /*! This base class provides the specific methodology/strategy
        used to construct a FittedBondDiscountCurve.  Derived classes
        need only define the virtual function discountFunction() based
        on the particular fitting method to be implemented, as well as
        size(), the number of variables to be solved for/optimized. The
        generic fitting methodology implemented here can be termed
        nonlinear, in contrast to (typically faster, computationally)
        linear fitting method.

        Optional parameters for FittingMethod include an Array of
        weights, which will be u