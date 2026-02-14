eCouponPricer>&);

    // inline

    inline Real BlackIborCouponPricer::swapletPrice() const {
        // past or future fixing is managed in InterestRateIndex::fixing()
        QL_REQUIRE(discount_ != Null<Rate>(), "no forecast curve provided");
        return swapletRate() * accrualPeriod_ * discount_;
    }

    inline Rate BlackIborCouponPricer::swapletRate() const {
        return gearing_ * adjustedFixing() + spread_;
    }

    inline Real BlackIborCouponPricer::capletPrice(Rate effectiveCap) const {
        QL_REQUIRE(discount_ != Null<Rate>(), "no forecast curve provided");
        return capletRate(effectiveCap) * accrualPeriod_ * discount_;
    }

    inline Rate BlackIborCouponPricer::capletRate(Rate effectiveCap) const {
        return gearing_ * optionletRate(Option::Call, effectiveCap);
    }

    inline
    Real BlackIborCouponPricer::floorletPrice(Rate effectiveFloor) const {
        QL_REQUIRE(discount_ != Null<Rate>(), "no forecast curve provided");
        return floorletRate(effectiveFloor) * accrualPeriod_ * discount_;
    }

    inline
    Rate BlackIborCouponPricer::floorletRate(Rate effectiveFloor) const {
        return gearing_ * optionletRate(Option::Put, effectiveFloor);
    }

}

#endif
