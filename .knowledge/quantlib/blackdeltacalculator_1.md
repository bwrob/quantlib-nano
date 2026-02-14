e that corresponds to "at-the-money" under different conventions
            commonly used in FX markets. This method does not require an explicit strike input
            as it determines the ATM level based on the specified convention.

            \param atmT The ATM convention to use:
                       - AtmNull: No ATM convention (returns null)
                       - AtmSpot: ATM strike equals the current spot rate
                       - AtmForward: ATM strike equals the forward rate
                       - AtmDeltaNeutral: ATM strike where call and put deltas sum to zero
                       - AtmVegaMax: ATM strike that maximizes vega (typically close to forward)
                       - AtmGammaMax: ATM strike that maximizes gamma
                       - AtmPutCall25: ATM strike where 25-delta call and put have equal volatility

            \return The ATM strike price according to the specified convention.

            \note This calculation is independent of the strike and uses the forward rate,
                  volatility, and time to expiration set at construction.
        */
        Real atmStrike(DeltaVolQuote::AtmType atmT) const;

        /*!
            \brief Sets the delta calculation convention.

            \param dt The new delta type convention:
        */
        void setDeltaType(DeltaVolQuote::DeltaType dt);

        /*!
            \brief Sets the option type (call or put).

            \param ot The option type
        */
        void setOptionType(Option::Type ot);

        /*! \deprecated Internal: do not use.
                        Deprecated in version 1.40.
                        This method will be moved in the private section
        */
        [[deprecated("Internal: do not use")]]
        Real cumD1(Real strike) const;    // N(d1) or N(-d1)

        /*! \deprecated Internal: do not use.
                        Deprecated in version 1.40.
                        This method will be moved in the private section
        */
        [[deprecated("Internal: do not use")]]
        Real cumD2(Real strike) const;    // N(d2) or N(-d2)

        /*! \deprecated Internal: do not use.
                        Deprecated in version 1.40.
                        This method will be moved in the private section
        */
        [[deprecated("Internal: do not use")]]
        Real nD1(Real strike) const;      // n(d1)

        /*! \deprecated Internal: do not use.
                        Deprecated in version 1.40.
                        This method will be moved in the private section
        */
        [[deprecated("Internal: do not use")]]
        Real nD2(Real strike) const;      // n(d2)

      private:
        // alternative delta type
        Real strikeFromDelta(Real delta, DeltaVolQuote::DeltaType dt) const;

        DeltaVolQuote::DeltaType dt_;
        Option::Type ot_;
        DiscountFactor dDiscount_, fDiscount_;
        Real stdDev_, spot_, forward_;
        Integer phi_;
        Real fExpPos_,fExpNeg_;
    };


    /*! \deprecated Obsolete: do not use.
                    Deprecated in version 1.40.
    */
    class [[deprecated("Obsolete: do not use")]] BlackDeltaPremiumAdjustedSolverClass {
      public:
        BlackDeltaPremiumAdjustedSolverClass(
                        Option::Type ot,
                        DeltaVolQuote::DeltaType dt,
                        Real spot,
                        DiscountFactor dDiscount,   // domestic discount
                        DiscountFactor fDiscount,   // foreign  discount
                        Real stdDev,
                        Real delta);

        Real operator()(Real strike) const;

      private:
        BlackDeltaCalculator bdc_;
        Real delta_;
    };


    /*! \deprecated Obsolete: do not use.
                    Deprecated in version 1.40.
    */
    class [[deprecated("Obsolete: do not use")]] BlackDeltaPremiumAdjustedMaxSt
