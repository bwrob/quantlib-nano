
            dates of the fixings; no settlement days must be used.
        */
        void addFixings(const TimeSeries<Real>& t, bool forceOverwrite = false);
        //! stores historical fixings at the given dates
        /*! the dates passed as arguments must be the actual calendar
            dates of the fixings; no settlement days must be used.
        */
        template <class DateIterator, class ValueIterator>
        void addFixings(DateIterator dBegin,
                        DateIterator dEnd,
                        ValueIterator vBegin,
                        bool forceOverwrite = false) {
            checkNativeFixingsAllowed();
            IndexManager::instance().addFixings(
                name(), dBegin, dEnd, vBegin, forceOverwrite,
                [this](const Date& d) { return isValidFixingDate(d); });
        }
        //! clears all stored historical fixings
        void clearFixings();

      protected:
        ext::shared_ptr<Observable> notifier() const {
            QL_DEPRECATED_DISABLE_WARNING
            return IndexManager::instance().notifier(name());
            QL_DEPRECATED_ENABLE_WARNING
        }

      private:
        //! check if index allows for native fixings
        void checkNativeFixingsAllowed();

    };

    inline bool Index::hasHistoricalFixing(const Date& fixingDate) const {
        QL_DEPRECATED_DISABLE_WARNING
        return IndexManager::instance().hasHistoricalFixing(name(), fixingDate);
        QL_DEPRECATED_ENABLE_WARNING
    }

    inline Real Index::pastFixing(const Date& fixingDate) const {
        QL_REQUIRE(isValidFixingDate(fixingDate), fixingDate << " is not a valid fixing date");
        return timeSeries()[fixingDate];
    }

    inline void Index::update() {
        notifyObservers();
    }

}

#endif
