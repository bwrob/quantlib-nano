rward())
            type = Option::Call;
        else
            type = Option::Put;
        impliedVol =
            blackFormulaImpliedStdDev(type, strike, model_->forward(),
                                      optionPrice(strike, type, 1.0), 1.0) /
            std::sqrt(exerciseTime());
    } catch (...) {
    }
    return impliedVol;
}

template <typename Evaluation>
Real ZabrSmileSection<Evaluation>::volatilityImpl(Rate strike,
                                                  ZabrLocalVolatility) const {
    return volatilityImpl(strike, ZabrShortMaturityNormal());
}

template <typename Evaluation>
Real ZabrSmileSection<Evaluation>::volatilityImpl(Rate strike,
                                                  ZabrFullFd) const {
    return volatilityImpl(strike, ZabrShortMaturityNormal());
}
}

#endif