        PiecewiseYieldCurve(const Date& referenceDate,
                            std::vector<ext::shared_ptr<typename Traits::helper> > instruments,
                            const DayCounter& dayCounter,
                            bootstrap_type bootstrap)
        : PiecewiseYieldCurve(std::move(instruments), std::move(bootstrap),
                              referenceDate, dayCounter) {}

        PiecewiseYieldCurve(
            Natural settlementDays,
            const Calendar& calendar,
            std::vector<ext::shared_ptr<typename Traits::helper> > instruments,
            const DayCounter& dayCounter,
            const std::vector<Handle<Quote> >& jumps = {},
            const std::vector<Date>& jumpDates = {},
            const Interpolator& i = {},
            bootstrap_type bootstrap = {})
        : PiecewiseYieldCurve(std::move(instruments), std::move(bootstrap),
                              settlementDays, calendar, dayCounter, jumps, jumpDates, i) {}

        PiecewiseYieldCurve(Natural settlementDays,
                            const Calendar& calendar,
                            std::vector<ext::shared_ptr<typename Traits::helper> > instruments,
                            const DayCounter& dayCounter,
                            const Interpolator& i,
                            bootstrap_type bootstrap = {})
        : PiecewiseYieldCurve(std::move(instruments), std::move(bootstrap),
                              settlementDays, calendar, dayCounter,
                              std::vector<Handle<Quote>>(), std::vector<Date>(), i) {}

        PiecewiseYieldCurve(
               Natural settlementDays,
               const Calendar& calendar,
               std::vector<ext::shared_ptr<typename Traits::helper> > instruments,
               const DayCounter& dayCounter,
               bootstrap_type bootstrap)
        : PiecewiseYieldCurve(std::move(instruments), std::move(bootstrap),
                              settlementDays, calendar, dayCounter) {}
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
        const MultiCurveBootstrapContributor* multiCurveBootstrapContributor() const override {
            if constexpr (std::is_convertible_v<bootstrap_type*, MultiCurveBootstrapContributor*>) {
                return &bootstrap_;
            } else {
                return nullptr;
            }
        }

      protected:
        template <class... Args>
        PiecewiseYieldCurve(
            std::vector<ext::shared_ptr<typename Traits::helper>> instruments,
            bootstrap_type bootstrap,
            Args&&... args)
        : base_curve(std::forward<Args>(args)...), instruments_(std::move(instruments)),
          accuracy_(1.0e-12), bootstrap_(std::move(bootstrap)) {
            bootstrap_.setup(this);
        }
      private:
        //! \name LazyObject interface
        //@{
        void performCalculations() const override;
        //@}
        // methods
        DiscountFactor discountImpl(Time) const override;
        // data members
        std::vector<ext::shared_ptr<typename Traits::helper> > instruments_;
        Real accuracy_;

        // bootstrapper classes are declared as friend to manipulate
        // the curve data. They might be passed the data instead, but
        // it would increase the complexity---which is high enough
        // already.
        friend class Bootstrap<this_curve>;
        Bootstrap<this_curve> bootstrap_;
    };


    // inline definitions

    template <class C, class I, template <class> class B>
    inline Date PiecewiseYi