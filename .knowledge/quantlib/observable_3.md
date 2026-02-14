     }
                }
            }

            void deactivate() {
                std::lock_guard<std::recursive_mutex> lock(mutex_);
                active_ = false;
            }

        private:
            bool active_;
            mutable std::recursive_mutex mutex_;
            Observer* const observer_;
        };

        ext::shared_ptr<Proxy> proxy_;
        mutable std::recursive_mutex mutex_;

        set_type observables_;
    };

    namespace detail {
        class Signal;
    }

    //! Object that notifies its changes to a set of observers
    /*! \ingroup patterns */
    class Observable {
        friend class Observer;
        friend class ObservableSettings;
      private:
        typedef std::set<ext::shared_ptr<Observer::Proxy>> set_type;
      public:
        typedef set_type::iterator iterator;

        // constructors, assignment, destructor
        Observable();
        Observable(const Observable&);
        Observable& operator=(const Observable&);
        virtual ~Observable() {}
        /*! This method should be called at the end of non-const methods
            or when the programmer desires to notify any changes.
        */
        void notifyObservers();
      private:
        void registerObserver(const ext::shared_ptr<Observer::Proxy>&);
        void unregisterObserver(
            const ext::shared_ptr<Observer::Proxy>& proxy, bool disconnect);

        ext::shared_ptr<detail::Signal> sig_;
        set_type observers_;
        mutable std::recursive_mutex mutex_;
    };

    //! global repository for run-time library settings
    class ObservableSettings : public Singleton<ObservableSettings> {
        friend class Singleton<ObservableSettings>;
        friend class Observable;

      public:
        void disableUpdates(bool deferred=false) {
            std::lock_guard<std::mutex> lock(mutex_);
            updatesType_ = (deferred) ? UpdatesDeferred : UpdatesDisabled;
        }
        void enableUpdates();

        bool updatesEnabled()  {return (updatesType_ & UpdatesEnabled) != 0; }
        bool updatesDeferred() {return (updatesType_ & UpdatesDeferred) != 0; }
      private:
        ObservableSettings() : updatesType_(UpdatesEnabled) {}

#if defined(QL_USE_STD_SHARED_PTR)
        typedef std::set<ext::weak_ptr<Observer::Proxy>,
                         std::owner_less<ext::weak_ptr<Observer::Proxy> > >
            set_type;
#else
        typedef std::set<ext::weak_ptr<Observer::Proxy>,
                         boost::owner_less<ext::weak_ptr<Observer::Proxy> > >
            set_type;
#endif

        void registerDeferredObservers(const Observable::set_type& observers);
        void unregisterDeferredObserver(const ext::shared_ptr<Observer::Proxy>& proxy);

        set_type deferredObservers_;
        mutable std::mutex mutex_;

        enum UpdateType { UpdatesDisabled = 0, UpdatesEnabled = 1, UpdatesDeferred = 2} ;
        std::atomic<int> updatesType_;
    };


    // inline definitions

    inline void ObservableSettings::registerDeferredObservers(const Observable::set_type& observers) {
        deferredObservers_.insert(observers.begin(), observers.end());
    }

    inline void ObservableSettings::unregisterDeferredObserver(
        const ext::shared_ptr<Observer::Proxy>& o) {
        deferredObservers_.erase(o);
    }

    inline void ObservableSettings::enableUpdates() {
        std::lock_guard<std::mutex> lock(mutex_);

        // if there are outstanding deferred updates, do the notification
        updatesType_ = UpdatesEnabled;

        if (deferredObservers_.size()) {
            bool successful = true;
            std::string errMsg;

            for (auto i=deferredObservers_.begin();
                i!=deferredObservers_.end(); ++i) {
                try {
                    const ext::shared_ptr<Observer::Proxy> proxy = i->lock();
                    if (proxy)
                        proxy->update();
                } catch (std::exception& e) {
                 