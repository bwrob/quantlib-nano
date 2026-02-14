dar::WesternImpl {
          public:
            std::string name() const override {
                return "North American Energy Reliability Council";
            }
            bool isBusinessDay(const Date&) const override;
        };
        class FederalReserveImpl final : public Calendar::WesternImpl {
          public:
            std::string name() const override { return "Federal Reserve Bankwire System"; }
            bool isBusinessDay(const Date&) const override;
        };
      public:
        //! US calendars
        enum Market { Settlement,     //!< generic settlement calendar
                      NYSE,           //!< New York stock exchange calendar
                      GovernmentBond, //!< government-bond calendar
                      NERC,           //!< off-peak days for NERC
                      LiborImpact,    //!< Libor impact calendar
                      FederalReserve, //!< Federal Reserve Bankwire System
                      SOFR            //!< SOFR fixing calendar
        };

        explicit UnitedStates(Market market);
    };

}


#endif