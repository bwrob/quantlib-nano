tr<ZeroInflationIndex>& CPISwap::fixedIndex() const { return fixedIndex_; }
    inline CPI::InterpolationType CPISwap::observationInterpolation() const { return observationInterpolation_; }
    inline Real CPISwap::inflationNominal() const { return inflationNominal_; }

    inline const Leg& CPISwap::cpiLeg() const {//inflation indexed
        return legs_[0];
    }

    inline const Leg& CPISwap::floatLeg() const {
        return legs_[1];
    }

}

#endif
