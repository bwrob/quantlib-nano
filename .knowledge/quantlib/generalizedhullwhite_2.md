+)
                sigma_.setParam(i, vol[i]);
            vol_ = voltraits.interpolate(volperiods_.begin(),
                volperiods_.end(),sigma_.params().begin());
            vol_.enableExtrapolation();
            sigmatemp.reset(vol_);

            generateArguments();
            registerWith(yieldtermStructure);
        }
    };

    //! Short-rate dynamics in the generalized Hull-White model
    /*! The short-rate is here

        f(r_t) = x_t + g(t)

        where g is the deterministic time-dependent
        parameter (which can't be determined analytically)
        used for initial term-structure fitting and  x_t is the state
        variable following an Ornstein-Uhlenbeck process.

        In this version, the function f may also be defined as a piece-wise linear
        function and can be calibrated to the away-from-the-money instruments.

    */
    class GeneralizedHullWhite::Dynamics
        : public GeneralizedHullWhite::ShortRateDynamics {
      public:
        Dynamics(Parameter fitting,
                 const std::function<Real(Time)>& alpha,
                 const std::function<Real(Time)>& sigma,
                 std::function<Real(Real)> f,
                 std::function<Real(Real)> fInverse)
        : ShortRateDynamics(ext::shared_ptr<StochasticProcess1D>(
              new GeneralizedOrnsteinUhlenbeckProcess(alpha, sigma))),
          fitting_(std::move(fitting)), _f_(std::move(f)), _fInverse_(std::move(fInverse)) {}

        //classical HW dynamics
        Dynamics(Parameter fitting, Real a, Real sigma)
        : GeneralizedHullWhite::ShortRateDynamics(
              ext::shared_ptr<StochasticProcess1D>(new OrnsteinUhlenbeckProcess(a, sigma))),
          fitting_(std::move(fitting)), _f_(identity()), _fInverse_(identity()) {}

        Real variable(Time t, Rate r) const override { return _f_(r) - fitting_(t); }

        Real shortRate(Time t, Real x) const override { return _fInverse_(x + fitting_(t)); }

      private:
        Parameter fitting_;
        std::function<Real(Real)> _f_;
        std::function<Real(Real)> _fInverse_;
        struct identity {
            Real operator()(Real x) const {return x;};
        };
    };

    //! Analytical term-structure fitting parameter \f$ \varphi(t) \f$.
    /*! \f$ \varphi(t) \f$ is analytically defined by
        \f[
            \varphi(t) = f(t) + \frac{1}{2}[\frac{\sigma(1-e^{-at})}{a}]^2,
        \f]
        where \f$ f(t) \f$ is the instantaneous forward rate at \f$ t \f$.
    */
    class GeneralizedHullWhite::FittingParameter
        : public TermStructureFittingParameter {
      private:
        class Impl final : public Parameter::Impl {
          public:
            Impl(Handle<YieldTermStructure> termStructure, Real a, Real sigma)
            : termStructure_(std::move(termStructure)), a_(a), sigma_(sigma) {}

            Real value(const Array&, Time t) const override {
                Rate forwardRate =
                    termStructure_->forwardRate(t, t, Continuous, NoFrequency);
                Real temp = a_ < std::sqrt(QL_EPSILON) ?
                            Real(sigma_*t) :
                            Real(sigma_*(1.0 - std::exp(-a_*t))/a_);
                return (forwardRate + 0.5*temp*temp);
            }

          private:
            Handle<YieldTermStructure> termStructure_;
            Real a_, sigma_;
        };
      public:
        FittingParameter(const Handle<YieldTermStructure>& termStructure,
                         Real a, Real sigma)
        : TermStructureFittingParameter(ext::shared_ptr<Parameter::Impl>(
                      new FittingParameter::Impl(termStructure, a, sigma))) {}
    };

    // Analytic fitting dynamics
    inline ext::shared_ptr<OneFactorModel::ShortRateDynamics>
    GeneralizedHullWhite::HWdynamics() const {
        return ext::shared_ptr<ShortRateDynamics>(
          new Dynamics(phi_, a(), sigma()));
    }

    namespace detail {
        template <class I1, class I2>
        class Linear
