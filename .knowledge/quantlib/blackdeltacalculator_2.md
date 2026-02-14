rikeClass {
      public:
        BlackDeltaPremiumAdjustedMaxStrikeClass(
                        Option::Type ot,
                        DeltaVolQuote::DeltaType dt,
                        Real spot,
                        DiscountFactor dDiscount,   // domestic discount
                        DiscountFactor fDiscount,   // foreign  discount
                        Real stdDev);

        Real operator()(Real strike) const;

      private:
        BlackDeltaCalculator bdc_;
        Real stdDev_;
    };

}


#endif
