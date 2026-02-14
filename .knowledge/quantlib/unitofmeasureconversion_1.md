sure& UnitOfMeasureConversion::target() const {
        return data_->target;
    }

    inline Real UnitOfMeasureConversion::conversionFactor() const {
        return data_->conversionFactor;
    }

    inline UnitOfMeasureConversion::Type UnitOfMeasureConversion::type() const {
        return data_->type;
    }

    inline const std::string& UnitOfMeasureConversion::code() const {
        return data_->code;
    }

}

#endif
