::vector<Rate> floorRates_;
    };

    //! Concrete YoY Inflation cap class
    /*! \ingroup instruments */
    class YoYInflationCap : public YoYInflationCapFloor {
      public:
        YoYInflationCap(const Leg& yoyLeg,
            const std::vector<Rate>& exerciseRates)
        : YoYInflationCapFloor(YoYInflationCapFloor::Cap, yoyLeg,
                   exerciseRates, std::vector<Rate>()) {}
    };

    //! Concrete YoY Inflation floor class
    /*! \ingroup instruments */
    class YoYInflationFloor : public YoYInflationCapFloor {
      public:
        YoYInflationFloor(const Leg& yoyLeg,
              const std::vector<Rate>& exerciseRates)
        : YoYInflationCapFloor(YoYInflationCapFloor::Floor, yoyLeg,
                   std::vector<Rate>(), exerciseRates) {}
    };

    //! Concrete YoY Inflation collar class
    /*! \ingroup instruments */
    class YoYInflationCollar : public YoYInflationCapFloor {
      public:
        YoYInflationCollar(const Leg& yoyLeg,
               const std::vector<Rate>& capRates,
               const std::vector<Rate>& floorRates)
        : YoYInflationCapFloor(YoYInflationCapFloor::Collar, yoyLeg,
                               capRates, floorRates) {}
    };


    //! %Arguments for YoY Inflation cap/floor calculation
    class YoYInflationCapFloor::arguments
        : public virtual PricingEngine::arguments {
      public:
        arguments() : type(YoYInflationCapFloor::Type(-1)) {}
        YoYInflationCapFloor::Type type;
        ext::shared_ptr<YoYInflationIndex> index;
        Period observationLag;
        std::vector<Date> startDates;
        std::vector<Date> fixingDates;
        std::vector<Date> payDates;
        std::vector<Time> accrualTimes;
        std::vector<Rate> capRates;
        std::vector<Rate> floorRates;
        std::vector<Real> gearings;
        std::vector<Real> spreads;
        std::vector<Real> nominals;
        void validate() const override;
    };

    //! base class for cap/floor engines
    class YoYInflationCapFloor::engine
    : public GenericEngine<YoYInflationCapFloor::arguments,
                           YoYInflationCapFloor::results> {};

    std::ostream& operator<<(std::ostream&, YoYInflationCapFloor::Type);

    // inline

    inline Volatility YoYInflationCapFloor::impliedVolatility(
                            Real,
                            const Handle<YoYInflationTermStructure>&,
                            Volatility,
                            Real,
                            Natural,
                            Volatility,
                            Volatility) const {
            QL_FAIL("not implemented yet");
        }

}

#endif
