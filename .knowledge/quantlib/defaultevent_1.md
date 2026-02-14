             const std::map<Seniority, Real>& recoveryRates = rate_map());
        /*! Use NoSeniority to settle to all seniorities with that
            recovery. In that case the event is assumed to have
            affected all seniorities.
        */
        DefaultEvent(const Date& creditEventDate,
                     const DefaultType& atomicEvType,
                     Currency curr,
                     Seniority bondsSen,
                     // Settlement information:
                     const Date& settleDate,
                     Real recoveryRate);

        Date date() const override;
        bool isRestructuring() const { return eventType_.isRestructuring(); }
        bool isDefault() const { return !isRestructuring();}
        bool hasSettled() const {
            return defSettlement_.date() != Date();
        }
        const DefaultSettlement& settlement() const {
            return defSettlement_;
        }
        const DefaultType& defaultType() const {
            return eventType_;
        }
        //! returns the currency of the bond this event refers to.
        const Currency& currency() const {
            return bondsCurrency_;
        }
        //! returns the seniority of the bond that triggered the event.
        Seniority eventSeniority() const {
            return bondsSeniority_;
        }
        /*! returns a value if the event lead to a settlement for the
            requested seniority.  Specializations on the default
            atomics and recoveries could change the default policy.
        */
        virtual Real recoveryRate(Seniority seniority) const {
            if(hasSettled()) {
                return defSettlement_.recoveryRate(seniority);
            }
            return Null<Real>();
        }

        /*! matches the event if this event would trigger a contract
            related to the requested event type.  Notice the
            contractual event types are not neccesarily atomic.
            Notice it does not check seniority or currency only event
            type.  typically used from Issuer
        */
        virtual bool matchesEventType(
                 const ext::shared_ptr<DefaultType>& contractEvType) const {
            // remember we are made of an atomic type.
            // behaviour by default...
            return
                contractEvType->containsRestructuringType(
                    eventType_.restructuringType()) &&
                contractEvType->containsDefaultType(
                    eventType_.defaultType());
        }
        /*! Returns true if this event would trigger a contract with
            the arguments characteristics.
        */
        virtual bool matchesDefaultKey(const DefaultProbKey& contractKey) const;

        void accept(AcyclicVisitor&) override;

      protected:
        Currency bondsCurrency_;
        Date defaultDate_;
        DefaultType eventType_;
        Seniority bondsSeniority_;
        DefaultSettlement defSettlement_;
    };

    /*! Two credit events are the same independently of their
        settlement member data. This has the side effect of
        overwriting different settlements from the same credit event
        when, say, inserting in a map. But on the other hand one given
        event can only have one settlement. This means we can not have
        two restructuring events on a bond on the same date.
    */
    bool operator==(const DefaultEvent& lhs, const DefaultEvent& rhs);

    inline bool operator!=(const DefaultEvent& lhs, const DefaultEvent& rhs) {
        return !(lhs == rhs);
    }

    template<>
    struct earlier_than<DefaultEvent> {
        bool operator()(const DefaultEvent& e1,
                        const DefaultEvent& e2) const {
            return e1.date() < e2.date();
        }
    };


    // ------------------------------------------------------------------------

    class FailureToPayEvent : public DefaultEvent {
      public:
        FailureToPayEvent(const Date& creditEve