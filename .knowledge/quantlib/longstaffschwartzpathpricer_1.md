se_) {
            // store paths for the calibration
            paths_.push_back(path);
            // result doesn't matter
            return 0.0;
        }

        Real price = (*pathPricer_)(path, len_-1);

        // Initialize with exercise on last date
        bool exercised = (price > 0.0);

        for (Size i=len_-2; i>0; --i) {
            price*=dF_[i];

            const Real exercise = (*pathPricer_)(path, i);
            if (exercise > 0.0) {
                const StateType regValue = pathPricer_->state(path, i);

                Real continuationValue = 0.0;
                for (Size l=0; l<v_.size(); ++l) {
                    continuationValue += coeff_[i-1][l] * v_[l](regValue);
                }

                if (continuationValue < exercise) {
                    price = exercise;

                    // Exercised
                    exercised = true;
                }
            }
        }

        exerciseProbability_.add(exercised ? 1.0 : 0.0);

        return price*dF_[0];
    }

    template <class PathType> inline
    void LongstaffSchwartzPathPricer<PathType>::calibrate() {
        const Size n = paths_.size();
        Array prices(n), exercise(n);
        std::vector<StateType> p_state(n);
        std::vector<Real> p_price(n), p_exercise(n);

        for (Size i=0; i<n; ++i) {
            p_state[i] = pathPricer_->state(paths_[i],len_-1);
            prices[i] = p_price[i] = (*pathPricer_)(paths_[i], len_-1);
            p_exercise[i] = prices[i];
        }

        post_processing(len_ - 1, p_state, p_price, p_exercise);

        std::vector<Real>      y;
        std::vector<StateType> x;
        for (Size i=len_-2; i>0; --i) {
            y.clear();
            x.clear();

            //roll back step
            for (Size j=0; j<n; ++j) {
                exercise[j]=(*pathPricer_)(paths_[j], i);
                if (exercise[j]>0.0) {
                    x.push_back(pathPricer_->state(paths_[j], i));
                    y.push_back(dF_[i]*prices[j]);
                }
            }

            if (v_.size() <=  x.size()) {
                coeff_[i-1] = GeneralLinearLeastSquares(x, y, v_).coefficients();
            }
            else {
            // if number of itm paths is smaller then the number of
            // calibration functions then early exercise if exerciseValue > 0
                coeff_[i-1] = Array(v_.size(), 0.0);
            }

            for (Size j=0, k=0; j<n; ++j) {
                prices[j]*=dF_[i];
                if (exercise[j]>0.0) {
                    Real continuationValue = 0.0;
                    for (Size l=0; l<v_.size(); ++l) {
                        continuationValue += coeff_[i-1][l] * v_[l](x[k]);
                    }
                    if (continuationValue < exercise[j]) {
                        prices[j] = exercise[j];
                    }
                    ++k;
                }
                p_state[j] = pathPricer_->state(paths_[j],i);
                p_price[j] = prices[j];
                p_exercise[j] = exercise[j];
            }

            post_processing(i, p_state, p_price, p_exercise);
        }

        // remove calibration paths and release memory
        std::vector<PathType> empty;
        paths_.swap(empty);
        // entering the calculation phase
        calibrationPhase_ = false;
    }

    template <class PathType> inline
    Real LongstaffSchwartzPathPricer<PathType>::exerciseProbability() const {
        return exerciseProbability_.mean();
    }


}


#endif