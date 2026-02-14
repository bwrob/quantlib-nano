    }
        return i->second;
    }

    ext::shared_ptr<StochasticProcess1D> stateProcess_;
    mutable Date evaluationDate_;
    mutable bool enforcesTodaysHistoricFixings_;
};

inline ext::shared_ptr<StochasticProcess1D> Gaussian1dModel::stateProcess() const {

    QL_REQUIRE(stateProcess_ != nullptr, "state process not set");
    return stateProcess_;
}

inline Real
Gaussian1dModel::numeraire(const Time t, const Real y,
                           const Handle<YieldTermStructure> &yts) const {

    return numeraireImpl(t, y, yts);
}

inline Real
Gaussian1dModel::zerobond(const Time T, const Time t, const Real y,
                          const Handle<YieldTermStructure> &yts) const {
    return zerobondImpl(T, t, y, yts);
}

inline Real
Gaussian1dModel::numeraire(const Date &referenceDate, const Real y,
                           const Handle<YieldTermStructure> &yts) const {

    return numeraire(termStructure()->timeFromReference(referenceDate), y, yts);
}

inline Real
Gaussian1dModel::zerobond(const Date &maturity, const Date &referenceDate,
                          const Real y, const Handle<YieldTermStructure> &yts) const {

    return zerobond(termStructure()->timeFromReference(maturity),
                    referenceDate != Date()
                        ? termStructure()->timeFromReference(referenceDate)
                        : 0.0,
                    y, yts);
}
}

#endif
