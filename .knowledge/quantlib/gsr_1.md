hould be identical to
    // the fixing dates of the helpers (except for the last one where
    // we do not need a step). Also note that the endcritera reflect
    // only the status of the last calibration when using this method.
    void calibrateVolatilitiesIterative(
        const std::vector<ext::shared_ptr<BlackCalibrationHelper> > &helpers,
        OptimizationMethod &method, const EndCriteria &endCriteria,
        const Constraint &constraint = Constraint(),
        const std::vector<Real> &weights = std::vector<Real>()) {

        for (Size i = 0; i < helpers.size(); i++) {
            std::vector<ext::shared_ptr<CalibrationHelper> > h(1, helpers[i]);
            calibrate(h, method, endCriteria, constraint, weights,
                      MoveVolatility(i));
        }
    }

    // With fixed volatility calibrate the reversions one by one
    // to the given helpers. In this case the step dates must be chosen
    // according to the maturities of the calibration instruments.
    void calibrateReversionsIterative(
        const std::vector<ext::shared_ptr<BlackCalibrationHelper> > &helpers,
        OptimizationMethod &method, const EndCriteria &endCriteria,
        const Constraint &constraint = Constraint(),
        const std::vector<Real> &weights = std::vector<Real>()) {

        for (Size i = 0; i < helpers.size(); i++) {
            std::vector<ext::shared_ptr<CalibrationHelper> > h(1, helpers[i]);
            calibrate(h, method, endCriteria, constraint, weights,
                      MoveReversion(i));
        }
    }

  protected:
    Real numeraireImpl(Time t, Real y, const Handle<YieldTermStructure>& yts) const override;

    Real zerobondImpl(Time T, Time t, Real y, const Handle<YieldTermStructure>& yts) const override;

    void generateArguments() override {
        ext::static_pointer_cast<GsrProcess>(stateProcess_)->flushCache();
        ext::static_pointer_cast<GsrProcess>(stateProcess_)->setVols(sigma_.params());
        ext::static_pointer_cast<GsrProcess>(stateProcess_)->setReversions(reversion_.params());
        notifyObservers();
    }

    void update() override;

    void performCalculations() const override {
        Gaussian1dModel::performCalculations();
        updateTimes();
    }

  private:
    void updateTimes() const;
    void updateVolatility();
    void updateReversion();

    void initialize(Real);

    Parameter &reversion_, &sigma_;

    std::vector<Handle<Quote> > volatilities_;
    std::vector<Handle<Quote> > reversions_;
    std::vector<Date> volstepdates_; // this is shared between vols,
                                     // adjusters and reverisons in
                                     // case of piecewise reversions
    mutable std::vector<Time> volsteptimes_;
    mutable Array volsteptimesArray_; // FIXME this is redundant (just a copy of
                                      // volsteptimes_)

    struct VolatilityObserver : public Observer {
        explicit VolatilityObserver(Gsr *p) : p_(p) {}
        void update() override { p_->updateVolatility(); }
        Gsr *p_;
    };
    struct ReversionObserver : public Observer {
        explicit ReversionObserver(Gsr *p) : p_(p) {}
        void update() override { p_->updateReversion(); }
        Gsr *p_;
    };

    ext::shared_ptr<VolatilityObserver> volatilityObserver_;
    ext::shared_ptr<ReversionObserver> reversionObserver_;
};

inline Real Gsr::numeraireTime() const {
    return ext::dynamic_pointer_cast<GsrProcess>(stateProcess_)
        ->getForwardMeasureTime();
}

inline void Gsr::numeraireTime(const Real T) {
    ext::dynamic_pointer_cast<GsrProcess>(stateProcess_)
        ->setForwardMeasureTime(T);
}
}

#endif
