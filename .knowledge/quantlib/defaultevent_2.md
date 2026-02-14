ntDate,
                          const Currency& curr,
                          Seniority bondsSen,
                          Real defaultedAmount,
                          // Settlement information:
                          const Date& settleDate,
                          const std::map<Seniority, Real>& recoveryRates);
        FailureToPayEvent(const Date& creditEventDate,
                          const Currency& curr,
                          Seniority bondsSen,
                          Real defaultedAmount,
                          // Settlement information:
                          const Date& settleDate,
                          Real recoveryRates);
        Real amountDefaulted() const {return defaultedAmount_;}
        bool matchesEventType(const ext::shared_ptr<DefaultType>& contractEvType) const override;

      private:
        Real defaultedAmount_;
    };


    // ------------------------------------------------------------------------

    class BankruptcyEvent : public DefaultEvent {
      public:
        BankruptcyEvent(const Date& creditEventDate,
                        const Currency& curr,
                        Seniority bondsSen,
                        // Settlement information:
                        const Date& settleDate,
                        const std::map<Seniority, Real>& recoveryRates);
        BankruptcyEvent(const Date& creditEventDate,
                        const Currency& curr,
                        Seniority bondsSen,
                        // Settlement information:
                        const Date& settleDate,
                        // means same for all
                        Real recoveryRates);
        //! This is a stronger than all event and will trigger all of them.
        bool matchesEventType(const ext::shared_ptr<DefaultType>&) const override { return true; }
    };

}

#endif
