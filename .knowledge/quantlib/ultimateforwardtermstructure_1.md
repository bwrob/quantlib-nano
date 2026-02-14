r interface
        //@{
        void update() override;
        //@}
      protected:
        //! returns the UFR extended zero yield rate
        Rate zeroYieldImpl(Time) const override;
        //@}
      private:
        //! applies rounding on zero rate with required compounding
        Rate applyRounding(Rate r, Time t) const;
        //@}

        Handle<YieldTermStructure> originalCurve_;
        Handle<Quote> llfr_;
        Handle<Quote> ufr_;
        Period fsp_;
        Real alpha_;
        ext::optional<Integer> roundingDigits_;
        Compounding compounding_;
        Frequency frequency_;
    };

    // inline definitions

    inline UltimateForwardTermStructure::UltimateForwardTermStructure(
        Handle<YieldTermStructure> h,
        Handle<Quote> lastLiquidForwardRate,
        Handle<Quote> ultimateForwardRate,
        const Period& firstSmoothingPoint,
        Real alpha,
        const ext::optional<Integer>& roundingDigits,
        Compounding compounding,
        Frequency frequency)
    : originalCurve_(std::move(h)), llfr_(std::move(lastLiquidForwardRate)),
      ufr_(std::move(ultimateForwardRate)), fsp_(firstSmoothingPoint), alpha_(alpha),
      roundingDigits_(roundingDigits), compounding_(compounding), frequency_(frequency) {
        QL_REQUIRE(fsp_.length() > 0,
                   "first smoothing point must be a period with positive length");
        if (!originalCurve_.empty())
            enableExtrapolation(originalCurve_->allowsExtrapolation());
        registerWith(originalCurve_);
        registerWith(llfr_);
        registerWith(ufr_);
    }

    inline DayCounter UltimateForwardTermStructure::dayCounter() const {
        return originalCurve_->dayCounter();
    }

    inline Calendar UltimateForwardTermStructure::calendar() const {
        return originalCurve_->calendar();
    }

    inline Natural UltimateForwardTermStructure::settlementDays() const {
        return originalCurve_->settlementDays();
    }

    inline const Date& UltimateForwardTermStructure::referenceDate() const {
        return originalCurve_->referenceDate();
    }

    inline Date UltimateForwardTermStructure::maxDate() const { return Date::maxDate(); }

    inline void UltimateForwardTermStructure::update() {
        if (!originalCurve_.empty()) {
            YieldTermStructure::update();
            enableExtrapolation(originalCurve_->allowsExtrapolation());
        } else {
            /* The implementation inherited from YieldTermStructure
               asks for our reference date, which we don't have since
               the original curve is still not set. Therefore, we skip
               over that and just call the base-class behavior. */
            // NOLINTNEXTLINE(bugprone-parent-virtual-call)
            TermStructure::update();
        }
    }

    inline Rate UltimateForwardTermStructure::applyRounding(Rate r, Time t) const {
        if (!roundingDigits_.has_value()) {
            return r;
        }
        // Input rate is continuously compounded by definition.
        // Hence, in case this is also the selected compounding method for rounding,
        // it is not required to calculate equivalent rates, and rounding
        // may be applied directly.
        Rate equivalentRate = compounding_ == Continuous ?
                                  r :
                                  InterestRate(r, dayCounter(), Continuous, NoFrequency)
                                      .equivalentRate(compounding_, frequency_, t);
        Rate rounded = ClosestRounding(*roundingDigits_)(equivalentRate);
        return compounding_ == Continuous ?
                   rounded :
                   InterestRate(rounded, dayCounter(), compounding_, frequency_)
                       .equivalentRate(Continuous, NoFrequency, t);
    }

    inline Rate UltimateForwardTermStructure::zeroYieldImpl(Time t) const {
        Time cutOffTime = originalCurve_->timeFromReference(referenceDate() + fsp_);
        Time deltaT = t -
