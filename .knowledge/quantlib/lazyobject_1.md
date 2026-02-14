n settings
        //@{
        /*! This method causes the object to forward the first notification received,
            and discard the others until recalculated; the rationale is that observers
            were already notified, and don't need further notifications until they
            recalculate, at which point this object would be recalculated too.
            After recalculation, this object would again forward the first notification
            received.

            Although not always correct, this behavior is a lot faster
            and thus is the current default.  The default can be
            changed at compile time, or at at run time by calling
            `LazyObject::Defaults::instance().alwaysForwardNotifications()`;
            the run-time change won't affect lazy objects already created.
        */
        void forwardFirstNotificationOnly();

        /*! This method causes the object to forward all notifications received.

            Although safer, this behavior is a lot slower and thus
            usually not the default.  The default can be changed at
            compile time, or at run-time by calling
            `LazyObject::Defaults::instance().alwaysForwardNotifications()`;
            the run-time change won't affect lazy objects already
            created.
        */
        void alwaysForwardNotifications();
        //@}

      protected:
        mutable bool calculated_ = false, frozen_ = false, alwaysForward_;
      private:
        bool updating_ = false;
        class UpdateChecker {  // NOLINT(cppcoreguidelines-special-member-functions)
            LazyObject* subject_;
          public:
            explicit UpdateChecker(LazyObject* subject) : subject_(subject) {
                subject_->updating_ = true;
            }
            ~UpdateChecker() {
                subject_->updating_ = false;
            }
        };
      public:
        class Defaults;
    };

    //! Per-session settings for the LazyObject class
    class LazyObject::Defaults : public Singleton<LazyObject::Defaults> {
        friend class Singleton<LazyObject::Defaults>;
      private:
        Defaults() = default;

      public:
        /*! by default, lazy objects created after calling this method
            will only forward the first notification after successful
            recalculation; see
            LazyObject::forwardFirstNotificationOnly for details.
        */
        void forwardFirstNotificationOnly() {
            forwardsAllNotifications_ = false;
        }

        /*! by default, lazy objects created after calling this method
            will always forward notifications; see
            LazyObject::alwaysForwardNotifications for details.
        */
        void alwaysForwardNotifications() {
            forwardsAllNotifications_ = true;
        }

        //! returns the current default
        bool forwardsAllNotifications() const {
            return forwardsAllNotifications_;
        }

      private:
        #ifdef QL_FASTER_LAZY_OBJECTS
        bool forwardsAllNotifications_ = false;
        #else
        bool forwardsAllNotifications_ = true;
        #endif
    };

    // inline definitions

    inline LazyObject::LazyObject()
    : alwaysForward_(LazyObject::Defaults::instance().forwardsAllNotifications()) {}

    inline void LazyObject::update() {
        if (updating_) {
            #ifdef QL_THROW_IN_CYCLES
            QL_FAIL("recursive notification loop detected; you probably created an object cycle");
            #else
            return;
            #endif
        }

        // This sets updating to true (so the above check breaks the
        // infinite loop if we enter this method recursively) and will
        // set it back to false when we exit this scope, either
        // successfully or because of an exception.
        UpdateChecker checker(this);

        // forwards notifications only the first time
        if (calculated_ || alwaysForward_) {
            // set to fal
