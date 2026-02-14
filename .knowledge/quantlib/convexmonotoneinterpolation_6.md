dAv))/(2*aAv);

                        xRatio_ = fAverage_ / avRoot;
                        xScaling_ *= xRatio_;

                        a_ = 3*fPrev_ + 3*fNext_ - 6*avRoot;
                        b_ = -(4*fPrev_ + 2*fNext_ - 6*avRoot);
                        c_ = fPrev_;
                        Real xRoot = -b_/(2*a_);
                        x2_ = x1_ + xRatio_ * (x4_-x1_) * xRoot;
                        x3_ = x4_ - xRatio_ * (x4_-x1_) * (1-xRoot);
                        primitive2_ =
                            primitive1_ + xScaling_*(a_/3*xRoot*xRoot + b_/2*xRoot + c_)*xRoot;
                    }
                }
            }

            Real value(Real x) const override {
                Real xVal = (x - x1_) / (x4_-x1_);
                if (splitRegion_) {
                    if (x <= x2_) {
                        xVal /= xRatio_;
                    } else if (x < x3_) {
                        return 0.0;
                    } else {
                        xVal = 1.0 - (1.0 - xVal) / xRatio_;
                    }
                }

                return c_ + b_*xVal + a_*xVal*xVal;
            }

            Real primitive(Real x) const override {
                Real xVal = (x - x1_) / (x4_-x1_);
                if (splitRegion_) {
                    if (x < x2_) {
                        xVal /= xRatio_;
                    } else if (x < x3_) {
                        return primitive2_;
                    } else {
                        xVal = 1.0 - (1.0 - xVal) / xRatio_;
                    }
                }
                return primitive1_ + xScaling_ * (a_/3*xVal*xVal+ b_/2*xVal+c_)*xVal;
            }

            Real fNext() const override { return fNext_; }

          private:
            bool splitRegion_ = false;
            Real x1_, x2_, x3_, x4_;
            Real a_, b_, c_;
            Real primitive1_, primitive2_;
            Real fAverage_, fPrev_, fNext_, xScaling_, xRatio_ = 1.0;
        };

        template <class I1, class I2>
        void ConvexMonotoneImpl<I1,I2>::update() {
            sectionHelpers_.clear();
            if (length_ == 2) { //single period
                ext::shared_ptr<SectionHelper> singleHelper(
                              new EverywhereConstantHelper(this->yBegin_[1],
                                                           0.0,
                                                           this->xBegin_[0]));
                sectionHelpers_[this->xBegin_[1]] = singleHelper;
                extrapolationHelper_ = singleHelper;
                return;
            }

            std::vector<Real> f(length_);
            sectionHelpers_ = preSectionHelpers_;
            Size startPoint = sectionHelpers_.size()+1;

            //first derive the boundary forwards.
            for (Size i=startPoint; i<length_-1; ++i) {
                Real dxPrev = this->xBegin_[i] - this->xBegin_[i-1];
                Real dx = this->xBegin_[i+1] - this->xBegin_[i];
                f[i] = dx/(dx+dxPrev) * this->yBegin_[i]
                     + dxPrev/(dx+dxPrev) * this->yBegin_[i+1];
            }

            if (startPoint > 1)
                f[startPoint-1] = preSectionHelpers_.rbegin()->second->fNext();
            if (startPoint == 1)
                f[0] = 1.5 * this->yBegin_[1] - 0.5 * f[1];

            f[length_-1] = 1.5 * this->yBegin_[length_-1] - 0.5 * f[length_-2];

            if (forcePositive_) {
                if (f[0] < 0)
                    f[0] = 0.0;
                if (f[length_-1] < 0.0)
                    f[length_-1] = 0.0;
            }

            Real primitive = 0.0;
            for (Size i = 0; i < startPoint-1; ++i)
                primitive +=
                    this->yBegin_[i+1] * (this->xBegin_[i+1]-this->xBegin_[i]);

            Size endPoint = length_;
            //constantLastPeriod_ = false;
            if (constantLastPeriod_)
                endPoint = endPoint-1;

            for (Size i=startPoint; i< endPoint; ++