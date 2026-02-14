le std::vector<Time> actualOptionTimes_;
        Date evaluationDate_;

        std::vector<Handle<Quote> > volHandles_;
        mutable std::vector<Volatility> vols_;
        mutable std::vector<Volatility> actualVols_;

        mutable std::vector<bool> inclusionInInterpolation_;

        ext::shared_ptr<AbcdInterpolation> interpolation_;
    };

    // inline

    inline Date AbcdAtmVolCurve::maxDate() const {
        calculate();
        return optionDateFromTenor(optionTenors_.back());
    }

    inline Real AbcdAtmVolCurve::minStrike() const {
        return QL_MIN_REAL;
    }

    inline Real AbcdAtmVolCurve::maxStrike() const {
        return QL_MAX_REAL;
    }

    inline Real AbcdAtmVolCurve::atmVarianceImpl(Time t) const {
        Volatility vol = atmVolImpl(t);
        return vol*vol*t;
    }

    inline Volatility AbcdAtmVolCurve::atmVolImpl(Time t) const {
        calculate();
        return k(t) * (*interpolation_)(t, true);
    }

    inline const std::vector<Period>& AbcdAtmVolCurve::optionTenors() const {
         return optionTenors_;
    }

    inline const std::vector<Period>& AbcdAtmVolCurve::optionTenorsInInterpolation() const {
        return actualOptionTenors_;
    }

    inline
    const std::vector<Date>& AbcdAtmVolCurve::optionDates() const {
        return optionDates_;
    }

    inline
    const std::vector<Time>& AbcdAtmVolCurve::optionTimes() const {
        return optionTimes_;
    }

    inline
    std::vector<Real> AbcdAtmVolCurve::k() const {
        return interpolation_->k();
    }

    inline
    Real AbcdAtmVolCurve::k(Time t) const {
        return interpolation_->k(t,actualOptionTimes_.begin(),actualOptionTimes_.end());
    }

    inline Real AbcdAtmVolCurve::a() const {
        return interpolation_->a();
    }

    inline Real AbcdAtmVolCurve::b() const {
        return interpolation_->b();
    }

    inline Real AbcdAtmVolCurve::c() const {
        return interpolation_->c();
    }

    inline Real AbcdAtmVolCurve::d() const {
        return interpolation_->d();
    }

    inline Real AbcdAtmVolCurve::rmsError() const {
        return interpolation_->rmsError();
    }
    inline Real AbcdAtmVolCurve::maxError() const {
        return interpolation_->maxError();
    }

    inline EndCriteria::Type AbcdAtmVolCurve::endCriteria() const { 
        return interpolation_->endCriteria();
    }
}

#endif