                                const Interpolator& interpolator);
        //! \name TermStructure interface
        //@{
        Date maxDate() const override;
        //@}
        //! \name other inspectors
        //@{
        const std::vector<Time>& times() const;
        const std::vector<Date>& dates() const;
        const std::vector<Real>& data() const;
        const std::vector<Rate>& hazardRates() const;
        std::vector<std::pair<Date, Real> > nodes() const;
        //@}
      protected:
        InterpolatedAffineHazardRateCurve(
            const DayCounter&,
            const ext::shared_ptr<OneFactorAffineModel>& model,
            const std::vector<Handle<Quote> >& jumps = std::vector<Handle<Quote> >(),
            const std::vector<Date>& jumpDates = std::vector<Date>(),
            const Interpolator& interpolator = Interpolator());
        InterpolatedAffineHazardRateCurve(
            const Date& referenceDate,
            const DayCounter&,
            const ext::shared_ptr<OneFactorAffineModel>& model,
            const std::vector<Handle<Quote> >& jumps = std::vector<Handle<Quote> >(),
            const std::vector<Date>& jumpDates = std::vector<Date>(),
            const Interpolator& interpolator = Interpolator());
        InterpolatedAffineHazardRateCurve(
            Natural settlementDays,
            const Calendar&,
            const DayCounter&,
            const ext::shared_ptr<OneFactorAffineModel>& model,
            const std::vector<Handle<Quote> >& jumps = std::vector<Handle<Quote> >(),
            const std::vector<Date>& jumpDates = std::vector<Date>(),
            const Interpolator& interpolator = Interpolator());
        //! \name DefaultProbabilityTermStructure implementation
        //@{
        //! Returns the deterministic hazard rate component.
        Real hazardRateImpl(Time) const override;
        Probability survivalProbabilityImpl(Time) const override;

      public:
        using DefaultProbabilityTermStructure::hazardRate;
    protected:
        /*! Probability of default conditional to the realization of a given
        value of the stochastic part of the hazard rate at a prior time (and
        thus to survival at that time).
        \f$ P_{surv}(\tau>tTarget|F_{tFwd}) \f$
        */
      Probability
      conditionalSurvivalProbabilityImpl(Time tFwd, Time tTarget, Real yVal) const override;
      //@}

      mutable std::vector<Date> dates_;

    private:
      void initialize();
    };


    namespace detail {
        // hazard rate compensation TS for affine models
        const Real minHazardRateComp = -1.0;
    }

    /*! Piecewise (deterministic) plus affine (stochastic) terms composed
        hazard rate
    */
    struct AffineHazardRate {
        // interpolated curve type
        template <class Interpolator>
        struct curve {
            typedef InterpolatedAffineHazardRateCurve<Interpolator> type;
        };
        // helper class
        typedef BootstrapHelper<DefaultProbabilityTermStructure> helper;

        // start of curve data
        static Date initialDate(const DefaultProbabilityTermStructure* c) {
            return c->referenceDate();
        }
        // dummy value at reference date
        static Real initialValue(const DefaultProbabilityTermStructure*) {
            return detail::avgHazardRate;
        }

        // guesses
        template <class C>
        static Real guess(Size i,
                          const C* c,
                          bool validData,
                          Size) // firstAliveHelper
        {
            if (validData) // previous iteration value
                return c->data()[i];

            if (i==1) // first pillar
                return 0.0001;
               // return detail::avgHazardRate;

            // extrapolate
            Date d = c->dates()[i];
            /* Uneasy about the naming: Here we are bootstrapping only the
             deterministic part of the intensity it might be a bette
