  Leg floatingLeg_;
        std::vector<Rate> capRates_;
        std::vector<Rate> floorRates_;
    };

    //! Concrete cap class
    /*! \ingroup instruments */
    class Cap : public CapFloor {
      public:
        Cap(const Leg& floatingLeg,
            const std::vector<Rate>& exerciseRates)
        : CapFloor(CapFloor::Cap, floatingLeg,
                   exerciseRates, std::vector<Rate>()) {}
    };

    //! Concrete floor class
    /*! \ingroup instruments */
    class Floor : public CapFloor {
      public:
        Floor(const Leg& floatingLeg,
              const std::vector<Rate>& exerciseRates)
        : CapFloor(CapFloor::Floor, floatingLeg,
                   std::vector<Rate>(), exerciseRates) {}
    };

    //! Concrete collar class
    /*! \ingroup instruments */
    class Collar : public CapFloor {
      public:
        Collar(const Leg& floatingLeg,
               const std::vector<Rate>& capRates,
               const std::vector<Rate>& floorRates)
        : CapFloor(CapFloor::Collar, floatingLeg, capRates, floorRates) {}
    };


    //! %Arguments for cap/floor calculation
    class CapFloor::arguments : public virtual PricingEngine::arguments {
      public:
        arguments() : type(CapFloor::Type(-1)) {}
        CapFloor::Type type;
        std::vector<Date> startDates;
        std::vector<Date> fixingDates;
        std::vector<Date> endDates;
        std::vector<Time> accrualTimes;
        std::vector<Rate> capRates;
        std::vector<Rate> floorRates;
        std::vector<Rate> forwards;
        std::vector<Real> gearings;
        std::vector<Real> spreads;
        std::vector<Real> nominals;
        std::vector<ext::shared_ptr<InterestRateIndex> > indexes;
        void validate() const override;
    };

    //! base class for cap/floor engines
    class CapFloor::engine
        : public GenericEngine<CapFloor::arguments, CapFloor::results> {};

    std::ostream& operator<<(std::ostream&, CapFloor::Type);

}

#endif
