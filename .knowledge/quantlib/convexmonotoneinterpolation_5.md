e(x);

                Real xVal = (x-xPrev_)/xScaling_;
                if (x <= x2_) {
                    xVal /= xRatio_;
                    return( prevPrimitive_ + xScaling_*xRatio_*(fAverage_ + A_ + (gPrev_-A_)/(eta4_*eta4_) *
                            (eta4_*eta4_ - eta4_*xVal + 1.0/3.0*xVal*xVal)) * xVal );
                } else if (x <= x3_) {
                    return( prevPrimitive_ + xScaling_*xRatio_*(fAverage_*eta4_ + A_*eta4_ + (gPrev_-A_)/(eta4_*eta4_) *
                            (1.0/3.0*eta4_*eta4_*eta4_)) );
                } else {
                    xVal = 1.0 - (1.0-xVal)/xRatio_;
                    return( prevPrimitive_ + xScaling_*xRatio_*(fAverage_*xVal + A_*xVal + (gPrev_-A_)*(1.0/3.0*eta4_) +
                            (gNext_-A_) / ((1.0-eta4_)*(1.0-eta4_)) *
                            (1.0/3.0*xVal*xVal*xVal - eta4_*xVal*xVal + eta4_*eta4_*xVal - 1.0/3.0*eta4_*eta4_*eta4_)) );
                }
            }

          private:
            bool splitRegion_ = false;
            Real xRatio_, x2_, x3_;
        };

        class ConstantGradHelper : public SectionHelper {
          public:
            ConstantGradHelper(Real fPrev, Real prevPrimitive,
                               Real xPrev, Real xNext, Real fNext)
            : fPrev_(fPrev), prevPrimitive_(prevPrimitive),
            xPrev_(xPrev), fGrad_((fNext-fPrev)/(xNext-xPrev)),fNext_(fNext)
            {}

            Real value(Real x) const override { return (fPrev_ + (x - xPrev_) * fGrad_); }
            Real primitive(Real x) const override {
                return (prevPrimitive_+(x-xPrev_)*(fPrev_+0.5*(x-xPrev_)*fGrad_));
            }
            Real fNext() const override { return fNext_; }

          private:
            Real fPrev_, prevPrimitive_, xPrev_, fGrad_, fNext_;
        };

        class QuadraticHelper : public SectionHelper {
          public:
            QuadraticHelper(Real xPrev, Real xNext,
                               Real fPrev, Real fNext,
                               Real fAverage,
                               Real prevPrimitive)
            : xPrev_(xPrev), xNext_(xNext), fPrev_(fPrev),
              fNext_(fNext), fAverage_(fAverage),
              prevPrimitive_(prevPrimitive) {
                a_ = 3*fPrev_ + 3*fNext_ - 6*fAverage_;
                b_ = -(4*fPrev_ + 2*fNext_ - 6*fAverage_);
                c_ = fPrev_;
                xScaling_ = xNext_-xPrev_;
            }

            Real value(Real x) const override {
                Real xVal = (x-xPrev_)/xScaling_;
                return( a_*xVal*xVal + b_*xVal + c_ );
            }

            Real primitive(Real x) const override {
                Real xVal = (x-xPrev_)/xScaling_;
                return( prevPrimitive_ + xScaling_ * (a_/3*xVal*xVal + b_/2*xVal + c_) * xVal );
            }

            Real fNext() const override { return fNext_; }

          private:
            Real xPrev_, xNext_, fPrev_, fNext_, fAverage_, prevPrimitive_;
            Real xScaling_, a_, b_, c_;
        };

        class QuadraticMinHelper : public SectionHelper {
          public:
            QuadraticMinHelper(
                Real xPrev, Real xNext, Real fPrev, Real fNext, Real fAverage, Real prevPrimitive)
            : x1_(xPrev), x4_(xNext), primitive1_(prevPrimitive), fAverage_(fAverage),
              fPrev_(fPrev), fNext_(fNext) {
                a_ = 3*fPrev_ + 3*fNext_ - 6*fAverage_;
                b_ = -(4*fPrev_ + 2*fNext_ - 6*fAverage_);
                c_ = fPrev_;
                Real d = b_*b_-4*a_*c_;
                xScaling_ = x4_-x1_;
                if (d > 0) {
                    Real aAv = 36;
                    Real bAv = -24*(fPrev_+fNext_);
                    Real cAv = 4*(fPrev_*fPrev_ + fPrev_*fNext_ + fNext_*fNext_);
                    Real dAv = bAv*bAv - 4.0*aAv*cAv;
                    if (dAv >= 0.0) {
                        splitRegion_ = true;
                        Real avRoot = (-bAv - std::sqrt(
