nk_==other.link_; }
        //! disequality test
        template <class U>
        bool operator!=(const Handle<U>& other) const { return link_!=other.link_; }
        //! strict weak ordering
        template <class U>
        bool operator<(const Handle<U>& other) const { return link_ < other.link_; }
    };

    //! Relinkable handle to an observable
    /*! An instance of this class can be relinked so that it points to
        another observable. The change will be propagated to all
        handles that were created as copies of such instance.

        \pre Class T must inherit from Observable

        \warning see the Handle documentation for issues
                 relatives to <tt>registerAsObserver</tt>.
    */
    template <class T>
    class RelinkableHandle : public Handle<T> {
      public:
        RelinkableHandle()
        : RelinkableHandle(ext::shared_ptr<T>()) {}
        explicit RelinkableHandle(
                       const ext::shared_ptr<T>& p,
                       bool registerAsObserver = true);
        explicit RelinkableHandle(
                       ext::shared_ptr<T>&& p,
                       bool registerAsObserver = true);
        void linkTo(const ext::shared_ptr<T>& h,
                    bool registerAsObserver = true);
        void linkTo(ext::shared_ptr<T>&& h,
                    bool registerAsObserver = true);
        void reset();
    };


    // inline definitions

    template <class T>
    inline Handle<T>::Link::Link(const ext::shared_ptr<T>& h, bool registerAsObserver) {
        linkTo(h, registerAsObserver);
    }

    template <class T>
    inline Handle<T>::Link::Link(ext::shared_ptr<T>&& h, bool registerAsObserver) {
        linkTo(std::move(h), registerAsObserver);
    }

    template <class T>
    inline void Handle<T>::Link::linkTo(ext::shared_ptr<T> h,
                                        bool registerAsObserver) {
        if ((h != h_) || (isObserver_ != registerAsObserver)) {
            if (h_ && isObserver_)
                unregisterWith(h_);
            h_ = std::move(h);
            isObserver_ = registerAsObserver;
            if (h_ && isObserver_)
                registerWith(h_);
            notifyObservers();
        }
    }


    template <class T>
    inline const ext::shared_ptr<T>& Handle<T>::currentLink() const {
        QL_REQUIRE(!empty(), "empty Handle cannot be dereferenced");
        return link_->currentLink();
    }

    template <class T>
    inline const ext::shared_ptr<T>& Handle<T>::operator->() const {
        QL_REQUIRE(!empty(), "empty Handle cannot be dereferenced");
        return link_->currentLink();
    }

    template <class T>
    inline const ext::shared_ptr<T>& Handle<T>::operator*() const {
        QL_REQUIRE(!empty(), "empty Handle cannot be dereferenced");
        return link_->currentLink();
    }

    template <class T>
    inline bool Handle<T>::empty() const {
        return link_->empty();
    }

    template <class T>
    inline Handle<T>::operator ext::shared_ptr<Observable>() const {
        return link_;
    }


    template <class T>
    inline RelinkableHandle<T>::RelinkableHandle(const ext::shared_ptr<T>& p,
                                                 bool registerAsObserver)
    : Handle<T>(p,registerAsObserver) {}

    template <class T>
    inline RelinkableHandle<T>::RelinkableHandle(ext::shared_ptr<T>&& p,
                                                 bool registerAsObserver)
    : Handle<T>(std::move(p), registerAsObserver) {}

    template <class T>
    inline void RelinkableHandle<T>::linkTo(const ext::shared_ptr<T>& h,
                                            bool registerAsObserver) {
        this->link_->linkTo(h, registerAsObserver);
    }

    template <class T>
    inline void RelinkableHandle<T>::linkTo(ext::shared_ptr<T>&& h,
                                            bool registerAsObserver) {
        this->link_->linkTo(std::move(h), registerAsObserver);
    }

    template <class T>

