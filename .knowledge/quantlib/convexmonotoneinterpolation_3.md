xt::shared_ptr<SectionHelper> quadraticHelper_;
            ext::shared_ptr<SectionHelper> convMonoHelper_;
        };

        class EverywhereConstantHelper : public SectionHelper {
          public:
            EverywhereConstantHelper(Real value, Real prevPrimitive, Real xPrev)
            : value_(value), prevPrimitive_(prevPrimitive), xPrev_(xPrev)
            {}

            Real value(Real) const override { return value_; }
            Real primitive(Real x) const override { return prevPrimitive_ + (x - xPrev_) * value_; }
            Real fNext() const override { return value_; }

          private:
            Real value_;
            Real prevPrimitive_;
            Real xPrev_;
        };

        class ConvexMonotone2Helper : public SectionHelper {
          public:
            ConvexMonotone2Helper(Real xPrev, Real xNext,
                                  Real gPrev, Real gNext,
                                  Real fAverage, Real eta2,
                                  Real prevPrimitive)
            : xPrev_(xPrev), xScaling_(xNext-xPrev), gPrev_(gPrev),
              gNext_(gNext), fAverage_(fAverage), eta2_(eta2),
              prevPrimitive_(prevPrimitive)
            {}

            Real value(Real x) const override {
                Real xVal = (x-xPrev_)/xScaling_;
                if (xVal <= eta2_) {
                    return( fAverage_ + gPrev_ );
                } else {
                    return( fAverage_ + gPrev_ + (gNext_-gPrev_)/((1-eta2_)*(1-eta2_))*(xVal-eta2_)*(xVal-eta2_) );
                }
            }

            Real primitive(Real x) const override {
                Real xVal = (x-xPrev_)/xScaling_;
                if (xVal <= eta2_) {
                    return( prevPrimitive_ + xScaling_*(fAverage_*xVal + gPrev_*xVal) );
                } else {
                    return( prevPrimitive_ + xScaling_*(fAverage_*xVal + gPrev_*xVal + (gNext_-gPrev_)/((1-eta2_)*(1-eta2_)) *
                            (1.0/3.0*(xVal*xVal*xVal - eta2_*eta2_*eta2_) - eta2_*xVal*xVal + eta2_*eta2_*xVal) ) );
                }
            }
            Real fNext() const override { return (fAverage_ + gNext_); }

          private:
            Real xPrev_, xScaling_, gPrev_, gNext_, fAverage_, eta2_, prevPrimitive_;
        };

        class ConvexMonotone3Helper : public SectionHelper {
          public:
            ConvexMonotone3Helper(Real xPrev, Real xNext,
                                  Real gPrev, Real gNext,
                                  Real fAverage, Real eta3,
                                  Real prevPrimitive)
              : xPrev_(xPrev), xScaling_(xNext-xPrev), gPrev_(gPrev),
                gNext_(gNext), fAverage_(fAverage), eta3_(eta3), prevPrimitive_(prevPrimitive)
            {}

            Real value(Real x) const override {
                Real xVal = (x-xPrev_)/xScaling_;
                if (xVal <= eta3_) {
                    return( fAverage_ + gNext_ + (gPrev_-gNext_) / (eta3_*eta3_) * (eta3_-xVal)*(eta3_-xVal) );
                } else {
                    return( fAverage_ + gNext_ );
                }
            }

            Real primitive(Real x) const override {
                Real xVal = (x-xPrev_)/xScaling_;
                if (xVal <= eta3_) {
                    return( prevPrimitive_ + xScaling_ * (fAverage_*xVal + gNext_*xVal + (gPrev_-gNext_)/(eta3_*eta3_) *
                            (1.0/3.0 * xVal*xVal*xVal - eta3_*xVal*xVal + eta3_*eta3_*xVal) ) );
                } else {
                    return( prevPrimitive_ + xScaling_ * (fAverage_*xVal + gNext_*xVal + (gPrev_-gNext_)/(eta3_*eta3_) *
                            (1.0/3.0 * eta3_*eta3_*eta3_)) );
                }
            }
            Real fNext() const override { return (fAverage_ + gNext_); }

          private:
            Real xPrev_, xScaling_, gPrev_, gNext_, fAverage_, eta3_, prevPrimitive_;
        };

        class ConvexMonotone4Helper : public SectionHelper {
          public
