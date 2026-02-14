ber to update the interpolation. If we don't and we are on the last "i", we will still
                        // have the last attempted value in the solver being used in ts_->interpolation_.
                        ts_->interpolation_.update();
                    } else {
                        QL_FAIL(io::ordinal(iteration + 1) << " iteration: failed "
                                "at " << io::ordinal(i) << " alive instrument, "
                                "pillar " << helper->pillarDate() <<
                                ", maturity " << helper->maturityDate() <<
                                ", reference date " << ts_->dates_[0] <<
                                ": " << e.what());
                    }
                }
            }

            if (!loopRequired_)
                 break;

            // exit condition
            Real change = 0;
            if (validData) {
                for (Size i=1; i<=alive_; ++i)
                    change = std::max(change, std::fabs(data[i]-previousData[i]));
                if (change<=accuracy)  // convergence reached
                    break;
            }

            // If we hit the max number of iterations and dontThrow is true, just use what we have
            if (iteration == maxIterations) {
                if (dontThrow_) {
                    break;
                } else {
                    QL_FAIL("convergence not reached after " << iteration <<
                            " iterations; last improvement " << change <<
                            ", required accuracy " << accuracy);
                }
            }

            validData = true;
        }
        validCurve_ = true;
    }

}

#endif
