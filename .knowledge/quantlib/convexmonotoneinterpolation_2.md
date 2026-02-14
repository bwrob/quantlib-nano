mpl<I1, I2> {
            typedef std::map<Real, ext::shared_ptr<SectionHelper> >
                                                                   helper_map;
          public:
            enum SectionType {
                EverywhereConstant,
                ConstantGradient,
                QuadraticMinimum,
                QuadraticMaximum
            };

            ConvexMonotoneImpl(const I1& xBegin,
                               const I1& xEnd,
                               const I2& yBegin,
                               Real quadraticity,
                               Real monotonicity,
                               bool forcePositive,
                               bool constantLastPeriod,
                               const helper_map& preExistingHelpers)
            : Interpolation::templateImpl<I1,I2>(xBegin,xEnd,yBegin,
                                                 ConvexMonotone::requiredPoints),
              preSectionHelpers_(preExistingHelpers),
              forcePositive_(forcePositive),
              constantLastPeriod_(constantLastPeriod),
              quadraticity_(quadraticity), monotonicity_(monotonicity),
              length_(xEnd-xBegin) {

                QL_REQUIRE(monotonicity_ >= 0 && monotonicity_ <= 1,
                           "Monotonicity must lie between 0 and 1");
                QL_REQUIRE(quadraticity_ >= 0 && quadraticity_ <= 1,
                           "Quadraticity must lie between 0 and 1");
                QL_REQUIRE(length_ >= 2,
                           "Single point provided, not supported by convex "
                           "monotone method as first point is ignored");
                QL_REQUIRE((length_ - preExistingHelpers.size()) > 1,
                            "Too many existing helpers have been supplied");
            }

            void update() override;

            Real value(Real x) const override;
            Real primitive(Real x) const override;
            Real derivative(Real) const override {
                QL_FAIL("Convex-monotone spline derivative not implemented");
            }
            Real secondDerivative(Real) const override {
                QL_FAIL("Convex-monotone spline second derivative "
                        "not implemented");
            }

            helper_map getExistingHelpers() {
                helper_map retArray(sectionHelpers_);
                if (constantLastPeriod_)
                    retArray.erase(*(this->xEnd_-1));
                return retArray;
            }
          private:
            helper_map sectionHelpers_;
            helper_map preSectionHelpers_;
            ext::shared_ptr<SectionHelper> extrapolationHelper_;
            bool forcePositive_, constantLastPeriod_;
            Real quadraticity_;
            Real monotonicity_;
            Size length_;
        };


        class ComboHelper : public SectionHelper {
          public:
            ComboHelper(ext::shared_ptr<SectionHelper>& quadraticHelper,
                        ext::shared_ptr<SectionHelper>& convMonoHelper,
                        Real quadraticity)
            : quadraticity_(quadraticity),
              quadraticHelper_(quadraticHelper),
              convMonoHelper_(convMonoHelper) {
                QL_REQUIRE(quadraticity < 1.0 && quadraticity > 0.0,
                           "Quadratic value must lie between 0 and 1"); }

            Real value(Real x) const override {
                return( quadraticity_*quadraticHelper_->value(x) + (1.0-quadraticity_)*convMonoHelper_->value(x) );
            }
            Real primitive(Real x) const override {
                return( quadraticity_*quadraticHelper_->primitive(x) + (1.0-quadraticity_)*convMonoHelper_->primitive(x) );
            }
            Real fNext() const override {
                return( quadraticity_*quadraticHelper_->fNext() + (1.0-quadraticity_)*convMonoHelper_->fNext() );
            }

          private:
            Real quadraticity_;
            e