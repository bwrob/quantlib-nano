n() const;
        mutable ext::shared_ptr<NoArbSabrInterpolation> noArbSabrInterpolation_;

        //! Market data
        const Handle<Quote> forward_;
        const Handle<Quote> atmVolatility_;
        std::vector<Handle<Quote> > volHandles_;
        mutable std::vector<Rate> strikes_;
        //! Only strikes corresponding to valid market data
        mutable std::vector<Rate> actualStrikes_;
        bool hasFloatingStrikes_;

        mutable Real forwardValue_;
        mutable std::vector<Volatility> vols_;
        //! Sabr parameters
        Real alpha_, beta_, nu_, rho_;
        //! Sabr interpolation settings
        bool isAlphaFixed_, isBetaFixed_, isNuFixed_, isRhoFixed_;
        bool vegaWeighted_;
        const ext::shared_ptr<EndCriteria> endCriteria_;
        const ext::shared_ptr<OptimizationMethod> method_;
    };

    inline void NoArbSabrInterpolatedSmileSection::update() {
        LazyObject::update();
        SmileSection::update();
    }

    inline Real NoArbSabrInterpolatedSmileSection::volatilityImpl(Rate strike) const {
        calculate();
        return (*noArbSabrInterpolation_)(strike, true);
    }

    inline Real NoArbSabrInterpolatedSmileSection::alpha() const {
        calculate();
        return noArbSabrInterpolation_->alpha();
    }

    inline Real NoArbSabrInterpolatedSmileSection::beta() const {
        calculate();
        return noArbSabrInterpolation_->beta();
    }

    inline Real NoArbSabrInterpolatedSmileSection::nu() const {
        calculate();
        return noArbSabrInterpolation_->nu();
    }

    inline Real NoArbSabrInterpolatedSmileSection::rho() const {
        calculate();
        return noArbSabrInterpolation_->rho();
    }

    inline Real NoArbSabrInterpolatedSmileSection::rmsError() const {
        calculate();
        return noArbSabrInterpolation_->rmsError();
    }

    inline Real NoArbSabrInterpolatedSmileSection::maxError() const {
        calculate();
        return noArbSabrInterpolation_->maxError();
    }

    inline EndCriteria::Type NoArbSabrInterpolatedSmileSection::endCriteria() const {
        calculate();
        return noArbSabrInterpolation_->endCriteria();
    }

    inline Real NoArbSabrInterpolatedSmileSection::minStrike() const {
        calculate();
        return actualStrikes_.front();

    }

    inline Real NoArbSabrInterpolatedSmileSection::maxStrike() const {
        calculate();
        return actualStrikes_.back();
    }

    inline Real NoArbSabrInterpolatedSmileSection::atmLevel() const {
        calculate();
        return forwardValue_;
    }


}

#endif
