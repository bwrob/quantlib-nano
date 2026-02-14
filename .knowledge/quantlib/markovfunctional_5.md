(),
            Real y = 0.0,
            bool zeroFixingDays = false,
            ext::shared_ptr<IborIndex> iborIdx = ext::shared_ptr<IborIndex>()) const;

        Real
        swapRateInternal(const Date& fixing,
                         const Period& tenor,
                         const Date& referenceDate = Date(),
                         Real y = 0.0,
                         bool zeroFixingDays = false,
                         ext::shared_ptr<SwapIndex> swapIdx = ext::shared_ptr<SwapIndex>()) const;

        Real swapAnnuityInternal(
            const Date& fixing,
            const Period& tenor,
            const Date& referenceDate = Date(),
            Real y = 0.0,
            bool zeroFixingDays = false,
            ext::shared_ptr<SwapIndex> swapIdx = ext::shared_ptr<SwapIndex>()) const;

        Real capletPriceInternal(
            const Option::Type& type,
            const Date& expiry,
            Rate strike,
            const Date& referenceDate = Date(),
            Real y = 0.0,
            bool zeroFixingDays = false,
            ext::shared_ptr<IborIndex> iborIdx = ext::shared_ptr<IborIndex>()) const;

        Real swaptionPriceInternal(
            const Option::Type& type,
            const Date& expiry,
            const Period& tenor,
            Rate strike,
            const Date& referenceDate = Date(),
            Real y = 0.0,
            bool zeroFixingDays = false,
            const ext::shared_ptr<SwapIndex>& swapIdx = ext::shared_ptr<SwapIndex>()) const;

        class ZeroHelper {
          public:
            ZeroHelper(const MarkovFunctional *model, const Date &expiry,
                       const CalibrationPoint &p, const Real marketPrice)
                : model_(model), marketPrice_(marketPrice), expiry_(expiry),
                  p_(p) {}
            Real operator()(Real strike) const {
                Real modelPrice = model_->marketDigitalPrice(
                    expiry_, p_, Option::Call, strike);
                return modelPrice - marketPrice_;
            };
            const MarkovFunctional *model_;
            const Real marketPrice_;
            const Date &expiry_;
            const CalibrationPoint &p_;
        };

        ModelSettings modelSettings_;
        mutable ModelOutputs modelOutputs_;

        const bool capletCalibrated_;

        ext::shared_ptr<Matrix> discreteNumeraire_;
        // vector of interpolated numeraires in y direction for all calibration
        // times
        std::vector<ext::shared_ptr<Interpolation> > numeraire_;

        Parameter reversion_;
        Parameter &sigma_;

        std::vector<Date> volstepdates_;
        mutable std::vector<Time> volsteptimes_;
        mutable Array volsteptimesArray_; // FIXME this is redundant (just a copy of
                                  // volsteptimes_)
        std::vector<Real> volatilities_;

        Date numeraireDate_;
        mutable Time numeraireTime_;

        Handle<SwaptionVolatilityStructure> swaptionVol_;
        Handle<OptionletVolatilityStructure> capletVol_;

        std::vector<Date> swaptionExpiries_, capletExpiries_;
        std::vector<Period> swaptionTenors_;
        ext::shared_ptr<SwapIndex> swapIndexBase_;
        ext::shared_ptr<IborIndex> iborIndex_;

        mutable std::map<Date, CalibrationPoint> calibrationPoints_;
        mutable std::vector<Real> times_;
        Array y_;

        Array normalIntegralX_;
        Array normalIntegralW_;

        mutable std::vector<std::pair<Size,Size> > arbitrageIndices_;
        std::vector<std::pair<Size,Size> > forcedArbitrageIndices_;
    };

    std::ostream &operator<<(std::ostream &out,
                             const MarkovFunctional::ModelOutputs &m);
}

#endif
