const_iterator const_iterator;
        const_iterator begin() const { return dates_.begin(); }
        const_iterator end() const { return dates_.end(); }
        const_iterator lower_bound(const Date& d = Date()) const;
        //@}
        //! \name Utilities
        //@{
        //! truncated schedule
        Schedule after(const Date& truncationDate) const;
        Schedule until(const Date& truncationDate) const;
        //@}
      private:
        ext::optional<Period> tenor_;
        Calendar calendar_;
        BusinessDayConvention convention_;
        ext::optional<BusinessDayConvention> terminationDateConvention_;
        ext::optional<DateGeneration::Rule> rule_;
        ext::optional<bool> endOfMonth_;
        Date firstDate_, nextToLastDate_;
        std::vector<Date> dates_;
        std::vector<bool> isRegular_;
    };


    //! helper class
    /*! This class provides a more comfortable interface to the
        argument list of Schedule's constructor.
    */
    class MakeSchedule {
      public:
        MakeSchedule& from(const Date& effectiveDate);
        MakeSchedule& to(const Date& terminationDate);
        MakeSchedule& withTenor(const Period&);
        MakeSchedule& withFrequency(Frequency);
        MakeSchedule& withCalendar(const Calendar&);
        MakeSchedule& withConvention(BusinessDayConvention);
        MakeSchedule& withTerminationDateConvention(BusinessDayConvention);
        MakeSchedule& withRule(DateGeneration::Rule);
        MakeSchedule& forwards();
        MakeSchedule& backwards();
        MakeSchedule& endOfMonth(bool flag=true);
        MakeSchedule& withFirstDate(const Date& d);
        MakeSchedule& withNextToLastDate(const Date& d);
        operator Schedule() const;
      private:
        Calendar calendar_;
        Date effectiveDate_, terminationDate_;
        ext::optional<Period> tenor_;
        ext::optional<BusinessDayConvention> convention_;
        ext::optional<BusinessDayConvention> terminationDateConvention_;
        DateGeneration::Rule rule_ = DateGeneration::Backward;
        bool endOfMonth_ = false;
        Date firstDate_, nextToLastDate_;
    };

    /*! Helper function for returning the date on or before date \p d that is the 20th of the month and obeserves the 
        given date generation \p rule if it is relevant.
    */
    Date previousTwentieth(const Date& d, DateGeneration::Rule rule);

    // inline definitions

    inline const Date& Schedule::date(Size i) const {
        return dates_.at(i);
    }

    inline const Date& Schedule::operator[](Size i) const {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        return dates_.at(i);
        #else
        return dates_[i];
        #endif
    }

    inline const Date& Schedule::at(Size i) const {
        return dates_.at(i);
    }

    inline const Date& Schedule::front() const {
        QL_REQUIRE(!dates_.empty(), "no front date for empty schedule");
        return dates_.front();
    }

    inline const Date& Schedule::back() const {
        QL_REQUIRE(!dates_.empty(), "no back date for empty schedule");
        return dates_.back();
    }

    inline const Calendar& Schedule::calendar() const {
        return calendar_;
    }

    inline const Date& Schedule::startDate() const {
        QL_REQUIRE(!dates_.empty(), "empty Schedule: no start date"); 
        return dates_.front();
    }

    inline const Date &Schedule::endDate() const {
        // Checks to avoid segfault, issue #2302
        QL_REQUIRE(!dates_.empty(), "empty Schedule: no end date"); 
        return dates_.back(); 
    }

    inline bool Schedule::hasTenor() const {
        return static_cast<bool>(tenor_);
    }

    inline const Period& Schedule::tenor() const {
        QL_REQUIRE(hasTenor(),
                   "full interface (tenor) not available");
        return *tenor_;  // NOLINT(bugprone-unchecked-optional-access)
    }

    inline BusinessDayConvention Schedule::businessDayConvention() const {
        return convention_;
    }

 