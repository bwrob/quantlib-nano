eps, t = from;
            evolver_.setStep(dt);

            if(!stoppingTimes_.empty() && stoppingTimes_.back() == from) {
                if (condition)
                    condition->applyTo(a,from);
            }
            for (Size i=0; i<steps; ++i, t -= dt) {
                Time now = t;
                // make sure last step ends exactly on "to" in order to not
                // miss a stopping time at "to" due to numerical issues
                Time next = (i < steps -1)? t-dt : to;

                if (std::fabs(to-next) < std::sqrt(QL_EPSILON)) next = to;
                bool hit = false;
                for (Integer j = static_cast<Integer>(stoppingTimes_.size())-1; j >= 0 ; --j) {
                    if (next <= stoppingTimes_[j] && stoppingTimes_[j] < now) {
                        // a stopping time was hit
                        hit = true;

                        // perform a small step to stoppingTimes_[j]...
                        evolver_.setStep(now-stoppingTimes_[j]);
                        evolver_.step(a,now);
                        if (condition)
                            condition->applyTo(a,stoppingTimes_[j]);
                        // ...and continue the cycle
                        now = stoppingTimes_[j];
                    }
                }
                // if we did hit...
                if (hit) {
                    // ...we might have to make a small step to
                    // complete the big one...
                    if (now > next) {
                        evolver_.setStep(now - next);
                        evolver_.step(a,now);
                        if (condition)
                            condition->applyTo(a,next);
                    }
                    // ...and in any case, we have to reset the
                    // evolver to the default step.
                    evolver_.setStep(dt);
                } else {
                    // if we didn't, the evolver is already set to the
                    // default step, which is ok for us.
                    evolver_.step(a,now);
                    if (condition)
                        condition->applyTo(a, next);
                }
            }
        }
        Evolver evolver_;
        std::vector<Time> stoppingTimes_;
    };

}


#endif
