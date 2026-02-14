  };
        class ISMA_Impl final : public Thirty360_Impl {
          public:
            std::string name() const override { return std::string("30/360 (Bond Basis)"); }
            Date::serial_type dayCount(const Date& d1, const Date& d2) const override;
        };
        class EU_Impl final : public Thirty360_Impl {
          public:
            std::string name() const override { return std::string("30E/360 (Eurobond Basis)"); }
            Date::serial_type dayCount(const Date& d1, const Date& d2) const override;
        };
        class IT_Impl final : public Thirty360_Impl {
          public:
            std::string name() const override { return std::string("30/360 (Italian)"); }
            Date::serial_type dayCount(const Date& d1, const Date& d2) const override;
        };
        class ISDA_Impl final : public Thirty360_Impl {
          public:
            explicit ISDA_Impl(const Date& terminationDate)
            : terminationDate_(terminationDate) {}
            std::string name() const override { return std::string("30E/360 (ISDA)"); }
            Date::serial_type dayCount(const Date& d1, const Date& d2) const override;
          private:
            Date terminationDate_;
        };
        class NASD_Impl final : public Thirty360_Impl {
          public:
            std::string name() const override { return std::string("30/360 (NASD)"); }
            Date::serial_type dayCount(const Date& d1, const Date& d2) const override;
        };
        static ext::shared_ptr<DayCounter::Impl>
        implementation(Convention c, const Date& terminationDate);
      public:
        explicit Thirty360(Convention c, const Date& terminationDate = Date())
        : DayCounter(implementation(c, terminationDate)) {}
    };

}

#endif