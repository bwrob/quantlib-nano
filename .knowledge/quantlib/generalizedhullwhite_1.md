    {
            initialize(yieldtermStructure,speedstructure,volstructure,
                speed,vol,speedtraits,voltraits,f,fInverse);
        }

        ext::shared_ptr<ShortRateDynamics> dynamics() const override {
            QL_FAIL("no defined process for generalized Hull-White model, "
                    "use HWdynamics()");
        }

        ext::shared_ptr<Lattice> tree(const TimeGrid& grid) const override;

        //Analytical calibration of HW

        GeneralizedHullWhite(
                  const Handle<YieldTermStructure>& yieldtermStructure,
                  Real a = 0.1, Real sigma = 0.01);


        ext::shared_ptr<ShortRateDynamics> HWdynamics() const;

        //! Only valid under Hull-White model
        Real discountBondOption(Option::Type type,
                                Real strike,
                                Time maturity,
                                Time bondMaturity) const override;

        //! vector to pass to 'calibrate' to fit only volatility
        std::vector<bool> fixedReversion() const;

      protected:
        //Analytical calibration of HW
        Real a() const { return a_(0.0); }
        Real sigma() const { return sigma_(0.0); }
        void generateArguments() override;
        Real A(Time t, Time T) const override;
        Real B(Time t, Time T) const override;
        Real V(Time t, Time T) const;

      private:

        class Dynamics;
        class Helper;
        class FittingParameter;// for analytic HW fitting

        std::vector<Date> speedstructure_;
        std::vector<Date> volstructure_;
        std::vector<Time> speedperiods_;
        std::vector<Time> volperiods_;
        Interpolation speed_;
        Interpolation vol_;

        std::function<Real (Time)> speed() const;
        std::function<Real (Time)> vol() const;

        Parameter& a_;
        Parameter& sigma_;
        Parameter phi_;

        std::function<Real(Real)> f_;
        std::function<Real(Real)> fInverse_;

        static Real identity(Real x) {
            return x;
        }

        template <class SpeedInterpolationTraits,class VolInterpolationTraits>
        void initialize(const Handle<YieldTermStructure>& yieldtermStructure,
            const std::vector<Date>& speedstructure,
            const std::vector<Date>& volstructure,
            const std::vector<Real>& speed,
            const std::vector<Real>& vol,
            const SpeedInterpolationTraits &speedtraits,
            const VolInterpolationTraits &voltraits,
            const std::function<Real(Real)>& f,
            const std::function<Real(Real)>& fInverse)
        {
            QL_REQUIRE(speedstructure.size()==speed.size(),
                "mean reversion inputs inconsistent");
            QL_REQUIRE(volstructure.size()==vol.size(),
                "volatility inputs inconsistent");
            if (!f_)
                f_ = identity;
            if (!fInverse_)
                fInverse_ = identity;

            DayCounter dc = yieldtermStructure->dayCounter();
            Date ref = yieldtermStructure->referenceDate();
            for (auto i : speedstructure)
                speedperiods_.push_back(dc.yearFraction(ref, i));
            for (auto i : volstructure)
                volperiods_.push_back(dc.yearFraction(ref, i));

            // interpolator x points to *periods_ vector, y points to
            // the internal Array in the parameter
            InterpolationParameter atemp(speedperiods_.size(), NoConstraint());
            a_ = atemp;
            for (Size i=0; i<speedperiods_.size(); i++)
                a_.setParam(i, speed[i]);
            speed_ = speedtraits.interpolate(speedperiods_.begin(),
                speedperiods_.end(),a_.params().begin());
            speed_.enableExtrapolation();
            atemp.reset(speed_);

            InterpolationParameter sigmatemp(volperiods_.size(), PositiveConstraint());
            sigma_ = sigmatemp;
            for (Size i=0; i<volperiods_.size(); i+