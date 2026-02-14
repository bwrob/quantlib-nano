atrix Q_(n_, n_, 0.0);
                    Q_[0][0]=1.0/(n_-1)*dx_[0];
                    Q_[0][1]=1.0/2*1.0/(n_-1)*dx_[0];
                    for (Size i=1; i<n_-1; ++i) {
                        Q_[i][i-1]=1.0/2*1.0/(n_-1)*dx_[i-1];
                        Q_[i][i]=1.0/(n_-1)*dx_[i]+1.0/(n_-1)*dx_[i-1];
                        Q_[i][i+1]=1.0/2*1.0/(n_-1)*dx_[i];
                    }
                    Q_[n_-1][n_-2]=1.0/2*1.0/(n_-1)*dx_[n_-2];
                    Q_[n_-1][n_-1]=1.0/(n_-1)*dx_[n_-2];
                    Matrix J_ = (I_-V_*inverse(transpose(V_)*Q_*V_)*transpose(V_)*Q_)*W_;
                    Array Y_(n_);
                    for (Size i=0; i<n_; ++i)
                        Y_[i]=this->yBegin_[i];
                    Array D_ = J_*Y_;
                    for (Size i=0; i<n_-1; ++i)
                        tmp_[i]=(Y_[i+1]-Y_[i])/dx_[i]-(2.0*D_[i]+D_[i+1])*dx_[i]/6.0;
                    tmp_[n_-1]=tmp_[n_-2]+D_[n_-2]*dx_[n_-2]+(D_[n_-1]-D_[n_-2])*dx_[n_-2]/2.0;
                } else { // local schemes
                    if (n_==2)
                        tmp_[0] = tmp_[1] = S_[0];
                    else {
                        switch (da_) {
                            case CubicInterpolation::FourthOrder:
                                QL_FAIL("FourthOrder not implemented yet");
                                break;
                            case CubicInterpolation::Parabolic:
                                // intermediate points
                                for (Size i=1; i<n_-1; ++i)
                                    tmp_[i] = (dx_[i-1]*S_[i]+dx_[i]*S_[i-1])/(dx_[i]+dx_[i-1]);
                                // end points
                                tmp_[0]    = ((2.0*dx_[   0]+dx_[   1])*S_[   0] - dx_[   0]*S_[   1]) / (dx_[   0]+dx_[   1]);
                                tmp_[n_-1] = ((2.0*dx_[n_-2]+dx_[n_-3])*S_[n_-2] - dx_[n_-2]*S_[n_-3]) / (dx_[n_-2]+dx_[n_-3]);
                                break;
                            case CubicInterpolation::FritschButland:
                                // intermediate points
                                for (Size i=1; i<n_-1; ++i) {
                                    Real Smin = std::min(S_[i-1], S_[i]);
                                    Real Smax = std::max(S_[i-1], S_[i]);
                                    if(Smax+2.0*Smin == 0){
                                        if (Smin*Smax < 0)
                                            tmp_[i] = QL_MIN_REAL;
                                        else if (Smin*Smax == 0)
                                            tmp_[i] = 0;
                                        else
                                            tmp_[i] = QL_MAX_REAL;
                                    }
                                    else
                                        tmp_[i] = 3.0*Smin*Smax/(Smax+2.0*Smin);
                                }
                                // end points
                                tmp_[0]    = ((2.0*dx_[   0]+dx_[   1])*S_[   0] - dx_[   0]*S_[   1]) / (dx_[   0]+dx_[   1]);
                                tmp_[n_-1] = ((2.0*dx_[n_-2]+dx_[n_-3])*S_[n_-2] - dx_[n_-2]*S_[n_-3]) / (dx_[n_-2]+dx_[n_-3]);
                                break;
                            case CubicInterpolation::Akima:
                                tmp_[0] = (std::abs(S_[1]-S_[0])*2*S_[0]*S_[1]+std::abs(2*S_[0]*S_[1]-4*S_[0]*S_[0]*S_[1])*S_[0])/(std::abs(S_[1]-S_[0])+std::abs(2*S_[0]*S_[1]-4*S_[0]*S_[0]*S_[1]));
                                tmp_[1] = (std::abs(S_[2]-S_[1])*S_[0]+std::abs(S_[0]-2*S_[0]*S_[1])*S_[1])/(std::abs(S_[2]-S_[1])+std::abs(S_[0]-2*S_[0]*S_[1]));
                                for (Size i=2; i<n_-2; ++i) {
                                    if ((S_[i-2]==S_[i-1]) && (S_[i]!=S_[i+1]))
                                        tmp_[i] = S_[i-1];
                                    else if ((S_[i-2]!=S_[i-1]) && (S_[i]==S_[i+1]))

