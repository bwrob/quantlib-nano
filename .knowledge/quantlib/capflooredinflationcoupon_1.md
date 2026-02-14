refPeriodEnd),
          isFloored_(false), isCapped_(false) {
            setCommon(cap, floor);
        }

        //! \name augmented Coupon interface
        //@{
        //! swap(let) rate
        Rate rate() const override;
        //! cap
        Rate cap() const;
        //! floor
        Rate floor() const;
        //! effective cap of fixing
        Rate effectiveCap() const;
        //! effective floor of fixing
        Rate effectiveFloor() const;
        //@}

        //! \name Observer interface
        //@{
        void update() override;
        //@}

        //! \name Visitability
        //@{
        void accept(AcyclicVisitor& v) override;
        //@}

        //! this returns the expected rate before cap and floor are applied
        Rate underlyingRate() const;

        bool isCapped() const { return isCapped_; }
        bool isFloored() const { return isFloored_; }

        void setPricer(const ext::shared_ptr<YoYInflationCouponPricer>&);

      protected:
        // data, we only use underlying_ if it was constructed that way,
        // generally we use the shared_ptr conversion to boolean to test
        ext::shared_ptr<YoYInflationCoupon> underlying_;
        bool isFloored_, isCapped_;
        Rate cap_, floor_;
      private:
        void setCommon(Rate cap, Rate floor);
    };

}

#endif
