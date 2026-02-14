 to pillarDate()
        */
        virtual Date latestDate() const;
        //@}
        //! \name Observer interface
        //@{
        void update() override;
        //@}
        //! \name Visitability
        //@{
        virtual void accept(AcyclicVisitor&);
        //@}
      protected:
        Handle<Quote> quote_;
        TS* termStructure_;
        Date earliestDate_, latestDate_;
        Date maturityDate_, latestRelevantDate_, pillarDate_;
    };

    //! Bootstrap helper with date schedule relative to global evaluation date
    /*! Derived classes must takes care of rebuilding the date schedule when
        the global evaluation date changes
    */
    template <class TS>
    class RelativeDateBootstrapHelper : public BootstrapHelper<TS> {
      public:
        explicit RelativeDateBootstrapHelper(
            const std::variant<Spread, Handle<Quote>>& quote,
            bool updateDates = true);

        //! \name Observer interface
        //@{
        void update() override {
            if (updateDates_ && evaluationDate_ != Settings::instance().evaluationDate()) {
                evaluationDate_ = Settings::instance().evaluationDate();
                initializeDates();
            }
            BootstrapHelper<TS>::update();
        }
        //@}
      protected:
        virtual void initializeDates() = 0;
        Date evaluationDate_;
        bool updateDates_;
    };

    // template definitions

    template <class TS>
    BootstrapHelper<TS>::BootstrapHelper(const std::variant<Spread, Handle<Quote>>& quote)
    : quote_(handleFromVariant(quote)), termStructure_(nullptr) {
        registerWith(quote_);
    }

    template <class TS>
    void BootstrapHelper<TS>::setTermStructure(TS* t) {
        QL_REQUIRE(t != nullptr, "null term structure given");
        termStructure_ = t;
    }

    template <class TS>
    Date BootstrapHelper<TS>::earliestDate() const {
        return earliestDate_;
    }

    template <class TS>
    Date BootstrapHelper<TS>::maturityDate() const {
        if (maturityDate_ == Date())
            return latestRelevantDate();
        return maturityDate_;
    }

    template <class TS>
    Date BootstrapHelper<TS>::latestRelevantDate() const {
        if (latestRelevantDate_ == Date())
            return latestDate();
        return latestRelevantDate_;
    }

    template <class TS>
    Date BootstrapHelper<TS>::pillarDate() const {
        if (pillarDate_==Date())
            return latestDate();
        return pillarDate_;
    }

    template <class TS>
    Date BootstrapHelper<TS>::latestDate() const {
        if (latestDate_ == Date())
            return pillarDate_;
        return latestDate_;
    }

    template <class TS>
    void BootstrapHelper<TS>::update() {
        notifyObservers();
    }

    template <class TS>
    void BootstrapHelper<TS>::accept(AcyclicVisitor& v) {
        auto* v1 = dynamic_cast<Visitor<BootstrapHelper<TS> >*>(&v);
        if (v1 != nullptr)
            v1->visit(*this);
        else
            QL_FAIL("not a bootstrap-helper visitor");
    }


    template <class TS>
    RelativeDateBootstrapHelper<TS>::RelativeDateBootstrapHelper(
        const std::variant<Spread, Handle<Quote>>& quote, bool updateDates)
    : BootstrapHelper<TS>(quote), updateDates_(updateDates) {
        if (updateDates) {
            this->registerWith(Settings::instance().evaluationDate());
            evaluationDate_ = Settings::instance().evaluationDate();
        }
    }


    inline std::ostream& operator<<(std::ostream& out,
                                    Pillar::Choice t) {
        switch (t) {
        case Pillar::MaturityDate:
            return out << "MaturityPillarDate";
        case Pillar::LastRelevantDate:
            return out << "LastRelevantPillarDate";
        case Pillar::CustomDate:
            return out << "CustomPillarDate";
        default:
            QL_FAIL("unknown Pillar::Choice(" << Integer(t) << ")");
        }
    }

    namespace d
