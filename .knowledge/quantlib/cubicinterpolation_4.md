{
                if (leftType_ == CubicInterpolation::Lagrange
                    || rightType_ == CubicInterpolation::Lagrange) {
                    QL_REQUIRE((xEnd-xBegin) >= 4,
                               "Lagrange boundary condition requires at least "
                               "4 points (" << (xEnd-xBegin) << " are given)");
                }
            }

            void update() override {

                for (Size i=0; i<n_-1; ++i) {
                    dx_[i] = this->xBegin_[i+1] - this->xBegin_[i];
                    S_[i] = (this->yBegin_[i+1] - this->yBegin_[i])/dx_[i];
                }

                // first derivative approximation
                if (da_==CubicInterpolation::Spline) {
                    for (Size i=1; i<n_-1; ++i) {
                        L_.setMidRow(i, dx_[i], 2.0*(dx_[i]+dx_[i-1]), dx_[i-1]);
                        tmp_[i] = 3.0*(dx_[i]*S_[i-1] + dx_[i-1]*S_[i]);
                    }

                    // left boundary condition
                    switch (leftType_) {
                      case CubicInterpolation::NotAKnot:
                        // ignoring end condition value
                        L_.setFirstRow(dx_[1]*(dx_[1]+dx_[0]),
                                      (dx_[0]+dx_[1])*(dx_[0]+dx_[1]));
                        tmp_[0] = S_[0]*dx_[1]*(2.0*dx_[1]+3.0*dx_[0]) +
                                 S_[1]*dx_[0]*dx_[0];
                        break;
                      case CubicInterpolation::FirstDerivative:
                        L_.setFirstRow(1.0, 0.0);
                        tmp_[0] = leftValue_;
                        break;
                      case CubicInterpolation::SecondDerivative:
                        L_.setFirstRow(2.0, 1.0);
                        tmp_[0] = 3.0*S_[0] - leftValue_*dx_[0]/2.0;
                        break;
                      case CubicInterpolation::Periodic:
                        QL_FAIL("this end condition is not implemented yet");
                      case CubicInterpolation::Lagrange:
                        L_.setFirstRow(1.0, 0.0);
                        tmp_[0] = cubicInterpolatingPolynomialDerivative(
                                            this->xBegin_[0],this->xBegin_[1],
                                            this->xBegin_[2],this->xBegin_[3],
                                            this->yBegin_[0],this->yBegin_[1],
                                            this->yBegin_[2],this->yBegin_[3],
                                            this->xBegin_[0]);
                        break;
                      default:
                        QL_FAIL("unknown end condition");
                    }

                    // right boundary condition
                    switch (rightType_) {
                      case CubicInterpolation::NotAKnot:
                        // ignoring end condition value
                        L_.setLastRow(-(dx_[n_-2]+dx_[n_-3])*(dx_[n_-2]+dx_[n_-3]),
                                     -dx_[n_-3]*(dx_[n_-3]+dx_[n_-2]));
                        tmp_[n_-1] = -S_[n_-3]*dx_[n_-2]*dx_[n_-2] -
                                     S_[n_-2]*dx_[n_-3]*(3.0*dx_[n_-2]+2.0*dx_[n_-3]);
                        break;
                      case CubicInterpolation::FirstDerivative:
                        L_.setLastRow(0.0, 1.0);
                        tmp_[n_-1] = rightValue_;
                        break;
                      case CubicInterpolation::SecondDerivative:
                        L_.setLastRow(1.0, 2.0);
                        tmp_[n_-1] = 3.0*S_[n_-2] + rightValue_*dx_[n_-2]/2.0;
                        break;
                      case CubicInterpolation::Periodic:
                        QL_FAIL("this end condition is not implemented yet");
                      case CubicInterpolation::Lagrange:
                        L_.setLastRow(0.0,1.0);
                        tmp_[n_-1] = cubicInterpolatingPolynomialDerivative(

