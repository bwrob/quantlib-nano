nline bool InflationIndex::revised() const {
        return revised_;
    }

    inline Frequency InflationIndex::frequency() const {
        return frequency_;
    }

    inline Period InflationIndex::availabilityLag() const {
        return availabilityLag_;
    }

    inline Currency InflationIndex::currency() const {
        return currency_;
    }

    inline Handle<ZeroInflationTermStructure>
    ZeroInflationIndex::zeroInflationTermStructure() const {
        return zeroInflation_;
    }

    inline bool YoYInflationIndex::interpolated() const {
        return interpolated_;
    }

    inline bool YoYInflationIndex::ratio() const {
        return ratio_;
    }

    inline ext::shared_ptr<ZeroInflationIndex> YoYInflationIndex::underlyingIndex() const {
        return underlyingIndex_;
    }

    inline Handle<YoYInflationTermStructure>
    YoYInflationIndex::yoyInflationTermStructure() const {
        return yoyInflation_;
    }

}

#endif
