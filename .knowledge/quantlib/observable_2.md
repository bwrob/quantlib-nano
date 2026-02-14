          observable->unregisterObserver(this);
    }

    inline std::pair<Observer::iterator, bool>
    Observer::registerWith(const ext::shared_ptr<Observable>& h) {
        if (h != nullptr) {
            h->registerObserver(this);
            return observables_.insert(h);
        }
        return std::make_pair(observables_.end(), false);
    }

    inline void
    Observer::registerWithObservables(const ext::shared_ptr<Observer> &o) {
        if (o != nullptr) {
            for (const auto& observable : o->observables_)
                registerWith(observable);
        }
    }

    inline
    Size Observer::unregisterWith(const ext::shared_ptr<Observable>& h) {
        if (h != nullptr)
            h->unregisterObserver(this);
        return observables_.erase(h);
    }

    inline void Observer::unregisterWithAll() {
        for (const auto& observable : observables_)
            observable->unregisterObserver(this);
        observables_.clear();
    }

    inline void Observer::deepUpdate() {
        update();
    }

}

#else

#ifndef QL_USE_STD_SHARED_PTR
#include <boost/smart_ptr/owner_less.hpp>
#endif
#include <atomic>
#include <mutex>
#include <set>
#include <thread>

namespace QuantLib {

    class Observable;
    class ObservableSettings;

    //! Object that gets notified when a given observable changes
    /*! \ingroup patterns */
    class Observer : public ext::enable_shared_from_this<Observer> {
        friend class Observable;
        friend class ObservableSettings;
      private:
        typedef std::set<ext::shared_ptr<Observable>> set_type;
      public:
        typedef set_type::iterator iterator;

        // constructors, assignment, destructor
        Observer() {}
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

        class Proxy {
          public:
            explicit Proxy(Observer* const observer)
             : active_  (true),
               observer_(observer) {
            }

            void update() const {
                std::lock_guard<std::recursive_mutex> lock(mutex_);
                if (active_) {
                    // c++17 is required if used with std::shared_ptr<T>
                    const ext::weak_ptr<Observer> o
                        = observer_->weak_from_this();

                    //check for empty weak reference
                    //https://stackoverflow.com/questions/45507041/how-to-check-if-weak-ptr-is-empty-non-assigned
                    const ext::weak_ptr<Observer> empty;
                    if (o.owner_before(empty) || empty.owner_before(o)) {
                        const ext::shared_ptr<Observer> obs(o.lock());
                        if (obs)
                            obs->update();
                    }
                    else {
                        observer_->update();
               