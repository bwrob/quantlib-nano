-1] = 3*S_[n_-2];
                                    }
                                }
                                break;
                            default:
                                QL_FAIL("unknown scheme");
                        }
                    }
                }

                std::fill(monotonicityAdjustments_.begin(),
                          monotonicityAdjustments_.end(), false);
                // Hyman monotonicity constrained filter
                if (monotonic_) {
                    Real correction;
                    Real pm, pu, pd, M;
                    for (Size i=0; i<n_; ++i) {
                        if (i==0) {
                            if (tmp_[i]*S_[0]>0.0) {
                                correction = tmp_[i]/std::fabs(tmp_[i]) *
                                    std::min<Real>(std::fabs(tmp_[i]),
                                                   std::fabs(3.0*S_[0]));
                            } else {
                                correction = 0.0;
                            }
                            if (correction!=tmp_[i]) {
                                tmp_[i] = correction;
                                monotonicityAdjustments_[i] = true;
                            }
                        } else if (i==n_-1) {
                            if (tmp_[i]*S_[n_-2]>0.0) {
                                correction = tmp_[i]/std::fabs(tmp_[i]) *
                                    std::min<Real>(std::fabs(tmp_[i]),
                                                   std::fabs(3.0*S_[n_-2]));
                            } else {
                                correction = 0.0;
                            }
                            if (correction!=tmp_[i]) {
                                tmp_[i] = correction;
                                monotonicityAdjustments_[i] = true;
                            }
                        } else {
                            pm=(S_[i-1]*dx_[i]+S_[i]*dx_[i-1])/
                                (dx_[i-1]+dx_[i]);
                            M = 3.0 * std::min({
                                    std::fabs(S_[i-1]),
                                    std::fabs(S_[i]),
                                    std::fabs(pm)
                                });
                            if (i>1) {
                                if ((S_[i-1]-S_[i-2])*(S_[i]-S_[i-1])>0.0) {
                                    pd=(S_[i-1]*(2.0*dx_[i-1]+dx_[i-2])
                                        -S_[i-2]*dx_[i-1])/
                                        (dx_[i-2]+dx_[i-1]);
                                    if (pm*pd>0.0 && pm*(S_[i-1]-S_[i-2])>0.0) {
                                        M = std::max<Real>(M, 1.5*std::min(
                                                std::fabs(pm),std::fabs(pd)));
                                    }
                                }
                            }
                            if (i<n_-2) {
                                if ((S_[i]-S_[i-1])*(S_[i+1]-S_[i])>0.0) {
                                    pu=(S_[i]*(2.0*dx_[i]+dx_[i+1])-S_[i+1]*dx_[i])/
                                        (dx_[i]+dx_[i+1]);
                                    if (pm*pu>0.0 && -pm*(S_[i]-S_[i-1])>0.0) {
                                        M = std::max<Real>(M, 1.5*std::min(
                                                std::fabs(pm),std::fabs(pu)));
                                    }
                                }
                            }
                            if (tmp_[i]*pm>0.0) {
                                correction = tmp_[i]/std::fabs(tmp_[i]) *
                                    std::min(std::fabs(tmp_[i]), M);
                            } else {
                                correction = 0.0;
                            }
                            if (correction!=tmp_[i]) {
                                tmp_[i] = correction;
                             