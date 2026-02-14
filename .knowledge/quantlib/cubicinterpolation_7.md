                       tmp_[i] = S_[i];
                                    else if (S_[i]==S_[i-1])
                                        tmp_[i] = S_[i];
                                    else if ((S_[i-2]==S_[i-1]) && (S_[i-1]!=S_[i]) && (S_[i]==S_[i+1]))
                                        tmp_[i] = (S_[i-1]+S_[i])/2.0;
                                    else
                                        tmp_[i] = (std::abs(S_[i+1]-S_[i])*S_[i-1]+std::abs(S_[i-1]-S_[i-2])*S_[i])/(std::abs(S_[i+1]-S_[i])+std::abs(S_[i-1]-S_[i-2]));
                                 }
                                 tmp_[n_-2] = (std::abs(2*S_[n_-2]*S_[n_-3]-S_[n_-2])*S_[n_-3]+std::abs(S_[n_-3]-S_[n_-4])*S_[n_-2])/(std::abs(2*S_[n_-2]*S_[n_-3]-S_[n_-2])+std::abs(S_[n_-3]-S_[n_-4]));
                                 tmp_[n_-1] = (std::abs(4*S_[n_-2]*S_[n_-2]*S_[n_-3]-2*S_[n_-2]*S_[n_-3])*S_[n_-2]+std::abs(S_[n_-2]-S_[n_-3])*2*S_[n_-2]*S_[n_-3])/(std::abs(4*S_[n_-2]*S_[n_-2]*S_[n_-3]-2*S_[n_-2]*S_[n_-3])+std::abs(S_[n_-2]-S_[n_-3]));
                                 break;
                            case CubicInterpolation::Kruger:
                                // intermediate points
                                for (Size i=1; i<n_-1; ++i) {
                                    if (S_[i-1]*S_[i]<0.0)
                                        // slope changes sign at point
                                        tmp_[i] = 0.0;
                                    else
                                        // slope will be between the slopes of the adjacent
                                        // straight lines and should approach zero if the
                                        // slope of either line approaches zero
                                        tmp_[i] = 2.0/(1.0/S_[i-1]+1.0/S_[i]);
                                }
                                // end points
                                tmp_[0] = (3.0*S_[0]-tmp_[1])/2.0;
                                tmp_[n_-1] = (3.0*S_[n_-2]-tmp_[n_-2])/2.0;
                                break;
                            case CubicInterpolation::Harmonic:
                                // intermediate points
                                for (Size i=1; i<n_-1; ++i) {
                                    Real w1 = 2*dx_[i]+dx_[i-1];
                                    Real w2 = dx_[i]+2*dx_[i-1];
                                    if (S_[i-1]*S_[i]<=0.0)
                                        // slope changes sign at point
                                        tmp_[i] = 0.0;
                                    else
                                        // weighted harmonic mean of S_[i] and S_[i-1] if they
                                        // have the same sign; otherwise 0
                                        tmp_[i] = (w1+w2)/(w1/S_[i-1]+w2/S_[i]);
                                }
                                // end points [0]
                                tmp_[0] = ((2 * dx_[0] + dx_[1])*S_[0] - dx_[0] * S_[1]) / (dx_[1] + dx_[0]);
                                if (tmp_[0]*S_[0]<0.0) {
                                    tmp_[0] = 0;
                                }
                                else if (S_[0]*S_[1]<0) {
                                    if (std::fabs(tmp_[0])>std::fabs(3*S_[0])) {
                                            tmp_[0] = 3*S_[0];
                                    }
                                }
                                // end points [n-1]
                                tmp_[n_-1] = ((2*dx_[n_-2]+dx_[n_-3])*S_[n_-2]-dx_[n_-2]*S_[n_-3])/(dx_[n_-3]+dx_[n_-2]);
                                if (tmp_[n_-1]*S_[n_-2]<0.0) {
                                    tmp_[n_-1] = 0;
                                }
                                else if (S_[n_-2]*S_[n_-3]<0) {
                                    if (std::fabs(tmp_[n_-1])>std::fabs(3*S_[n_-2])) {
                                        tmp_[n_
