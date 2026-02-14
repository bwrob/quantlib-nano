Array startArray(localisation_+1-dataAdjust);
            for (Size j = 0; j < startArray.size()-1; ++j)
                startArray[j] = ts_->data_[initialDataPt+j];

            // here we are extending the interpolation a point at a
            // time... but the local interpolator can make an
            // approximation for the final localisation period.
            // e.g. if the localisation is 2, then the first section
            // of the curve will be solved using the first 2
            // instruments... with the local interpolator making
            // suitable boundary conditions.
            ts_->interpolation_ =
                ts_->interpolator_.localInterpolate(
                                              ts_->times_.begin(),
                                              ts_->times_.begin()+(iInst + 2),
                                              ts_->data_.begin(),
                                              localisation_,
                                              ts_->interpolation_,
                                              nInsts+1);

            if (iInst >= localisation_) {
                startArray[localisation_-dataAdjust] =
                    Traits::guess(iInst, ts_, false, 0); // ?
            } else {
                startArray[localisation_-dataAdjust] = ts_->data_[0];
            }

            SimpleCostFunction currentCost([&](const Array& x) {
                for (Size i = 0; i < x.size(); ++i) {
                    Traits::updateGuess(ts_->data_, x[i], initialDataPt + i);
                }
                ts_->interpolation_.update();

                Array penalties(localisation_);
                auto helpersEnd = ts_->instruments_.begin() + (iInst + 1);
                std::transform(helpersEnd - localisation_, helpersEnd,
                               penalties.begin(),
                               [](const auto& helper) { return helper->quoteError(); });
                return penalties;
            });

            Problem toSolve(currentCost, solverConstraint, startArray);

            EndCriteria::Type endType = solver.minimize(toSolve, endCriteria);

            // check the end criteria
            QL_REQUIRE(EndCriteria::succeeded(endType),
                       "Unable to strip yieldcurve to required accuracy: " << endType);
            ++iInst;
        } while ( iInst < nInsts );
        validCurve_ = true;
    }

    QL_DEPRECATED_DISABLE_WARNING

    template <class Curve>
    Real PenaltyFunction<Curve>::value(const Array& x) const {
        Size i = initialIndex_;
        Array::const_iterator guessIt = x.begin();
        while (guessIt != x.end()) {
            Traits::updateGuess(curve_->data_, *guessIt, i);
            ++guessIt;
            ++i;
        }

        curve_->interpolation_.update();

        Real penalty = 0.0;
        helper_iterator instIt = rateHelpersStart_;
        while (instIt != rateHelpersEnd_) {
            Real quoteError = (*instIt)->quoteError();
            penalty += std::fabs(quoteError);
            ++instIt;
        }
        return penalty;
    }

    template <class Curve>
    Array PenaltyFunction<Curve>::values(const Array& x) const {
        Array::const_iterator guessIt = x.begin();
        Size i = initialIndex_;
        while (guessIt != x.end()) {
            Traits::updateGuess(curve_->data_, *guessIt, i);
            ++guessIt;
            ++i;
        }

        curve_->interpolation_.update();

        Array penalties(localisation_);
        helper_iterator instIt = rateHelpersStart_;
        Array::iterator penIt = penalties.begin();
        while (instIt != rateHelpersEnd_) {
            Real quoteError = (*instIt)->quoteError();
            *penIt = std::fabs(quoteError);
            ++instIt;
            ++penIt;
        }
        return penalties;
    }

    QL_DEPRECATED_ENABLE_WARNING

}

#endif
