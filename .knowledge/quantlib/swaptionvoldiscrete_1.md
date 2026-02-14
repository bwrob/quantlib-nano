latilityDiscrete::optionTenors() const {
         return optionTenors_;
    }

    inline const std::vector<Date>&
    SwaptionVolatilityDiscrete::optionDates() const {
        return optionDates_;
    }

    inline const std::vector<Time>&
    SwaptionVolatilityDiscrete::optionTimes() const {
        return optionTimes_;
    }

    inline const std::vector<Period>&
    SwaptionVolatilityDiscrete::swapTenors() const {
     return swapTenors_;
    }

    inline const std::vector<Time>&
    SwaptionVolatilityDiscrete::swapLengths() const {
        return swapLengths_;
    }

    inline Date SwaptionVolatilityDiscrete::optionDateFromTime(Time optionTime) const {
        return Date(static_cast<Date::serial_type>(optionInterpolator_(optionTime)));
    }
}

#endif