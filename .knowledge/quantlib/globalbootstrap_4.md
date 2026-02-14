 quote");
        helper->setTermStructure(const_cast<Curve*>(ts_));
    }

    // setup interpolation
    if (!validCurve_) {
        ts_->interpolation_ = ts_->interpolator_.interpolate(ts_->times_.begin(), ts_->times_.end(),
                                                             ts_->data_.begin());
    }

    // Initial guess. We have guesses for the curve values first (numberPillars),
    // followed by guesses for the additional variables.
    Array additionalGuesses;
    if (additionalVariables_) {
        additionalGuesses = additionalVariables_->initialize(validCurve_);
    }
    Array guess(ts_->times_.size() - 1 + additionalGuesses.size());
    for (Size i = 0; i < ts_->times_.size() - 1; ++i) {
        // just pass zero as the first alive helper, it's not used in the standard QL traits anyway
        // update ts_->data_ since Traits::guess() usually depends on previous values
        Traits::updateGuess(ts_->data_, Traits::guess(i + 1, ts_, validCurve_, 0), i + 1);
        guess[i] = Traits::transformInverse(ts_->data_[i + 1], i + 1, ts_);
    }
    std::copy(additionalGuesses.begin(), additionalGuesses.end(),
              guess.begin() + ts_->times_.size() - 1);
    return guess;
}

template <class Curve>
void GlobalBootstrap<Curve>::setCostFunctionArgument(const Array& x) const {
    // x has the same layout as guess above: the first numberPillars values go into
    // the curve, while the rest are new values for the additional variables.
    for (Size i = 0; i < ts_->times_.size() - 1; ++i) {
        Traits::updateGuess(ts_->data_, Traits::transformDirect(x[i], i + 1, ts_), i + 1);
    }
    ts_->interpolation_.update();
    if (additionalVariables_) {
        additionalVariables_->update(Array(x.begin() + ts_->times_.size() - 1, x.end()));
    }
}

template <class Curve>
Array GlobalBootstrap<Curve>::evaluateCostFunction() const {
    Array additionalErrors;
    if (additionalPenalties_) {
        additionalErrors = additionalPenalties_(ts_->times_, ts_->data_);
    }
    Array result(aliveInstruments_.size() + additionalErrors.size());
    for (Size i = 0; i < aliveInstruments_.size(); ++i)
        result[i] = aliveInstruments_[i]->quoteError() * aliveInstrumentWeights_[i];
    std::copy(additionalErrors.begin(), additionalErrors.end(),
              result.begin() + aliveInstruments_.size());
    return result;
}

template <class Curve>
void GlobalBootstrap<Curve>::calculate() const {

    if (parentBootstrapper_) {
        parentBootstrapper_->runMultiCurveBootstrap();
        return;
    }

    // single curve boostrap

    Array guess = setupCostFunction();

    NoConstraint noConstraint;

    SimpleCostFunction costFunction([this](const Array& x) {
        this->setCostFunctionArgument(x);
        return this->evaluateCostFunction();
    });

    Problem problem(costFunction, noConstraint, guess);
    EndCriteria::Type endType = optimizer_->minimize(problem, *endCriteria_);
    QL_REQUIRE(EndCriteria::succeeded(endType),
               "global bootstrap failed to minimize to required accuracy: " << endType);
    validCurve_ = true;
}

} // namespace QuantLib

#endif