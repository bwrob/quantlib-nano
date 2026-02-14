t, this flag specifies whether or not CashFlows
            occurring on today's date should enter the NPV.  When the
            NPV date (i.e., the date at which the cash flows are
            discounted) equals today's date, this flag overrides the
            behavior chosen for includeReferenceDate. It cannot be overridden
            locally when calling the CashFlow::hasOccurred method.
        */
        ext::optional<bool>& includeTodaysCashFlows();
        ext::optional<bool> includeTodaysCashFlows() const;

        bool& enforcesTodaysHistoricFixings();
        bool enforcesTodaysHistoricFixings() const;

      private:
        DateProxy evaluationDate_;
        bool includeReferenceDateEvents_ = false;
        ext::optional<bool> includeTodaysCashFlows_;
        bool enforcesTodaysHistoricFixings_ = false;
    };


    // helper class to temporarily and safely change the settings
    class SavedSettings { // NOLINT(cppcoreguidelines-special-member-functions)
      public:
        SavedSettings();
        ~SavedSettings();
      private:
        Date evaluationDate_;
        bool includeReferenceDateEvents_;
        ext::optional<bool> includeTodaysCashFlows_;
        bool enforcesTodaysHistoricFixings_;
    };


    // inline

    inline Settings::DateProxy::operator Date() const {
        if (value() == Date())
            return Date::todaysDate();
        else
            return value();
    }

    inline Settings::DateProxy& Settings::DateProxy::operator=(const Date& d) {
        if (value() != d) // avoid notifications if the date doesn't actually change
            ObservableValue<Date>::operator=(d);
        return *this;
    }

    inline Settings::DateProxy& Settings::evaluationDate() {
        return evaluationDate_;
    }

    inline const Settings::DateProxy& Settings::evaluationDate() const {
        return evaluationDate_;
    }

    inline bool& Settings::includeReferenceDateEvents() {
        return includeReferenceDateEvents_;
    }

    inline bool Settings::includeReferenceDateEvents() const {
        return includeReferenceDateEvents_;
    }

    inline ext::optional<bool>& Settings::includeTodaysCashFlows() {
        return includeTodaysCashFlows_;
    }

    inline ext::optional<bool> Settings::includeTodaysCashFlows() const {
        return includeTodaysCashFlows_;
    }

    inline bool& Settings::enforcesTodaysHistoricFixings() {
        return enforcesTodaysHistoricFixings_;
    }

    inline bool Settings::enforcesTodaysHistoricFixings() const {
        return enforcesTodaysHistoricFixings_;
    }

}

#endif