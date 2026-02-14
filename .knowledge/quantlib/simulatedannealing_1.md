al fac) {
        fac1_ = (1.0 - fac) / ((Real)n_);
        fac2_ = fac1_ - fac;
        for (j_ = 0; j_ < n_; j_++) {
            ptry_[j_] = sum_[j_] * fac1_ - vertices_[ihi_][j_] * fac2_;
        }
        if (!P.constraint().test(ptry_))
            ytry_ = QL_MAX_REAL;
        else
            ytry_ = P.value(ptry_);
        if (std::isnan(ytry_)) {
            ytry_ = QL_MAX_REAL;
        }
        if (ytry_ <= yb_) {
            yb_ = ytry_;
            pb_ = ptry_;
        }
        yflu_ = ytry_ - tt_ * std::log(rng_.next().value);
        if (yflu_ < yhi_) {
            values_[ihi_] = ytry_;
            yhi_ = yflu_;
            for (j_ = 0; j_ < n_; j_++) {
                sum_[j_] += ptry_[j_] - vertices_[ihi_][j_];
                vertices_[ihi_][j_] = ptry_[j_];
            }
        }
        ytry_ = yflu_;
    }

    template <class RNG>
    EndCriteria::Type SimulatedAnnealing<RNG>::minimize(Problem &P,
                                                        const EndCriteria &ec) {

        Size stationaryStateIterations_ = 0;
        EndCriteria::Type ecType = EndCriteria::None;
        P.reset();
        Array x = P.currentValue();
        iteration_ = 0;
        n_ = x.size();
        ptry_ = Array(n_, 0.0);

        // build vertices

        vertices_ = std::vector<Array>(n_ + 1, x);
        for (i_ = 0; i_ < n_; i_++) {
            Array direction(n_, 0.0);
            direction[i_] = 1.0;
            P.constraint().update(vertices_[i_ + 1], direction, lambda_);
        }
        values_ = Array(n_ + 1, 0.0);
        for (i_ = 0; i_ <= n_; i_++) {
            if (!P.constraint().test(vertices_[i_]))
                values_[i_] = QL_MAX_REAL;
            else
                values_[i_] = P.value(vertices_[i_]);
            if (std::isnan(ytry_)) { // handle NAN
                values_[i_] = QL_MAX_REAL;
            }
        }

        // minimize

        T_ = T0_;
        yb_ = QL_MAX_REAL;
        pb_ = Array(n_, 0.0);
        do {
            iterationT_ = iteration_;
            do {
                sum_ = Array(n_, 0.0);
                for (i_ = 0; i_ <= n_; i_++)
                    sum_ += vertices_[i_];
                tt_ = -T_;
                ilo_ = 0;
                ihi_ = 1;
                ynhi_ = values_[0] + tt_ * std::log(rng_.next().value);
                ylo_ = ynhi_;
                yhi_ = values_[1] + tt_ * std::log(rng_.next().value);
                if (ylo_ > yhi_) {
                    ihi_ = 0;
                    ilo_ = 1;
                    ynhi_ = yhi_;
                    yhi_ = ylo_;
                    ylo_ = ynhi_;
                }
                for (i_ = 2; i_ < n_ + 1; i_++) {
                    yt_ = values_[i_] + tt_ * std::log(rng_.next().value);
                    if (yt_ <= ylo_) {
                        ilo_ = i_;
                        ylo_ = yt_;
                    }
                    if (yt_ > yhi_) {
                        ynhi_ = yhi_;
                        ihi_ = i_;
                        yhi_ = yt_;
                    } else {
                        if (yt_ > ynhi_) {
                            ynhi_ = yt_;
                        }
                    }
                }

                // rtol_ = 2.0 * std::fabs(yhi_ - ylo_) /
                //         (std::fabs(yhi_) + std::fabs(ylo_));
                // check rtol against some ftol... // NR end criterion in f(x)

                // GSL end criterion in x (cf. above)
                if (ec.checkStationaryPoint(simplexSize(), 0.0,
                                            stationaryStateIterations_,
                                            ecType) ||
                    ec.checkMaxIterations(iteration_, ecType)) {
                    // no matter what, we return the best ever point !
                    P.setCurrentValue(pb_);
                    P.setFunctionValue(yb_);
                    return ecType;
                }

                iteration_ += 2;

