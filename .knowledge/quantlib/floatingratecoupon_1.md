onPricer> pricer() const;
      protected:
        //! convexity adjustment for the given index fixing
        Rate convexityAdjustmentImpl(Rate fixing) const;
        ext::shared_ptr<InterestRateIndex> index_;
        DayCounter dayCounter_;
        Natural fixingDays_;
        Real gearing_;
        Spread spread_;
        bool isInArrears_;
        ext::shared_ptr<FloatingRateCouponPricer> pricer_;
        mutable Real rate_;
    };

    // inline definitions

    inline const ext::shared_ptr<InterestRateIndex>&
    FloatingRateCoupon::index() const {
        return index_;
    }

    inline Rate FloatingRateCoupon::convexityAdjustment() const {
        return convexityAdjustmentImpl(indexFixing());
    }

    inline Rate FloatingRateCoupon::adjustedFixing() const {
        return (rate()-spread())/gearing();
    }

    inline ext::shared_ptr<FloatingRateCouponPricer>
    FloatingRateCoupon::pricer() const {
        return pricer_;
    }

    inline Rate
    FloatingRateCoupon::convexityAdjustmentImpl(Rate fixing) const {
        return (gearing() == 0.0 ? Rate(0.0) : Rate(adjustedFixing()-fixing));
    }

    inline void FloatingRateCoupon::accept(AcyclicVisitor& v) {
        auto* v1 = dynamic_cast<Visitor<FloatingRateCoupon>*>(&v);
        if (v1 != nullptr)
            v1->visit(*this);
        else
            Coupon::accept(v);
    }

}

#endif