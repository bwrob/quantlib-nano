t::shared_ptr<Observable>> set_type;
      public:
        typedef set_type::iterator iterator;

        // constructors, assignment, destructor
        Observer() = default;
        Observer(const Observer&);
        Observer& operator=(const Observer&);
        virtual ~Observer();

        // observer interface
        std::pair<iterator, bool>
        registerWith(const ext::shared_ptr<Observable>&);

        /*! register with all observables of a given observer. Note
            that this does not include registering with the observer
            itself.
        */
        void registerWithObservables(const ext::shared_ptr<Observer>&);

        Size unregisterWith(const ext::shared_ptr<Observable>&);
        void unregisterWithAll();

        /*! This method must be implemented in derived classes. An
            instance of %Observer does not call this method directly:
            instead, it will be called by the observables the instance
            registered with when they need to notify any changes.
        */
        virtual void update() = 0;

        /*! This method allows to explicitly update the instance itself
          and nested observers. If notifications are disabled a call to
          this method ensures an update of such nested observers. It
          should be implemented in derived classes whenever applicable */
        virtual void deepUpdate();

      private:
        set_type observables_;
    };


    // inline definitions

    inline void ObservableSettings::registerDeferredObservers(const Observable::set_type& observers) {
        if (updatesDeferred()) {
            for (Observer* obs : observers)
                deferredObservers_.emplace(obs, true);
        }
    }

    inline void ObservableSettings::unregisterDeferredObserver(Observer* o) {
        if (updatesDeferred())
            deferredObservers_.erase(o);
        else
        {
            auto it = deferredObservers_.find(o);
            if (it != deferredObservers_.end())
                it->second = false;
        }
    }

    inline Observable::Observable(const Observable&) {
        // the observer set is not copied; no observer asked to
        // register with this object
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

    inline std::pair<Observable::iterator, bool>
    Observable::registerObserver(Observer* o) {
        return observers_.insert(o);
    }

    inline Size Observable::unregisterObserver(Observer* o) {
        if (ObservableSettings::instance().updatesDeferred() ||
            ObservableSettings::instance().runningDeferredUpdates())
            ObservableSettings::instance().unregisterDeferredObserver(o);

        return observers_.erase(o);
    }


    inline Observer::Observer(const Observer& o)
    : observables_(o.observables_) {
        for (const auto& observable : observables_)
            observable->registerObserver(this);
    }

    inline Observer& Observer::operator=(const Observer& o) {
        for (const auto& observable : observables_)
            observable->unregisterObserver(this);
        observables_ = o.observables_;
        for (const auto& observable : observables_)
            observable->registerObserver(this);
        return *this;
    }

    inline Observer::~Observer() {
        for (const auto& observable : observables_)
  