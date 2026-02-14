tyCurve
        : public InterpolatedYoYOptionletVolatilityCurve<Interpolator>,
          public LazyObject {
      private:
        typedef InterpolatedYoYOptionletVolatilityCurve<Interpolator>
                                                                   base_curve;
        typedef PiecewiseYoYOptionletVolatilityCurve<Interpolator,
                                                     Bootstrap,
                                                     Traits> this_curve;
      public:
        typedef Traits traits_type;
        typedef Interpolator interpolator_type;

        PiecewiseYoYOptionletVolatilityCurve(
            Natural settlementDays,
            const Calendar& cal,
            BusinessDayConvention bdc,
            const DayCounter& dc,
            const Period& lag,
            Frequency frequency,
            bool indexIsInterpolated,
            Rate minStrike,
            Rate maxStrike,
            Volatility baseYoYVolatility,
            std::vector<ext::shared_ptr<typename Traits::helper> > instruments,
            Real accuracy = 1.0e-12,
            const Interpolator& interpolator = Interpolator())
        : base_curve(settlementDays,
                     cal,
                     bdc,
                     dc,
                     lag,
                     frequency,
                     indexIsInterpolated,
                     minStrike,
                     maxStrike,
                     baseYoYVolatility,
                     interpolator),
          instruments_(std::move(instruments)), accuracy_(accuracy) {
            bootstrap_.setup(this);
        }

        //! \name Inflation interface
        //@{
        Date baseDate() const override;
        Date maxDate() const override;
        //@
        //! \name Inspectors
        //@{
        const std::vector<Time>& times() const override;
        const std::vector<Date>& dates() const override;
        const std::vector<Real>& data() const override;
        std::vector<std::pair<Date, Real> > nodes() const override;
        //@}
        //! \name Observer interface
        //@{
        void update() override;
        //@}
      private:
        // methods
        void performCalculations() const override;
        // data members
        std::vector<ext::shared_ptr<typename Traits::helper> > instruments_;
        Real accuracy_;

        friend class Bootstrap<this_curve>;
        Bootstrap<this_curve> bootstrap_;
    };


    // inline and template definitions

    template <class I, template <class> class B, class T>
    inline Date PiecewiseYoYOptionletVolatilityCurve<I,B,T>::baseDate() const {
        this->calculate();
        return base_curve::baseDate();
    }

    template <class I, template <class> class B, class T>
    inline Date PiecewiseYoYOptionletVolatilityCurve<I,B,T>::maxDate() const {
        this->calculate();
        return base_curve::maxDate();
    }

    template <class I, template <class> class B, class T>
    const std::vector<Time>&
    PiecewiseYoYOptionletVolatilityCurve<I,B,T>::times() const {
        calculate();
        return base_curve::times();
    }

    template <class I, template <class> class B, class T>
    const std::vector<Date>&
    PiecewiseYoYOptionletVolatilityCurve<I,B,T>::dates() const {
        calculate();
        return base_curve::dates();
    }

    template <class I, template <class> class B, class T>
    const std::vector<Real>&
    PiecewiseYoYOptionletVolatilityCurve<I,B,T>::data() const {
        calculate();
        return base_curve::data();
    }

    template <class I, template <class> class B, class T>
    std::vector<std::pair<Date, Real> >
    PiecewiseYoYOptionletVolatilityCurve<I,B,T>::nodes() const {
        calculate();
        return base_curve::nodes();
    }

    template <class I, template <class> class B, class T>
    void
    PiecewiseYoYOptionletVolatilityCurve<I,B,T>::performCalculations() const {
        bootstrap_.calculate();
    }

    template <class I, templat