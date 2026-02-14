     updateInterpolation();
            YieldTermStructure::update();
        } else {
            /* The implementation inherited from YieldTermStructure
               asks for our reference date, which we don't have since
               the original curve is still not set. Therefore, we skip
               over that and just call the base-class behavior. */
            // NOLINTNEXTLINE(bugprone-parent-virtual-call)
            TermStructure::update();
        }
    }

    template <class T>
    inline void InterpolatedPiecewiseForwardSpreadedTermStructure<T>::updateInterpolation() {
        for (Size i = 0; i < dates_.size(); i++) {
            times_[i] = timeFromReference(dates_[i]);
            spreadValues_[i] = spreads_[i]->value();
        }
        interpolator_ = factory_.interpolate(times_.begin(),
                                             times_.end(),
                                             spreadValues_.begin());
    }

}


#endif
