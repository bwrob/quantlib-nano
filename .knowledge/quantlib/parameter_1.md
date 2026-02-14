rivate:
        class Impl final : public Parameter::Impl {
          public:
            explicit Impl(std::vector<Time> times) : times_(std::move(times)) {}

            Real value(const Array& params, Time t) const override {
                Size i = std::upper_bound(times_.begin(), times_.end(), t) - times_.begin();
                return params[i];
            }

          private:
            std::vector<Time> times_;
        };
      public:
        PiecewiseConstantParameter(const std::vector<Time>& times,
                                   const Constraint& constraint =
                                                             NoConstraint())
        : Parameter(times.size()+1,
                    ext::shared_ptr<Parameter::Impl>(
                                 new PiecewiseConstantParameter::Impl(times)),
                    constraint)
        {}
    };

    //! Deterministic time-dependent parameter used for yield-curve fitting
    class TermStructureFittingParameter : public Parameter {
      public:
        class NumericalImpl : public Parameter::Impl {
          public:
            NumericalImpl(Handle<YieldTermStructure> termStructure)
            : times_(0), values_(0), termStructure_(std::move(termStructure)) {}

            void set(Time t, Real x) {
                times_.push_back(t);
                values_.push_back(x);
            }
            void change(Real x) {
                values_.back() = x;
            }
            void reset() {
                times_.clear();
                values_.clear();
            }
            Real value(const Array&, Time t) const override {
                auto result = std::find(times_.begin(), times_.end(), t);
                QL_REQUIRE(result!=times_.end(),
                           "fitting parameter not set!");
                return values_[result - times_.begin()];
            }
            const Handle<YieldTermStructure>& termStructure() const {
                return termStructure_;
            }
          private:
            std::vector<Time> times_;
            std::vector<Real> values_;
            Handle<YieldTermStructure> termStructure_;
        };

        TermStructureFittingParameter(
                               const ext::shared_ptr<Parameter::Impl>& impl)
        : Parameter(0, impl, NoConstraint()) {}

        TermStructureFittingParameter(const Handle<YieldTermStructure>& term)
        : Parameter(
                  0,
                  ext::shared_ptr<Parameter::Impl>(new NumericalImpl(term)),
                  NoConstraint())
        {}
    };

}


#endif
