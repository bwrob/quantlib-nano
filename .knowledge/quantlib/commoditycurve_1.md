t;
    };


    // inline definitions

    inline bool operator==(const CommodityCurve& c1, const CommodityCurve& c2) {
        return c1.name() == c2.name();
    }

    inline const CommodityType& CommodityCurve::commodityType() const {
        return commodityType_;
    }

    inline const UnitOfMeasure& CommodityCurve::unitOfMeasure() const {
        return unitOfMeasure_;
    }

    inline const Currency& CommodityCurve::currency() const {
        return currency_;
    }

    inline const std::string& CommodityCurve::name() const {
        return name_;
    }

    inline Date CommodityCurve::maxDate() const {
        return dates_.back();
    }

    inline const std::vector<Time>& CommodityCurve::times() const {
        return times_;
    }

    inline const std::vector<Date>& CommodityCurve::dates() const {
        return dates_;
    }

    inline const std::vector<Real>& CommodityCurve::prices() const {
        return data_;
    }

    inline bool CommodityCurve::empty() const {
        return dates_.empty();
    }

    inline const ext::shared_ptr<CommodityCurve>&
    CommodityCurve::basisOfCurve() const {
        return basisOfCurve_;
    }

    inline std::vector<std::pair<Date,Real> > CommodityCurve::nodes() const {
        std::vector<std::pair<Date,Real> > results(dates_.size());
        for (Size i = 0; i < dates_.size(); ++i)
            results[i] = std::make_pair(dates_[i], data_[i]);
        return results;
    }

    inline Real CommodityCurve::basisOfPrice(const Date& d) const {
        Time t = timeFromReference(d);
        return basisOfPriceImpl(t);
    }

    // gets a price that can include an arbitrary number of basis curves
    inline Real CommodityCurve::price(
                const Date& d,
                const ext::shared_ptr<ExchangeContracts>& exchangeContracts,
                Integer nearbyOffset) const {
        Date date = nearbyOffset > 0 ?
            underlyingPriceDate(d, exchangeContracts, nearbyOffset) : d;
        Time t = timeFromReference(date);
        Real priceValue = 0;
        try {
            priceValue = priceImpl(t);
        } catch (const std::exception& e) {
            QL_FAIL("error retrieving price for curve [" << name() << "]: "
                    << e.what());
        }
        return priceValue + basisOfPriceImpl(t);
    }

    // get the date for the underlying price, in the case of nearby
    // curves, rolls on the underlying contract expiry
    inline Date CommodityCurve::underlyingPriceDate(
                const Date& date,
                const ext::shared_ptr<ExchangeContracts>& exchangeContracts,
                Integer nearbyOffset) const {
        QL_REQUIRE(nearbyOffset > 0, "nearby offset must be > 0");
        auto ic =
            exchangeContracts->lower_bound(date);
        if (ic != exchangeContracts->end()) {
            for (int i = 0; i < nearbyOffset-1 && ic!=exchangeContracts->end(); ++i)
                ++ic;
            QL_REQUIRE(ic != exchangeContracts->end(),
                       "not enough nearby contracts available for curve ["
                       << name() << "] for date [" << date << "].");
            return ic->second.underlyingStartDate();
        }
        return date;
    }

    inline Real CommodityCurve::basisOfPriceImpl(Time t) const {
        if (basisOfCurve_ != nullptr) {
            Real basisCurvePriceValue = 0;
            try {
                basisCurvePriceValue =
                    basisOfCurve_->priceImpl(t)
                    * basisOfCurveUomConversionFactor_;
            } catch (const std::exception& e) {
                QL_FAIL("error retrieving price for curve [" << name() <<
                        "]: " << e.what());
            }
            return basisCurvePriceValue + basisOfCurve_->basisOfPriceImpl(t);
        }
        return 0;
    }

    inline Real CommodityCurve::priceImpl(Time t) const {
        return interpolation_(t, true);
    }

}


#endif