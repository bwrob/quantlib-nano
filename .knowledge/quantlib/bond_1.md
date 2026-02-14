flows, including the redemptions. */
        const Leg& cashflows() const;
        /*! returns just the redemption flows (not interest payments) */
        const Leg& redemptions() const;
        /*! returns the redemption, if only one is defined */
        const ext::shared_ptr<CashFlow>& redemption() const;

        Date startDate() const;
        Date maturityDate() const;
        Date issueDate() const;

        bool isTradable(Date d = Date()) const;
        Date settlementDate(Date d = Date()) const;
        //@}

        //! \name Calculations
        //@{

        //! theoretical clean price
        /*! The default bond settlement is used for calculation.

            \warning the theoretical price calculated from a flat term
                     structure might differ slightly from the price
                     calculated from the corresponding yield by means
                     of the other overload of this function. If the
                     price from a constant yield is desired, it is
                     advisable to use such other overload.
        */
        Real cleanPrice() const;

        //! theoretical dirty price
        /*! The default bond settlement is used for calculation.

            \warning the theoretical price calculated from a flat term
                     structure might differ slightly from the price
                     calculated from the corresponding yield by means
                     of the other overload of this function. If the
                     price from a constant yield is desired, it is
                     advisable to use such other overload.
        */
        Real dirtyPrice() const;

        //! theoretical settlement value
        /*! The default bond settlement date is used for calculation. */
        Real settlementValue() const;

        //! theoretical bond yield
        /*! The default bond settlement and theoretical price are used
            for calculation.
        */
        Rate yield(const DayCounter& dc,
                   Compounding comp,
                   Frequency freq,
                   Real accuracy = 1.0e-8,
                   Size maxEvaluations = 100,
                   Real guess = 0.05,
                   Bond::Price::Type priceType = Bond::Price::Clean) const;

        //! clean price given a yield and settlement date
        /*! The default bond settlement is used if no date is given. */
        Real cleanPrice(Rate yield,
                        const DayCounter& dc,
                        Compounding comp,
                        Frequency freq,
                        Date settlementDate = Date()) const;

        //! dirty price given a yield and settlement date
        /*! The default bond settlement is used if no date is given. */
        Real dirtyPrice(Rate yield,
                        const DayCounter& dc,
                        Compounding comp,
                        Frequency freq,
                        Date settlementDate = Date()) const;

        //! settlement value as a function of the clean price
        /*! The default bond settlement date is used for calculation. */
        Real settlementValue(Real cleanPrice) const;

        //! yield given a price and settlement date
        /*! The default bond settlement is used if no date is given. */
        Rate yield(Bond::Price price,
                   const DayCounter& dc,
                   Compounding comp,
                   Frequency freq,
                   Date settlementDate = Date(),
                   Real accuracy = 1.0e-8,
                   Size maxEvaluations = 100,
                   Real guess = 0.05) const;

        //! accrued amount at a given date
        /*! The default bond settlement is used if no date is given. */
        virtual Real accruedAmount(Date d = Date()) const;
        //@}

        /*! Expected next coupon: depending on (the bond and) the given date
            the coupon can be historic, deterministic or expected in a
            stoch
