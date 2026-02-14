:
            ConvexMonotone4Helper(Real xPrev,  Real xNext,
                                  Real gPrev, Real gNext,
                                  Real fAverage, Real eta4,
                                  Real prevPrimitive)
            : xPrev_(xPrev), xScaling_(xNext-xPrev), gPrev_(gPrev),
              gNext_(gNext), fAverage_(fAverage), eta4_(eta4), prevPrimitive_(prevPrimitive) {
                A_ = -0.5*(eta4_*gPrev_ + (1-eta4_)*gNext_);
            }

            Real value(Real x) const override {
                Real xVal = (x-xPrev_)/xScaling_;
                if (xVal <= eta4_) {
                    return(fAverage_ + A_ + (gPrev_-A_)*(eta4_-xVal)*(eta4_-xVal)/(eta4_*eta4_) );
                } else {
                    return(fAverage_ + A_ + (gNext_-A_)*(xVal-eta4_)*(xVal-eta4_)/((1-eta4_)*(1-eta4_)) );
                }
            }

            Real primitive(Real x) const override {
                Real xVal = (x-xPrev_)/xScaling_;
                Real retVal;
                if (xVal <= eta4_) {
                    retVal = prevPrimitive_ + xScaling_ * (fAverage_ + A_ + (gPrev_-A_)/(eta4_*eta4_) *
                            (eta4_*eta4_ - eta4_*xVal + 1.0/3.0*xVal*xVal)) * xVal;
                } else {
                    retVal = prevPrimitive_ + xScaling_ *(fAverage_*xVal + A_*xVal + (gPrev_-A_)*(1.0/3.0*eta4_) +
                             (gNext_-A_)/((1-eta4_)*(1-eta4_)) *
                             (1.0/3.0*xVal*xVal*xVal - eta4_*xVal*xVal + eta4_*eta4_*xVal - 1.0/3.0*eta4_*eta4_*eta4_));
                }
                return retVal;
            }
            Real fNext() const override { return (fAverage_ + gNext_); }

          protected:
            Real xPrev_, xScaling_, gPrev_, gNext_, fAverage_, eta4_, prevPrimitive_;
            Real A_;
        };

        class ConvexMonotone4MinHelper : public ConvexMonotone4Helper {
          public:
            ConvexMonotone4MinHelper(Real xPrev,
                                     Real xNext,
                                     Real gPrev,
                                     Real gNext,
                                     Real fAverage,
                                     Real eta4,
                                     Real prevPrimitive)
            : ConvexMonotone4Helper(xPrev, xNext, gPrev, gNext, fAverage, eta4, prevPrimitive) {
                if ( A_+ fAverage_ <= 0.0 ) {
                    splitRegion_ = true;
                    Real fPrev = gPrev_+fAverage_;
                    Real fNext = gNext_+fAverage_;
                    Real reqdShift = (eta4_*fPrev + (1-eta4_)*fNext)/3.0 - fAverage_;
                    Real reqdPeriod = reqdShift * xScaling_ / (fAverage_+reqdShift);
                    Real xAdjust = xScaling_ - reqdPeriod;
                    xRatio_ =  xAdjust/xScaling_;

                    fAverage_ += reqdShift;
                    gNext_ = fNext - fAverage_;
                    gPrev_ = fPrev - fAverage_;
                    A_ = -(eta4_ * gPrev_ + (1.0-eta4)*gNext_)/2.0;
                    x2_ = xPrev_ + xAdjust  * eta4_;
                    x3_ = xPrev_ + xScaling_ - xAdjust*(1.0-eta4_);
                }
            }

            Real value(Real x) const override {
                if (!splitRegion_)
                    return ConvexMonotone4Helper::value(x);

                Real xVal = (x-xPrev_)/xScaling_;
                if (x <= x2_) {
                    xVal /= xRatio_;
                    return(fAverage_ + A_ + (gPrev_-A_)*(eta4_-xVal)*(eta4_-xVal)/(eta4_*eta4_));
                } else if (x < x3_) {
                    return 0.0;
                } else {
                    xVal = 1.0 - (1.0 - xVal) / xRatio_;
                    return(fAverage_ + A_ + (gNext_-A_)*(xVal-eta4_)*(xVal-eta4_)/((1-eta4_)*(1-eta4_)) );
                }
            }

            Real primitive(Real x) const override {
                if (!splitRegion_)
                    return ConvexMonotone4Helper::primitiv
