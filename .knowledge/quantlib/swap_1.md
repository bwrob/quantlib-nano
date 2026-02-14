   const Leg& leg(Size j) const {
            QL_REQUIRE(j<legs_.size(), "leg #" << j << " doesn't exist!");
            return legs_[j];
        }
        bool payer(Size j) const {
            QL_REQUIRE(j<legs_.size(), "leg #" << j << " doesn't exist!");
            return payer_[j] < 0.0;
        }
        //@}
      protected:
        //! \name Constructors
        //@{
        /*! This constructor can be used by derived classes that will
            build their legs themselves.
        */
        Swap(Size legs);
        //@}
        //! \name Instrument interface
        //@{
        void setupExpired() const override;
        //@}
        // data members
        std::vector<Leg> legs_;
        std::vector<Real> payer_;
        mutable std::vector<Real> legNPV_;
        mutable std::vector<Real> legBPS_;
        mutable std::vector<DiscountFactor> startDiscounts_, endDiscounts_;
        mutable DiscountFactor npvDateDiscount_;
    };


    class Swap::arguments : public virtual PricingEngine::arguments {
      public:
        std::vector<Leg> legs;
        std::vector<Real> payer;
        void validate() const override;
    };

    class Swap::results : public Instrument::results {
      public:
        std::vector<Real> legNPV;
        std::vector<Real> legBPS;
        std::vector<DiscountFactor> startDiscounts, endDiscounts;
        DiscountFactor npvDateDiscount;
        void reset() override;
    };

    class Swap::engine : public GenericEngine<Swap::arguments,
                                              Swap::results> {};

    std::ostream& operator<<(std::ostream& out, Swap::Type t);

}

#endif