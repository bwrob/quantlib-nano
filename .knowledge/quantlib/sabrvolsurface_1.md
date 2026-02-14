ce::referenceDate() const {
        return atmCurve_->referenceDate();
    }

    inline Calendar SabrVolSurface::calendar() const {
        return atmCurve_->calendar();
    }

    inline Natural SabrVolSurface::settlementDays() const {
        return atmCurve_->settlementDays();
    }

    inline Real SabrVolSurface::minStrike() const {
        return QL_MIN_REAL;
    }

    inline Real SabrVolSurface::maxStrike() const {
        return QL_MAX_REAL;
    }

    inline const Handle<BlackAtmVolCurve>& SabrVolSurface::atmCurve() const {
        return atmCurve_;
    }

    inline std::vector<Volatility>
    SabrVolSurface::volatilitySpreads(const Period& p) const {
        return volatilitySpreads(optionDateFromTenor(p));
    }
}

#endif