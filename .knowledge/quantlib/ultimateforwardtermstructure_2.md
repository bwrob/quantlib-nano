cutOffTime;
        /* If time to maturity (T) exceeds the cut-off point (T_c),
           i.e. the first smoothing point, the forward rate f is
           extrapolated as follows:

           f(t,T_c,T) = UFR(t) + (LLFR(t) - UFR(t)) * B(T-T_c),

           where:
           UFR(t) - Ultimate Forward Rate quote,
           LLFR(t) - Last Liquid Forward Rate quote,
           B(t-T_c) = [1 - exp(-a * (T-T_c))] / [a * (T-T_c)],
           with a being the growth factor (alpha). */
        if (deltaT > 0.0) {
            InterestRate baseRate = originalCurve_->zeroRate(cutOffTime, Continuous, NoFrequency);
            Real beta = (1.0 - std::exp(-alpha_ * deltaT)) / (alpha_ * deltaT);
            Rate extrapolatedForward = ufr_->value() + (llfr_->value() - ufr_->value()) * beta;
            return applyRounding((cutOffTime * baseRate + deltaT * extrapolatedForward) / t, t);
        }
        return applyRounding(originalCurve_->zeroRate(t, Continuous, NoFrequency), t);
    }
}

#endif