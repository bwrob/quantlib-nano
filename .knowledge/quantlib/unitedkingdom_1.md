isBusinessDay(const Date&) const override;
        };
      public:
        //! UK calendars
        enum Market { Settlement,     //!< generic settlement calendar
                      Exchange,       //!< London stock-exchange calendar
                      Metals          //|< London metals-exchange calendar
        };
        UnitedKingdom(Market market = Settlement);
    };

}


#endif