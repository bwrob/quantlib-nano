   successful = false;
                    errMsg = e.what();
                } catch (...) {
                    successful = false;
                }
            }

            deferredObservers_.clear();

            QL_ENSURE(successful,
                  "could not notify one or more observers: " << errMsg);
        }
    }


    /*! \warning notification is sent before the copy constructor has
             a chance of actually change the data
             members. Therefore, observers whose update() method
             tries to use their observables will not see the
             updated values. It is suggested that the update()
             method just raise a flag in order to trigger
            a later recalculation.
    */
    inline Observable& Observable::operator=(const Observable& o) {
        // as above, the observer set is not copied. Moreover,
        // observers of this object must be notified of the change
        if (&o != this)
            notifyObservers();
        return *this;
    }

    inline Observer::Observer(const Observer& o) {
        proxy_.reset(new Proxy(this));

        {
             std::lock_guard<std::recursive_mutex> lock(o.mutex_);
             observables_ = o.observables_;
        }

        for (const auto& observable : observables_)
            observable->registerObserver(proxy_);
    }

    inline Observer& Observer::operator=(const Observer& o) {
        std::lock_guard<std::recursive_mutex> lock(mutex_);
        if (!proxy_) {
            proxy_.reset(new Proxy(this));
        }

        for (const auto& observable : observables_)
            observable->unregisterObserver(proxy_, true);

        {
            std::lock_guard<std::recursive_mutex> lock(o.mutex_);
            observables_ = o.observables_;
        }
        for (const auto& observable : observables_)
            observable->registerObserver(proxy_);

        return *this;
    }

    inline Observer::~Observer() {
        std::lock_guard<std::recursive_mutex> lock(mutex_);
        if (proxy_)
            proxy_->deactivate();

        for (const auto& observable : observables_)
            observable->unregisterObserver(proxy_, false);
    }

    inline std::pair<Observer::iterator, bool>
    Observer::registerWith(const ext::shared_ptr<Observable>& h) {
        std::lock_guard<std::recursive_mutex> lock(mutex_);
        if (!proxy_) {
            proxy_.reset(new Proxy(this));
        }

        if (h) {
            h->registerObserver(proxy_);
            return observables_.insert(h);
        }
        return std::make_pair(observables_.end(), false);
    }

    inline void
    Observer::registerWithObservables(const ext::shared_ptr<Observer>& o) {
        if (o) {
            std::lock_guard<std::recursive_mutex> lock(o->mutex_);

            for (const auto& observable : o->observables_)
                registerWith(observable);
        }
    }

    inline
    Size Observer::unregisterWith(const ext::shared_ptr<Observable>& h) {
        std::lock_guard<std::recursive_mutex> lock(mutex_);

        if (h && proxy_)  {
            h->unregisterObserver(proxy_, true);
        }

        return observables_.erase(h);
    }

    inline void Observer::unregisterWithAll() {
        std::lock_guard<std::recursive_mutex> lock(mutex_);

        for (const auto& observable : observables_)
            observable->unregisterObserver(proxy_, true);

        observables_.clear();
    }

    inline void Observer::deepUpdate() {
        update();
    }
}
#endif
#endif
