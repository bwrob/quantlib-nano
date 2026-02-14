   inline bool
    Schedule::hasTerminationDateBusinessDayConvention() const {
        return static_cast<bool>(terminationDateConvention_);
    }

    inline BusinessDayConvention
    Schedule::terminationDateBusinessDayConvention() const {
        QL_REQUIRE(hasTerminationDateBusinessDayConvention(),
                   "full interface (termination date bdc) not available");
        return *terminationDateConvention_;  // NOLINT(bugprone-unchecked-optional-access)
    }

    inline bool Schedule::hasRule() const {
        return static_cast<bool>(rule_);
    }

    inline DateGeneration::Rule Schedule::rule() const {
        QL_REQUIRE(hasRule(), "full interface (rule) not available");
        return *rule_;  // NOLINT(bugprone-unchecked-optional-access)
    }

    inline bool Schedule::hasEndOfMonth() const {
        return static_cast<bool>(endOfMonth_);
    }

    inline bool Schedule::endOfMonth() const {
        QL_REQUIRE(hasEndOfMonth(),
                   "full interface (end of month) not available");
        return *endOfMonth_;  // NOLINT(bugprone-unchecked-optional-access)
    }

}

#endif