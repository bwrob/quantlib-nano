  xMax_ = enforceBounds_(root_+step);
                fxMax_ = f(xMax_);
            }

            evaluationNumber_ = 2;
            while (evaluationNumber_ <= maxEvaluations_) {
                if (fxMin_*fxMax_ <= 0.0) {
                    if (close(fxMin_, 0.0))
                        return xMin_;
                    if (close(fxMax_, 0.0))
                        return xMax_;
                    root_ = (xMax_+xMin_)/2.0;
                    return this->impl().solveImpl(f, accuracy);
                }
                if (std::fabs(fxMin_) < std::fabs(fxMax_)) {
                    xMin_ = enforceBounds_(xMin_+growthFactor*(xMin_ - xMax_));
                    fxMin_= f(xMin_);
                } else if (std::fabs(fxMin_) > std::fabs(fxMax_)) {
                    xMax_ = enforceBounds_(xMax_+growthFactor*(xMax_ - xMin_));
                    fxMax_= f(xMax_);
                } else if (flipflop == -1) {
                    xMin_ = enforceBounds_(xMin_+growthFactor*(xMin_ - xMax_));
                    fxMin_= f(xMin_);
                    evaluationNumber_++;
                    flipflop = 1;
                } else if (flipflop == 1) {
                    xMax_ = enforceBounds_(xMax_+growthFactor*(xMax_ - xMin_));
                    fxMax_= f(xMax_);
                    flipflop = -1;
                }
                evaluationNumber_++;
            }

            QL_FAIL("unable to bracket root in " << maxEvaluations_
                    << " function evaluations (last bracket attempt: "
                    << "f[" << xMin_ << "," << xMax_ << "] "
                    << "-> [" << fxMin_ << "," << fxMax_ << "])");
        }
        /*! This method returns the zero of the function \f$ f \f$,
            determined with the given accuracy \f$ \epsilon \f$;
            depending on the particular solver, this might mean that
            the returned \f$ x \f$ is such that \f$ |f(x)| < \epsilon
            \f$, or that \f$ |x-\xi| < \epsilon \f$ where \f$ \xi \f$
            is the real zero.

            An initial guess must be supplied, as well as two values
            \f$ x_\mathrm{min} \f$ and \f$ x_\mathrm{max} \f$ which
            must bracket the zero (i.e., either \f$ f(x_\mathrm{min})
            \leq 0 \leq f(x_\mathrm{max}) \f$, or \f$
            f(x_\mathrm{max}) \leq 0 \leq f(x_\mathrm{min}) \f$ must
            be true).
        */
        template <class F>
        Real solve(const F& f,
                   Real accuracy,
                   Real guess,
                   Real xMin,
                   Real xMax) const {

            QL_REQUIRE(accuracy>0.0,
                       "accuracy (" << accuracy << ") must be positive");
            // check whether we really want to use epsilon
            accuracy = std::max(accuracy, QL_EPSILON);

            xMin_ = xMin;
            xMax_ = xMax;

            QL_REQUIRE(xMin_ < xMax_,
                       "invalid range: xMin_ (" << xMin_
                       << ") >= xMax_ (" << xMax_ << ")");
            QL_REQUIRE(!lowerBoundEnforced_ || xMin_ >= lowerBound_,
                       "xMin_ (" << xMin_
                       << ") < enforced low bound (" << lowerBound_ << ")");
            QL_REQUIRE(!upperBoundEnforced_ || xMax_ <= upperBound_,
                       "xMax_ (" << xMax_
                       << ") > enforced hi bound (" << upperBound_ << ")");

            fxMin_ = f(xMin_);
            if (close(fxMin_, 0.0))
                return xMin_;

            fxMax_ = f(xMax_);
            if (close(fxMax_, 0.0))
                return xMax_;

            evaluationNumber_ = 2;

            QL_REQUIRE(fxMin_*fxMax_ < 0.0,
                       "root not bracketed: f["
                       << xMin_ << "," << xMax_ << "] -> ["
                       << std::scientific
                       << fxMin_ << "," << fxMax_ << "]");

            QL_REQUIRE(guess > xMin_,
                       "guess (" << guess << ") < xMin_ (" << xMin_ << ")