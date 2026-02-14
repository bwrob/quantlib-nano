e putPosition = Position::Long,
                      bool isPutITMIncluded = false,
                      Rate putDigitalPayoff = Null<Rate>(),
                      ext::shared_ptr<DigitalReplication> replication = {},
                      bool nakedOption = false);

        //@}
        //! \name Obverver interface
        //@{
        void deepUpdate() override;
        //@}
        //! \name LazyObject interface
        //@{
        void performCalculations() const override;
        //@}
        //! \name Coupon interface
        //@{
        Rate rate() const override;
        Rate convexityAdjustment() const override;
        //@}
        //@}
        //! \name Digital inspectors
        //@{
        Rate callStrike() const;
        Rate putStrike() const;
        Rate callDigitalPayoff() const;
        Rate putDigitalPayoff() const;
        bool hasPut() const { return hasPutStrike_; }
        bool hasCall() const {return hasCallStrike_; }
        bool hasCollar() const {return (hasCallStrike_ && hasPutStrike_); }
        bool isLongPut() const { return (putCsi_==1.); }
        bool isLongCall() const { return (callCsi_==1.); }
        ext::shared_ptr<FloatingRateCoupon> underlying() const { return underlying_; }
        /*! Returns the call option rate
           (multiplied by: nominal*accrualperiod*discount is the NPV of the option)
        */
        Rate callOptionRate() const;
        /*! Returns the put option rate
           (multiplied by: nominal*accrualperiod*discount is the NPV of the option)
        */
        Rate putOptionRate() const;
        //@}
        //! \name Visitability
        //@{
        void accept(AcyclicVisitor&) override;

        void setPricer(const ext::shared_ptr<FloatingRateCouponPricer>& pricer) override {
            if (pricer_ != nullptr)
                unregisterWith(pricer_);
            pricer_ = pricer;
            if (pricer_ != nullptr)
                registerWith(pricer_);
            update();
            underlying_->setPricer(pricer);
        }

        protected:
        //! \name Data members
        //@{
        //!
        ext::shared_ptr<FloatingRateCoupon> underlying_;
        //! strike rate for the the call option
        Rate callStrike_;
        //! strike rate for the the put option
        Rate putStrike_;
        //! multiplicative factor of call payoff
        Real callCsi_ = 0.;
        //! multiplicative factor of put payoff
        Real putCsi_ = 0.;
        //! inclusion flag og the call payoff if the call option ends at-the-money
        bool isCallATMIncluded_;
        //! inclusion flag og the put payoff if the put option ends at-the-money
        bool isPutATMIncluded_;
        //! digital call option type: if true, cash-or-nothing, if false asset-or-nothing
        bool isCallCashOrNothing_ = false;
        //! digital put option type: if true, cash-or-nothing, if false asset-or-nothing
        bool isPutCashOrNothing_ = false;
        //! digital call option payoff rate, if any
        Rate callDigitalPayoff_;
        //! digital put option payoff rate, if any
        Rate putDigitalPayoff_;
        //! the left and right gaps applied in payoff replication for call
        Real callLeftEps_, callRightEps_;
        //! the left and right gaps applied in payoff replication for put
        Real putLeftEps_, putRightEps_;
        //!
        bool hasPutStrike_ = false, hasCallStrike_ = false;
        //! Type of replication
        Replication::Type replicationType_;
        //! underlying excluded from the payoff
        bool nakedOption_;

        //@}
      private:
        Rate callPayoff() const;
        Rate putPayoff() const;

    };

}

#endif
