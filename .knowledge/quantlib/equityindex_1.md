const Handle<YieldTermStructure>& interest,
                                                   const Handle<YieldTermStructure>& dividend,
                                                   const Handle<Quote>& spot) const;
        // @}
      private:
        std::string name_;
        Calendar fixingCalendar_;
        Currency currency_;
        Handle<YieldTermStructure> interest_;
        Handle<YieldTermStructure> dividend_;
        Handle<Quote> spot_;
    };

    inline bool EquityIndex::isValidFixingDate(const Date& d) const {
        return fixingCalendar().isBusinessDay(d);
    }
}

#endif