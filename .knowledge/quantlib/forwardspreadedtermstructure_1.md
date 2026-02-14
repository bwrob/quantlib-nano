
            YieldTermStructure::update();
            enableExtrapolation(originalCurve_->allowsExtrapolation());
        } else {
            /* The implementation inherited from YieldTermStructure
               asks for our reference date, which we don't have since
               the original curve is still not set. Therefore, we skip
               over that and just call the base-class behavior. */
            // NOLINTNEXTLINE(bugprone-parent-virtual-call)
            TermStructure::update();
        }
    }

    inline Rate ForwardSpreadedTermStructure::forwardImpl(Time t) const {
        return originalCurve_->forwardRate(t, t, Continuous, NoFrequency, true)
            + spread_->value();
    }

    inline Rate ForwardSpreadedTermStructure::zeroYieldImpl(Time t) const {
        return originalCurve_->zeroRate(t, Continuous, NoFrequency, true)
            + spread_->value();
    }

}

#endif
