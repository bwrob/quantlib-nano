                           const Calendar& calendar,
                                 BusinessDayConvention bdc,
                                 const std::vector<Period>& optionTenors,
                                 const std::vector<Period>& swapTenors,
                                 const Matrix& volatilities,
                                 const DayCounter& dayCounter,
                                 bool flatExtrapolation = false,
                                 VolatilityType type = ShiftedLognormal,
                                 const Matrix& shifts = Matrix());
        //! fixed reference date and fixed market data, option dates
        SwaptionVolatilityMatrix(const Date& referenceDate,
                                 const Calendar& calendar,
                                 BusinessDayConvention bdc,
                                 const std::vector<Date>& optionDates,
                                 const std::vector<Period>& swapTenors,
                                 const Matrix& volatilities,
                                 const DayCounter& dayCounter,
                                 bool flatExtrapolation = false,
                                 VolatilityType type = ShiftedLognormal,
                                 const Matrix& shifts = Matrix());

        // make class non-copyable and non-movable
        SwaptionVolatilityMatrix(SwaptionVolatilityMatrix&&) = delete;
        SwaptionVolatilityMatrix(const SwaptionVolatilityMatrix&) = delete;
        SwaptionVolatilityMatrix& operator=(SwaptionVolatilityMatrix&&) = delete;
        SwaptionVolatilityMatrix& operator=(const SwaptionVolatilityMatrix&) = delete;

        ~SwaptionVolatilityMatrix() override = default;

        //! \name LazyObject interface
        //@{
        void performCalculations() const override;
        //@}
        //! \name TermStructure interface
        //@{
        Date maxDate() const override;
        //@}
        //! \name VolatilityTermStructure interface
        //@{
        Rate minStrike() const override;
        Rate maxStrike() const override;
        //@}
        //! \name SwaptionVolatilityStructure interface
        //@{
        const Period& maxSwapTenor() const override;
        //@}
        //! \name Other inspectors
        //@{
        //! returns the lower indexes of surrounding volatility matrix corners
        std::pair<Size,Size> locate(const Date& optionDate,
                                    const Period& swapTenor) const {
            return locate(timeFromReference(optionDate),
                          swapLength(swapTenor));
        }
        //! returns the lower indexes of surrounding volatility matrix corners
        std::pair<Size,Size> locate(Time optionTime,
                                    Time swapLength) const {
            return std::make_pair(interpolation_.locateY(optionTime),
                                  interpolation_.locateX(swapLength));
        }
        //@}
        VolatilityType volatilityType() const override;

      protected:
        // defining the following method would break CMS test suite
        // to be further investigated
        //ext::shared_ptr<SmileSection> smileSectionImpl(const Date&,
        //                                                 const Period&) const;
        ext::shared_ptr<SmileSection> smileSectionImpl(Time, Time) const override;
        Volatility volatilityImpl(Time optionTime, Time swapLength, Rate strike) const override;
        Real shiftImpl(Time optionTime, Time swapLength) const override;

      private:
        void checkInputs(Size volRows,
                         Size volsColumns,
                         Size shiftRows,
                         Size shiftsColumns) const;
        void registerWithMarketData();
        std::vector<std::vector<Handle<Quote> > > volHandles_;
        std::vector<std::vector<Real> > shiftValues_;
        mutable Matrix volatilities_, shifts_;
        Interpolation2D interpolation_,
