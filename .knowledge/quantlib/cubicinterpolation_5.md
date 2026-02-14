               this->xBegin_[n_-4],this->xBegin_[n_-3],
                                      this->xBegin_[n_-2],this->xBegin_[n_-1],
                                      this->yBegin_[n_-4],this->yBegin_[n_-3],
                                      this->yBegin_[n_-2],this->yBegin_[n_-1],
                                      this->xBegin_[n_-1]);
                        break;
                      default:
                        QL_FAIL("unknown end condition");
                    }

                    // solve the system
                    L_.solveFor(tmp_, tmp_);
                } else if (da_==CubicInterpolation::SplineOM1) {
                    Matrix T_(n_-2, n_, 0.0);
                    for (Size i=0; i<n_-2; ++i) {
                        T_[i][i]=dx_[i]/6.0;
                        T_[i][i+1]=(dx_[i+1]+dx_[i])/3.0;
                        T_[i][i+2]=dx_[i+1]/6.0;
                    }
                    Matrix S_(n_-2, n_, 0.0);
                    for (Size i=0; i<n_-2; ++i) {
                        S_[i][i]=1.0/dx_[i];
                        S_[i][i+1]=-(1.0/dx_[i+1]+1.0/dx_[i]);
                        S_[i][i+2]=1.0/dx_[i+1];
                    }
                    Matrix Up_(n_, 2, 0.0);
                    Up_[0][0]=1;
                    Up_[n_-1][1]=1;
                    Matrix Us_(n_, n_-2, 0.0);
                    for (Size i=0; i<n_-2; ++i)
                        Us_[i+1][i]=1;
                    Matrix Z_ = Us_*inverse(T_*Us_);
                    Matrix I_(n_, n_, 0.0);
                    for (Size i=0; i<n_; ++i)
                        I_[i][i]=1;
                    Matrix V_ = (I_-Z_*T_)*Up_;
                    Matrix W_ = Z_*S_;
                    Matrix Q_(n_, n_, 0.0);
                    Q_[0][0]=1.0/(n_-1)*dx_[0]*dx_[0]*dx_[0];
                    Q_[0][1]=7.0/8*1.0/(n_-1)*dx_[0]*dx_[0]*dx_[0];
                    for (Size i=1; i<n_-1; ++i) {
                        Q_[i][i-1]=7.0/8*1.0/(n_-1)*dx_[i-1]*dx_[i-1]*dx_[i-1];
                        Q_[i][i]=1.0/(n_-1)*dx_[i]*dx_[i]*dx_[i]+1.0/(n_-1)*dx_[i-1]*dx_[i-1]*dx_[i-1];
                        Q_[i][i+1]=7.0/8*1.0/(n_-1)*dx_[i]*dx_[i]*dx_[i];
                    }
                    Q_[n_-1][n_-2]=7.0/8*1.0/(n_-1)*dx_[n_-2]*dx_[n_-2]*dx_[n_-2];
                    Q_[n_-1][n_-1]=1.0/(n_-1)*dx_[n_-2]*dx_[n_-2]*dx_[n_-2];
                    Matrix J_ = (I_-V_*inverse(transpose(V_)*Q_*V_)*transpose(V_)*Q_)*W_;
                    Array Y_(n_);
                    for (Size i=0; i<n_; ++i)
                        Y_[i]=this->yBegin_[i];
                    Array D_ = J_*Y_;
                    for (Size i=0; i<n_-1; ++i)
                        tmp_[i]=(Y_[i+1]-Y_[i])/dx_[i]-(2.0*D_[i]+D_[i+1])*dx_[i]/6.0;
                    tmp_[n_-1]=tmp_[n_-2]+D_[n_-2]*dx_[n_-2]+(D_[n_-1]-D_[n_-2])*dx_[n_-2]/2.0;

                } else if (da_==CubicInterpolation::SplineOM2) {
                    Matrix T_(n_-2, n_, 0.0);
                    for (Size i=0; i<n_-2; ++i) {
                        T_[i][i]=dx_[i]/6.0;
                        T_[i][i+1]=(dx_[i]+dx_[i+1])/3.0;
                        T_[i][i+2]=dx_[i+1]/6.0;
                    }
                    Matrix S_(n_-2, n_, 0.0);
                    for (Size i=0; i<n_-2; ++i) {
                        S_[i][i]=1.0/dx_[i];
                        S_[i][i+1]=-(1.0/dx_[i+1]+1.0/dx_[i]);
                        S_[i][i+2]=1.0/dx_[i+1];
                    }
                    Matrix Up_(n_, 2, 0.0);
                    Up_[0][0]=1;
                    Up_[n_-1][1]=1;
                    Matrix Us_(n_, n_-2, 0.0);
                    for (Size i=0; i<n_-2; ++i)
                        Us_[i+1][i]=1;
                    Matrix Z_ = Us_*inverse(T_*Us_);
                    Matrix I_(n_, n_, 0.0);
                    for (Size i=0; i<n_; ++i)
                        I_[i][i]=1;
                    Matrix V_ = (I_-Z_*T_)*Up_;
                    Matrix W_ = Z_*S_;
                    M
