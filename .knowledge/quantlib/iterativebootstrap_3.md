 = minValues[i];
                Real& max = maxValues[i];

                // bracket root and calculate guess
                if (min == Null<Real>()) {
                    // First attempt; we take min and max either from
                    // explicit constructor parameter or from traits
                    min = (minValue_ != Null<Real>() ? minValue_ :
                           Traits::minValueAfter(i, ts_, validData, firstAliveHelper_));
                    max = (maxValue_ != Null<Real>() ? maxValue_ :
                           Traits::maxValueAfter(i, ts_, validData, firstAliveHelper_));
                } else {
                    // Extending a previous attempt.  A negative min
                    // is enlarged; a positive one is shrunk towards 0.
                    min = (min < 0.0 ? Real(min * minFactor_) : Real(min / minFactor_));
                    // The opposite holds for the max.
                    max = (max > 0.0 ? Real(max * maxFactor_) : Real(max / maxFactor_));
                }
                Real guess = Traits::guess(i, ts_, validData, firstAliveHelper_);

                // adjust guess if needed
                if (guess >= max)
                    guess = max - (max - min) / 5.0;
                else if (guess <= min)
                    guess = min + (max - min) / 5.0;

                // extend interpolation if needed
                if (!validData) {
                    try { // extend interpolation a point at a time
                          // including the pillar to be boostrapped
                        ts_->interpolation_ = ts_->interpolator_.interpolate(
                            times.begin(), times.begin()+i+1, data.begin());
                    } catch (...) {
                        if (!Interpolator::global)
                            throw; // no chance to fix it in a later iteration

                        // otherwise use Linear while the target
                        // interpolation is not usable yet
                        ts_->interpolation_ = Linear().interpolate(
                            times.begin(), times.begin()+i+1, data.begin());
                    }
                    ts_->interpolation_.update();
                }

                const auto& helper = ts_->instruments_[j];
                auto error = [&](Rate guess) {
                    Traits::updateGuess(ts_->data_, guess, i);
                    ts_->interpolation_.update();
                    return helper->quoteError();
                };
                try {
                    if (validData)
                        solver_.solve(error, accuracy, guess, min, max);
                    else
                        firstSolver_.solve(error, accuracy, guess, min, max);
                } catch (std::exception &e) {
                    if (validCurve_) {
                        // the previous curve state might have been a
                        // bad guess, so we retry without using it.
                        // This would be tricky to do here (we're
                        // inside multiple nested for loops, we need
                        // to re-initialize...), so we invalidate the
                        // curve, make a recursive call and then exit.
                        validCurve_ = initialized_ = false;
                        calculate();
                        return;
                    }

                    // If we have more attempts left on this iteration, try again. Note that the max and min
                    // bounds will be widened on the retry.
                    if (attempts[i] < maxAttempts_) {
                        attempts[i]++;
                        i--;
                        j--;
                        continue;
                    }

                    if (dontThrow_) {
                        // Use the fallback value
                        ts_->data_[i] = detail::dontThrowFallback(error, min, max, dontThrowSteps_);

                        // Remem
