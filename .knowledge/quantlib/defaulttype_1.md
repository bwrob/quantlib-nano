e or a set of event types is within this
            one and as such will be recognised as a trigger. Not the
            same as equality.

            Notice that these methods do not include any event logical
            hierarchy. The match is in a strict sense. If event B is
            contained in (implied by) event A this would not send a
            match. This policies should be implemented at the
            CreditEvent class, which is polymorphic.
        */
        bool containsDefaultType(AtomicDefault::Type defType) const {
            return defTypes_ ==  defType;
        }

        bool containsRestructuringType(Restructuring::Type resType) const {
            return (restrType_ == resType) ||
                (Restructuring::AnyRestructuring == resType);
        }
    protected:
        //std::set<AtomicDefault::Type> defTypes_;
        AtomicDefault::Type defTypes_;
        Restructuring::Type restrType_;
    };


    /*! Equality is the criteria for indexing the curves. This depends
        only on the atomic types and not on idiosincracies of derived
        type as mentioned in the functional documentation (specific
        event characteristics are relevant to credit event matching
        but not to the probability meaning).  operator== is also used
        to remove duplicates in some containers. This ensures we do
        not have two equal events (despite having different
        characteristics) in those containers. This makes sense, theres
        no logic in having two FailureToPay in a contract even if they
        have different characteristics.
    */
    bool operator==(const DefaultType& lhs, const DefaultType& rhs);



    //! Failure to Pay atomic event type.
    class FailureToPay : public DefaultType {
      public:
        // Only atomic construction.
        // Amount contract by default is in dollars as per ISDA doc and not
        //   the contract curr. Theres an issue here...... FIX ME
        explicit FailureToPay(const Period& grace,
                              Real amount = 1.e+6)
        : DefaultType(AtomicDefault::FailureToPay, Restructuring::XR),
          gracePeriod_(grace), amountRequired_(amount) {}

        Real amountRequired() const {return amountRequired_;}
        const Period& gracePeriod() const {return gracePeriod_;}
      private:
        // Grace period to consider the event. If payment occurs during
        // the period the event should be removed from its container.
        Period gracePeriod_;
        // Minimum default amount triggering the event
        Real amountRequired_;
    };

}

#endif
