           std::numeric_limits < Array::value_type > ::max());
            }
            Array lowerBound(const Array& params) const override {
                return Array(params.size(), 0.0);
            }
        };
      public:
        PositiveConstraint()
        : Constraint(ext::shared_ptr<Constraint::Impl>(
                                             new PositiveConstraint::Impl)) {}
    };

    //! %Constraint imposing all arguments to be in [low,high]
    class BoundaryConstraint : public Constraint {
      private:
        class Impl final : public Constraint::Impl {
          public:
            Impl(Real low, Real high)
            : low_(low), high_(high) {}
            bool test(const Array& params) const override {
                return std::all_of(params.begin(), params.end(), [this](Real p) { return low_ <= p && p <= high_; });
            }
            Array upperBound(const Array& params) const override {
                return Array(params.size(), high_);
            }
            Array lowerBound(const Array& params) const override {
                return Array(params.size(), low_);
            }

          private:
            Real low_, high_;
        };
      public:
        BoundaryConstraint(Real low, Real high)
        : Constraint(ext::shared_ptr<Constraint::Impl>(
                                  new BoundaryConstraint::Impl(low, high))) {}
    };

    //! %Constraint enforcing both given sub-constraints
    class CompositeConstraint : public Constraint {
      private:
        class Impl final : public Constraint::Impl {
          public:
            Impl(Constraint c1, Constraint c2) : c1_(std::move(c1)), c2_(std::move(c2)) {}
            bool test(const Array& params) const override {
                return c1_.test(params) && c2_.test(params);
            }
            Array upperBound(const Array& params) const override {
                Array c1ub = c1_.upperBound(params);
                Array c2ub = c2_.upperBound(params);
                Array rtrnArray(c1ub.size(), 0.0);
                for (Size iter = 0; iter < c1ub.size(); iter++) {
                    rtrnArray.at(iter) = std::min(c1ub.at(iter), c2ub.at(iter));
                }
                return rtrnArray;
            }
            Array lowerBound(const Array& params) const override {
                Array c1lb = c1_.lowerBound(params);
                Array c2lb = c2_.lowerBound(params);
                Array rtrnArray(c1lb.size(), 0.0);
                for (Size iter = 0; iter < c1lb.size(); iter++) {
                    rtrnArray.at(iter) = std::max(c1lb.at(iter), c2lb.at(iter));
                }
                return rtrnArray;
            }

          private:
            Constraint c1_, c2_;
        };
      public:
        CompositeConstraint(const Constraint& c1, const Constraint& c2)
        : Constraint(ext::shared_ptr<Constraint::Impl>(
                                     new CompositeConstraint::Impl(c1,c2))) {}
    };

    //! %Constraint imposing i-th argument to be in [low_i,high_i] for all i
    class NonhomogeneousBoundaryConstraint: public Constraint {
      private:
        class Impl final : public Constraint::Impl {
          public:
            Impl(Array low, Array high) : low_(std::move(low)), high_(std::move(high)) {
                QL_ENSURE(low_.size()==high_.size(),
                          "Upper and lower boundaries sizes are inconsistent.");
            }
            bool test(const Array& params) const override {
                QL_ENSURE(params.size()==low_.size(),
                          "Number of parameters and boundaries sizes are inconsistent.");
                for (Size i = 0; i < params.size(); i++) {
                    if ((params[i] < low_[i]) || (params[i] > high_[i]))
                        return false;
                }
                return true;
            }
            Array upperBound(const Array&) const override { return high_; }
            Array lowerBound(co