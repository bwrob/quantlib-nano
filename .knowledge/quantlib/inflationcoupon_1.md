 definitions


    inline void InflationCoupon::accept(AcyclicVisitor& v) {
        auto* v1 = dynamic_cast<Visitor<InflationCoupon>*>(&v);
        if (v1 != nullptr)
            v1->visit(*this);
        else
            Coupon::accept(v);
    }

    inline ext::shared_ptr<InflationCouponPricer>
    InflationCoupon::pricer() const {
        return pricer_;
    }

}

#endif
