inline Real CommodityIndex::lotQuantity() const {
        return lotQuantity_;
    }

    inline const ext::shared_ptr<CommodityCurve>&
    CommodityIndex::forwardCurve() const {
        return forwardCurve_;
    }

    inline Real CommodityIndex::forwardPrice(const Date& date) const {
        try {
            Real forwardPrice =
                forwardCurve_->price(date, exchangeContracts_, nearbyOffset_);
            return forwardPrice * forwardCurveUomConversionFactor_;
        } catch (const std::exception& e) {
            QL_FAIL("error fetching forward price for index " << name_
                    << ": " << e.what());
        }
    }

    inline Date CommodityIndex::lastQuoteDate() const {
        return timeSeries().lastDate();
    }

    inline bool CommodityIndex::empty() const {
        return timeSeries().empty();
    }

    inline bool CommodityIndex::forwardCurveEmpty() const {
        if (forwardCurve_ != nullptr)
            return forwardCurve_->empty();
        return false;
    }

}

#endif