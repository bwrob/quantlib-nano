ename Traits::helper> > instruments,
                              const DayCounter& dayCounter,
                              bootstrap_type bootstrap)
        : base_curve(referenceDate,
                     dayCounter),
          instruments_(std::move(instruments)), accuracy_(1.0e-12),
          bootstrap_(std::move(bootstrap)) {
            bootstrap_.setup(this);
        }

        PiecewiseDefaultCurve(
            Natural settlementDays,
            const Calendar& calendar,
            std::vector<ext::shared_ptr<typename Traits::helper> > instruments,
            const DayCounter& dayCounter,
            const std::vector<Handle<Quote> >& jumps = {},
            const std::vector<Date>& jumpDates = {},
            const Interpolator& i = {},
            bootstrap_type bootstrap = {})
        : base_curve(settlementDays, calendar, dayCounter, jumps, jumpDates, i),
          instruments_(std::move(instruments)), accuracy_(1.0e-12),
          bootstrap_(std::move(bootstrap)) {
            bootstrap_.setup(this);
        }

        PiecewiseDefaultCurve(
               Natural settlementDays,
               const Calendar& calendar,
               const std::vector<ext::shared_ptr<typename Traits::helper> >&
                                                                  instruments,
               const DayCounter& dayCounter,
               const Interpolator& i,
               const bootstrap_type& bootstrap = bootstrap_type())
        : base_curve(settlementDays, calendar, dayCounter,
                     {}, {}, i),
          instruments_(instruments), accuracy_(1.0e-12), bootstrap_(bootstrap) {
            bootstrap_.setup(this);
        }

        PiecewiseDefaultCurve(
               Natural settlementDays,
               const Calendar& calendar,
               const std::vector<ext::shared_ptr<typename Traits::helper> >&
                                                                  instruments,
               const DayCounter& dayCounter,
               const bootstrap_type& bootstrap)
        : base_curve(settlementDays, calendar, dayCounter),
          instruments_(instruments), accuracy_(1.0e-12), bootstrap_(bootstrap) {
            bootstrap_.setup(this);
        }

        /* AffineHazardRate Traits constructor case. Other constructors of
        base_curve would fail and this would fail for other cases of Traits.
        This is a case of substitution failure, it might be preferred
        to specialization of the class.
        The way the methods are used in the bootstrapping means the target
        term structure is the deterministic TS to be added to the model
        passed in order to reproduce instrument market prices.

        \todo Implement the remaining signatures
        */
        PiecewiseDefaultCurve(
            const Date& referenceDate,
            const std::vector<ext::shared_ptr<typename Traits::helper> >& instruments,
            const DayCounter& dayCounter,
            const ext::shared_ptr<OneFactorAffineModel>& model,
            const Interpolator& i = {},
            const bootstrap_type& bootstrap = {})
        : base_curve(referenceDate,
                     dayCounter,
                     model,
                     {},
                     {},
                     i),
          instruments_(instruments), accuracy_(1.0e-12), bootstrap_(bootstrap) {
            bootstrap_.setup(this);
        }
        //@}
        //! \name TermStructure interface
        //@{
        Date maxDate() const override;
        //@}
        //! \name base_curve interface
        //@{
        const std::vector<Time>& times() const;
        const std::vector<Date>& dates() const;
        const std::vector<Real>& data() const;
        std::vector<std::pair<Date, Real> > nodes() const;
        //@}
        //! \name Observer interface
        //@{
        void update() override;
        //@}
      private:
        //! \name LazyObject interface
        //@{
        void performCalculations() 