protected:

        //! Creates the mutable SABRInterpolation
        void createInterpolation() const;
        mutable ext::shared_ptr<SABRInterpolation> sabrInterpolation_;

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

        mutable Date evaluationDate_;
    };

    inline void SabrInterpolatedSmileSection::update() {
        LazyObject::update();
        SmileSection::update();
    }

    inline Real SabrInterpolatedSmileSection::volatilityImpl(Rate strike) const {
        calculate();
        return (*sabrInterpolation_)(strike, true);
    }

    inline Real SabrInterpolatedSmileSection::alpha() const {
        calculate();
        return sabrInterpolation_->alpha();
    }

    inline Real SabrInterpolatedSmileSection::beta() const {
        calculate();
        return sabrInterpolation_->beta();
    }

    inline Real SabrInterpolatedSmileSection::nu() const {
        calculate();
        return sabrInterpolation_->nu();
    }

    inline Real SabrInterpolatedSmileSection::rho() const {
        calculate();
        return sabrInterpolation_->rho();
    }

    inline Real SabrInterpolatedSmileSection::rmsError() const {
        calculate();
        return sabrInterpolation_->rmsError();
    }

    inline Real SabrInterpolatedSmileSection::maxError() const {
        calculate();
        return sabrInterpolation_->maxError();
    }

    inline EndCriteria::Type SabrInterpolatedSmileSection::endCriteria() const {
        calculate();
        return sabrInterpolation_->endCriteria();
    }

    inline Real SabrInterpolatedSmileSection::minStrike() const {
        calculate();
        return actualStrikes_.front();

    }

    inline Real SabrInterpolatedSmileSection::maxStrike() const {
        calculate();
        return actualStrikes_.back();
    }

    inline Real SabrInterpolatedSmileSection::atmLevel() const {
        calculate();
        return forwardValue_;
    }


}

#endif