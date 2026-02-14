() const override { return "Frankfurt stock exchange"; }
            bool isBusinessDay(const Date&) const override;
        };
        class XetraImpl final : public Calendar::WesternImpl {
          public:
            std::string name() const override { return "Xetra"; }
            bool isBusinessDay(const Date&) const override;
        };
        class EurexImpl final : public Calendar::WesternImpl {
          public:
            std::string name() const override { return "Eurex"; }
            bool isBusinessDay(const Date&) const override;
        };
        class EuwaxImpl final : public Calendar::WesternImpl {
        public:
          std::string name() const override { return "Euwax"; }
          bool isBusinessDay(const Date&) const override;
        };

      public:
        //! German calendars
        enum Market { Settlement,             //!< generic settlement calendar
                      FrankfurtStockExchange, //!< Frankfurt stock-exchange
                      Xetra,                  //!< Xetra
                      Eurex,                  //!< Eurex
                      Euwax                   //!< Euwax
        };
        Germany(Market market = FrankfurtStockExchange);
    };

}


#endif
