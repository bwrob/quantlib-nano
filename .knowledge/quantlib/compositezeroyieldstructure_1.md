Function>
    inline void CompositeZeroYieldStructure<BinaryFunction>::update() {
        if (!curve1_.empty() && !curve2_.empty()) {
            YieldTermStructure::update();
            enableExtrapolation(curve1_->allowsExtrapolation() && curve2_->allowsExtrapolation());
        }
        else {
            /* The implementation inherited from YieldTermStructure
            asks for our reference date, which we don't have since
            the original curve is still not set. Therefore, we skip
            over that and just call the base-class behavior. */
            // NOLINTNEXTLINE(bugprone-parent-virtual-call)
            TermStructure::update();
        }
    }

    template <class BinaryFunction>
    inline Rate CompositeZeroYieldStructure<BinaryFunction>::zeroYieldImpl(Time t) const {
        Rate zeroRate1 =
            curve1_->zeroRate(t, comp_, freq_, true);

        InterestRate zeroRate2 =
            curve2_->zeroRate(t, comp_, freq_, true);

        InterestRate compositeRate(f_(zeroRate1, zeroRate2), dayCounter(), comp_, freq_);
        return compositeRate.equivalentRate(Continuous, NoFrequency, t);
    }
}
#endif