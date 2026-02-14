 const;
        //! forward (at-the-money) variance
        Real blackForwardVariance(const Date& date1,
                                  const Date& date2,
                                  Real strike,
                                  bool extrapolate = false) const;
        //! forward (at-the-money) variance
        Real blackForwardVariance(Time time1,
                                  Time time2,
                                  Real strike,
                                  bool extrapolate = false) const;
        //@}
        //! \name Visitability
        //@{
        virtual void accept(AcyclicVisitor&);
        //@}
      protected:
        /*! \name Calculations

            These methods must be implemented in derived classes to perform
            the actual volatility calculations. When they are called,
            range check has already been performed; therefore, they must
            assume that extrapolation is required.
        */
        //@{
        //! Black variance calculation
        virtual Real blackVarianceImpl(Time t, Real strike) const = 0;
        //! Black volatility calculation
        virtual Volatility blackVolImpl(Time t, Real strike) const = 0;
        //@}
    };

    //! Black-volatility term structure
    /*! This abstract class acts as an adapter to BlackVolTermStructure
        allowing the programmer to implement only the
        <tt>blackVolImpl(Time, Real, bool)</tt> method in derived classes.

        Volatility are assumed to be expressed on an annual basis.
    */
    class BlackVolatilityTermStructure : public BlackVolTermStructure {
      public:
        /*! \name Constructors
            See the TermStructure documentation for issues regarding
            constructors.
        */
        //@{
        //! default constructor
        /*! \warning term structures initialized by means of this
                     constructor must manage their own reference date
                     by overriding the referenceDate() method.
        */
        BlackVolatilityTermStructure(BusinessDayConvention bdc = Following,
                                     const DayCounter& dc = DayCounter());
        //! initialize with a fixed reference date
        BlackVolatilityTermStructure(const Date& referenceDate,
                                     const Calendar& cal = Calendar(),
                                     BusinessDayConvention bdc = Following,
                                     const DayCounter& dc = DayCounter());
        //! calculate the reference date based on the global evaluation date
        BlackVolatilityTermStructure(Natural settlementDays,
                                     const Calendar& cal,
                                     BusinessDayConvention bdc = Following,
                                     const DayCounter& dc = DayCounter());
        //@}
        //! \name Visitability
        //@{
        void accept(AcyclicVisitor&) override;
        //@}
      protected:
        /*! Returns the variance for the given strike and date calculating it
            from the volatility.
        */
        Real blackVarianceImpl(Time maturity, Real strike) const override;
    };


    //! Black variance term structure
    /*! This abstract class acts as an adapter to VolTermStructure allowing
        the programmer to implement only the
        <tt>blackVarianceImpl(Time, Real, bool)</tt> method in derived
        classes.

        Volatility are assumed to be expressed on an annual basis.
    */
    class BlackVarianceTermStructure : public BlackVolTermStructure {
      public:
        /*! \name Constructors
            See the TermStructure documentation for issues regarding
            constructors.
        */
        //@{
        //! default constructor
        /*! \warning term structures initialized by means of this
                     constructor must manage their own reference date
                     by overriding the referenceDate() method.
        */
        