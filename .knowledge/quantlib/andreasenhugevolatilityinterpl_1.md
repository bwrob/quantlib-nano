y& previousNPVs) const;

        Size getExerciseTimeIdx(Time t) const;

        Real getCacheValue(
            Real strike, const TimeValueCacheType::const_iterator& f) const;

        Array getPriceSlice(Time t, Option::Type optionType) const;

        Array getLocalVolSlice(Time t, Option::Type optionType) const;

        CalibrationSet calibrationSet_;
        const Handle<Quote> spot_;
        const Handle<YieldTermStructure> rTS_;
        const Handle<YieldTermStructure> qTS_;
        const InterpolationType interpolationType_;
        const CalibrationType calibrationType_;

        const Size nGridPoints_;
        const Real minStrike_, maxStrike_;

        const ext::shared_ptr<OptimizationMethod> optimizationMethod_;
        const EndCriteria endCriteria_;

        std::vector<Real> strikes_;
        std::vector<Date> expiries_;
        mutable std::vector<Time> expiryTimes_, dT_;

        std::vector<std::vector<Size> > calibrationMatrix_;
        mutable Real avgError_, minError_, maxError_;

        mutable ext::shared_ptr<FdmMesherComposite> mesher_;
        mutable Array gridPoints_, gridInFwd_;

        mutable std::vector<SingleStepCalibrationResult> calibrationResults_;

        mutable TimeValueCacheType localVolCache_, priceCache_;
    };

}

#endif
