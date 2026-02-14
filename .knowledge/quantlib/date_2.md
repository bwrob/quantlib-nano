ate time object
        static boost::posix_time::time_duration::tick_type ticksPerSecond();
#endif

        //@}

      private:
        static Date::serial_type minimumSerialNumber();
        static Date::serial_type maximumSerialNumber();
        static void checkSerialNumber(Date::serial_type serialNumber);

#ifdef QL_HIGH_RESOLUTION_DATE
        boost::posix_time::ptime dateTime_;
#else
        Date::serial_type serialNumber_;
        static Date advance(const Date& d, Integer units, TimeUnit);
        static Integer monthLength(Month m, bool leapYear);
        static Integer monthOffset(Month m, bool leapYear);
        static Date::serial_type yearOffset(Year y);
#endif
    };

    /*! \relates Date
        \brief Difference in days between dates
    */
    Date::serial_type operator-(const Date&, const Date&);
    /*! \relates Date
        \brief Difference in days (including fraction of days) between dates
    */
    Time daysBetween(const Date&, const Date&);

    /*! \relates Date */
    bool operator==(const Date&, const Date&);
    /*! \relates Date */
    bool operator!=(const Date&, const Date&);
    /*! \relates Date */
    bool operator<(const Date&, const Date&);
    /*! \relates Date */
    bool operator<=(const Date&, const Date&);
    /*! \relates Date */
    bool operator>(const Date&, const Date&);
    /*! \relates Date */
    bool operator>=(const Date&, const Date&);

    /*!
      Compute a hash value of @p d.

      This method makes Date hashable via <tt>boost::hash</tt>.

      Example:

      \code{.cpp}
      #include <unordered_set>

      std::unordered_set<Date> set;
      Date d = Date(1, Jan, 2020);

      set.insert(d);
      assert(set.count(d)); // 'd' was added to 'set'
      \endcode

      \param [in] d Date to hash
      \return A hash value of @p d
      \relates Date
    */
    std::size_t hash_value(const Date& d);

    /*! \relates Date */
    std::ostream& operator<<(std::ostream&, const Date&);

    namespace detail {

        struct short_date_holder {
            explicit short_date_holder(const Date d) : d(d) {}
            Date d;
        };
        std::ostream& operator<<(std::ostream&, const short_date_holder&);

        struct long_date_holder {
            explicit long_date_holder(const Date& d) : d(d) {}
            Date d;
        };
        std::ostream& operator<<(std::ostream&, const long_date_holder&);

        struct iso_date_holder {
            explicit iso_date_holder(const Date& d) : d(d) {}
            Date d;
        };
        std::ostream& operator<<(std::ostream&, const iso_date_holder&);

        struct formatted_date_holder {
            formatted_date_holder(const Date& d, std::string f) : d(d), f(std::move(f)) {}
            Date d;
            std::string f;
        };
        std::ostream& operator<<(std::ostream&,
                                 const formatted_date_holder&);

#ifdef QL_HIGH_RESOLUTION_DATE
        struct iso_datetime_holder {
            explicit iso_datetime_holder(const Date& d) : d(d) {}
            Date d;
        };
        std::ostream& operator<<(std::ostream&, const iso_datetime_holder&);
#endif
    }

    namespace io {

        //! output dates in short format (mm/dd/yyyy)
        /*! \ingroup manips */
        detail::short_date_holder short_date(const Date&);

        //! output dates in long format (Month ddth, yyyy)
        /*! \ingroup manips */
        detail::long_date_holder long_date(const Date&);

        //! output dates in ISO format (yyyy-mm-dd)
        /*! \ingroup manips */
        detail::iso_date_holder iso_date(const Date&);

        //! output dates in user defined format using boost date functionality
        /*! \ingroup manips */
        detail::formatted_date_holder formatted_date(const Date&,
                                                     const std::string& fmt);

#ifdef QL_HIGH_RESOLUTION_DATE
        //! output datetimes in ISO format (YYYY-MM-DDThh:mm:ss,SSSSSS)
        /*! \ingroup ma
