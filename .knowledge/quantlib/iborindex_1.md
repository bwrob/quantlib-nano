lone(const Handle<YieldTermStructure>& h) const override;
    };


    // inline

    inline BusinessDayConvention IborIndex::businessDayConvention() const {
        return convention_;
    }

    inline Handle<YieldTermStructure>
    IborIndex::forwardingTermStructure() const {
        return termStructure_;
    }

    inline Rate IborIndex::forecastFixing(const Date& d1,
                                          const Date& d2,
                                          Time t) const {
        QL_REQUIRE(!termStructure_.empty(),
                   "null term structure set to this instance of " << name());
        DiscountFactor disc1 = termStructure_->discount(d1);
        DiscountFactor disc2 = termStructure_->discount(d2);
        return (disc1/disc2 - 1.0) / t;
    }

}

#endif