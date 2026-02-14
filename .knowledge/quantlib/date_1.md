        //! More traditional constructor.
        Date(Day d, Month m, Year y);

#ifdef QL_HIGH_RESOLUTION_DATE
        //! Constructor taking boost posix date time object
        explicit Date(const boost::posix_time::ptime& localTime);
        //! More traditional constructor.
        Date(Day d, Month m, Year y,
             Hour hours, Minute minutes, Second seconds,
             Millisecond millisec = 0, Microsecond microsec = 0);
#endif
        //@}

        //! \name inspectors
        //@{
        Weekday weekday() const;
        Day dayOfMonth() const;
        //! One-based (Jan 1st = 1)
        Day dayOfYear() const;
        Month month() const;
        Year year() const;
        Date::serial_type serialNumber() const;

#ifdef QL_HIGH_RESOLUTION_DATE
        Hour hours() const;
        Minute minutes() const;
        Second seconds() const;
        Millisecond milliseconds() const;
        Microsecond microseconds() const;

        Time fractionOfDay() const;
        Time fractionOfSecond() const;

        const boost::posix_time::ptime& dateTime() const;
#endif
        //@}

        //! \name date algebra
        //@{
        //! increments date by the given number of days
        Date& operator+=(Date::serial_type days);
        //! increments date by the given period
        Date& operator+=(const Period&);
        //! decrement date by the given number of days
        Date& operator-=(Date::serial_type days);
        //! decrements date by the given period
        Date& operator-=(const Period&);
        //! 1-day pre-increment
        Date& operator++();
        //! 1-day post-increment
        Date operator++(int );
        //! 1-day pre-decrement
        Date& operator--();
        //! 1-day post-decrement
        Date operator--(int );
        //! returns a new date incremented by the given number of days
        Date operator+(Date::serial_type days) const;
        //! returns a new date incremented by the given period
        Date operator+(const Period&) const;
        //! returns a new date decremented by the given number of days
        Date operator-(Date::serial_type days) const;
        //! returns a new date decremented by the given period
        Date operator-(const Period&) const;
        //@}

        //! \name static methods
        //@{
        //! today's date.
        static Date todaysDate();
        //! earliest allowed date
        static Date minDate();
        //! latest allowed date
        static Date maxDate();
        //! whether the given year is a leap one
        static bool isLeap(Year y);
        //! first day of the month to which the given date belongs
        static Date startOfMonth(const Date& d);
        //! whether a date is the first day of its month
        static bool isStartOfMonth(const Date& d);
        //! last day of the month to which the given date belongs
        static Date endOfMonth(const Date& d);
        //! whether a date is the last day of its month
        static bool isEndOfMonth(const Date& d);
        //! next given weekday following or equal to the given date
        /*! E.g., the Friday following Tuesday, January 15th, 2002
            was January 18th, 2002.

            see http://www.cpearson.com/excel/DateTimeWS.htm
        */
        static Date nextWeekday(const Date& d,
                                Weekday w);
        //! n-th given weekday in the given month and year
        /*! E.g., the 4th Thursday of March, 1998 was March 26th,
            1998.

            see http://www.cpearson.com/excel/DateTimeWS.htm
        */
        static Date nthWeekday(Size n,
                               Weekday w,
                               Month m,
                               Year y);

#ifdef QL_HIGH_RESOLUTION_DATE
        //! local date time, based on the time zone settings of the computer
        static Date localDateTime();
        //! UTC date time
        static Date universalDateTime();

        //! underlying resolution of the  posix d