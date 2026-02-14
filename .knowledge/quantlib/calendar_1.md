       bool isWeekend(Weekday w) const;
        /*! Returns <tt>true</tt> iff in the given market, the date is on
            or before the first business day for that month.
        */
        bool isStartOfMonth(const Date& d) const;
        //! first business day of the month to which the given date belongs
        Date startOfMonth(const Date& d) const;
        /*! Returns <tt>true</tt> iff in the given market, the date is on
            or after the last business day for that month.
        */
        bool isEndOfMonth(const Date& d) const;
        //! last business day of the month to which the given date belongs
        Date endOfMonth(const Date& d) const;

        /*! Adds a date to the set of holidays for the given calendar. */
        void addHoliday(const Date&);
        /*! Removes a date from the set of holidays for the given calendar. */
        void removeHoliday(const Date&);

        /*! Returns the holidays between two dates. */
        std::vector<Date> holidayList(const Date& from,
                                      const Date& to,
                                      bool includeWeekEnds = false) const;
        /*! Returns the business days between two dates. */
        std::vector<Date> businessDayList(const Date& from,
                                          const Date& to) const;

        /*! Adjusts a non-business day to the appropriate near business day
            with respect to the given convention.
        */
        Date adjust(const Date&,
                    BusinessDayConvention convention = Following) const;
        /*! Advances the given date of the given number of business days and
            returns the result.
            \note The input date is not modified.
        */
        Date advance(const Date&,
                     Integer n,
                     TimeUnit unit,
                     BusinessDayConvention convention = Following,
                     bool endOfMonth = false) const;
        /*! Advances the given date as specified by the given period and
            returns the result.
            \note The input date is not modified.
        */
        Date advance(const Date& date,
                     const Period& period,
                     BusinessDayConvention convention = Following,
                     bool endOfMonth = false) const;
        /*! Calculates the number of business days between two given
            dates and returns the result.
        */
        Date::serial_type businessDaysBetween(const Date& from,
                                              const Date& to,
                                              bool includeFirst = true,
                                              bool includeLast = false) const;
        //@}

      protected:
        //! partial calendar implementation
        /*! This class provides the means of determining the Easter
            Monday for a given year, as well as specifying Saturdays
            and Sundays as weekend days.
        */
        class WesternImpl : public Impl {
          public:
            bool isWeekend(Weekday) const override;
            //! expressed relative to first day of year
            static Day easterMonday(Year);
        };
        //! partial calendar implementation
        /*! This class provides the means of determining the Orthodox
            Easter Monday for a given year, as well as specifying
            Saturdays and Sundays as weekend days.
        */
        class OrthodoxImpl : public Impl {
          public:
            bool isWeekend(Weekday) const override;
            //! expressed relative to first day of year
            static Day easterMonday(Year);
        };
    };

    /*! Returns <tt>true</tt> iff the two calendars belong to the same
        derived class.
        \relates Calendar
    */
    bool operator==(const Calendar&, const Calendar&);

    /*! \relates Calendar */
    bool operator!=(const Calendar&, const Calendar&);

    /*! \relates Calendar */
    std::
