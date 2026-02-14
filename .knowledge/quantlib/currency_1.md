m& operator<<(std::ostream&,
                             const Currency&);


    // inline definitions

    inline void Currency::checkNonEmpty() const {
        QL_REQUIRE(data_, "no currency data provided");
    }

    inline const std::string& Currency::name() const {
        checkNonEmpty();
        return data_->name;
    }

    inline const std::string& Currency::code() const {
        checkNonEmpty();
        return data_->code;
    }

    inline Integer Currency::numericCode() const {
        checkNonEmpty();
        return data_->numeric;
    }

    inline const std::string& Currency::symbol() const {
        checkNonEmpty();
        return data_->symbol;
    }

    inline const std::string& Currency::fractionSymbol() const {
        checkNonEmpty();
        return data_->fractionSymbol;
    }

    inline Integer Currency::fractionsPerUnit() const {
        checkNonEmpty();
        return data_->fractionsPerUnit;
    }

    inline const Rounding& Currency::rounding() const {
        checkNonEmpty();
        return data_->rounding;
    }

    inline bool Currency::empty() const {
        return !data_;
    }

    inline const Currency& Currency::triangulationCurrency() const {
        checkNonEmpty();
        return data_->triangulated;
    }

    inline const std::set<std::string>& Currency::minorUnitCodes() const {
        checkNonEmpty();
        return data_->minorUnitCodes;
    }

    inline bool operator==(const Currency& c1, const Currency& c2) {
        return (c1.empty() && c2.empty()) ||
               (!c1.empty() && !c2.empty() && c1.name() == c2.name());
    }

    inline bool operator!=(const Currency& c1, const Currency& c2) {
        return !(c1 == c2);
    }

}


#endif
