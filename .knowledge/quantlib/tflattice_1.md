   // induction using up and down probabilities on tree on
            // previous conversion probabilities, ie weighted average
            // of previous probabilities.
            newConversionProbability[j] =
                this->pd_*conversionProbability[j] +
                this->pu_*conversionProbability[j+1];

            // Use blended discounting rate
            newSpreadAdjustedRate[j] =
                newConversionProbability[j] * this->riskFreeRate_ +
                (1-newConversionProbability[j])*(this->riskFreeRate_+creditSpread_);

            newValues[j] =
                (this->pd_*values[j]/(1+(spreadAdjustedRate[j]*this->dt_)))
              + (this->pu_*values[j+1]/(1+(spreadAdjustedRate[j+1]*this->dt_)));

        }
    }

    template <class T>
    void TsiveriotisFernandesLattice<T>::rollback(DiscretizedAsset& asset,
                                                  Time to) const {
        partialRollback(asset,to);
        asset.adjustValues();
    }


    template <class T>
    void TsiveriotisFernandesLattice<T>::partialRollback(DiscretizedAsset& asset,
                                                         Time to) const {

        Time from = asset.time();

        if (close(from,to))
            return;

        QL_REQUIRE(from > to,
                   "cannot roll the asset back to" << to
                   << " (it is already at t = " << from << ")");

        auto& convertible = dynamic_cast<DiscretizedConvertible&>(asset);

        auto iFrom = Integer(this->t_.index(from));
        auto iTo = Integer(this->t_.index(to));

        for (Integer i=iFrom-1; i>=iTo; --i) {

            Array newValues(this->size(i));
            Array newSpreadAdjustedRate(this->size(i));
            Array newConversionProbability(this->size(i));

            stepback(i, convertible.values(),
                     convertible.conversionProbability(),
                     convertible.spreadAdjustedRate(), newValues,
                     newConversionProbability,newSpreadAdjustedRate);

            convertible.time() = this->t_[i];
            convertible.values() = newValues;
            convertible.spreadAdjustedRate() = newSpreadAdjustedRate;
            convertible.conversionProbability() = newConversionProbability;

            // skip the very last adjustment
            if (i != iTo)
                convertible.adjustValues();
        }
    }

}

#endif
