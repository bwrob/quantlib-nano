se early
            // 1) to prevent infinite recursion
            // 2) otherways non-lazy observers would be served obsolete
            //    data because of calculated_ being still true
            calculated_ = false;
            // observers don't expect notifications from frozen objects
            if (!frozen_)
                notifyObservers();
                // exiting notifyObservers() calculated_ could be
                // already true because of non-lazy observers
        }
    }

    inline void LazyObject::recalculate() {
        bool wasFrozen = frozen_;
        calculated_ = frozen_ = false;
        try {
            calculate();
        } catch (...) {
            frozen_ = wasFrozen;
            notifyObservers();
            throw;
        }
        frozen_ = wasFrozen;
        notifyObservers();
    }

    inline void LazyObject::freeze() {
        frozen_ = true;
    }

    inline void LazyObject::unfreeze() {
        // send notifications, just in case we lost any,
        // but only once, i.e. if it was frozen
        if (frozen_) {
            frozen_ = false;
            notifyObservers();
        }
    }

    inline void LazyObject::forwardFirstNotificationOnly() {
        alwaysForward_ = false;
    }

    inline void LazyObject::alwaysForwardNotifications() {
        alwaysForward_ = true;
    }

    inline void LazyObject::calculate() const {
        if (!calculated_ && !frozen_) {
            calculated_ = true;   // prevent infinite recursion in
                                  // case of bootstrapping
            try {
                performCalculations();
            } catch (...) {
                calculated_ = false;
                throw;
            }
        }
    }

    inline bool LazyObject::isCalculated() const {
        return calculated_;
    }

    inline void LazyObject::setCalculated(const bool c) const {
        calculated_ = c;
    }
}

#endif