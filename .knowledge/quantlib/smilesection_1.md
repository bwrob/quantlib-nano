eturn volatilityImpl(strike);
    }

    inline const Date& SmileSection::referenceDate() const {
        QL_REQUIRE(referenceDate_!=Date(),
                   "referenceDate not available for this instance");
        return referenceDate_;
    }

    inline Real SmileSection::varianceImpl(Rate strike) const {
        Volatility v = volatilityImpl(strike);
        return v*v*exerciseTime();
    }

}

#endif