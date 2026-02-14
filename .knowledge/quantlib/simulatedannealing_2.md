 amotsa(P, -1.0);
                if (ytry_ <= ylo_) {
                    amotsa(P, 2.0);
                } else {
                    if (ytry_ >= ynhi_) {
                        ysave_ = yhi_;
                        amotsa(P, 0.5);
                        if (ytry_ >= ysave_) {
                            for (i_ = 0; i_ < n_ + 1; i_++) {
                                if (i_ != ilo_) {
                                    for (j_ = 0; j_ < n_; j_++) {
                                        sum_[j_] = 0.5 * (vertices_[i_][j_] +
                                                          vertices_[ilo_][j_]);
                                        vertices_[i_][j_] = sum_[j_];
                                    }
                                    values_[i_] = P.value(sum_);
                                }
                            }
                            iteration_ += n_;
                            for (i_ = 0; i_ < n_; i_++)
                                sum_[i_] = 0.0;
                            for (i_ = 0; i_ <= n_; i_++)
                                sum_ += vertices_[i_];
                        }
                    } else {
                        iteration_ += 1;
                    }
                }
            } while (iteration_ <
                     iterationT_ + (scheme_ == ConstantFactor ? m_ : 1));

            switch (scheme_) {
            case ConstantFactor:
                T_ *= (1.0 - epsilon_);
                break;
            case ConstantBudget:
                if (iteration_ <= K_)
                    T_ = T0_ *
                         std::pow(1.0 - (Real)iteration_ / (Real)K_, alpha_);
                else
                    T_ = 0.0;
                break;
            }

        } while (true);
    }
}

#endif
