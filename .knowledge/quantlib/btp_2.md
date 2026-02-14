  inline const std::vector<Time>& RendistatoCalculator::durations() const {
        calculate();
        return durations_;
    }

    inline const std::vector<Time>& RendistatoCalculator::swapLengths() const {
        return swapLengths_;
    }

    inline const std::vector<Rate>& RendistatoCalculator::swapRates() const {
        calculate();
        return swapRates_;
    }

    inline const std::vector<Rate>& RendistatoCalculator::swapYields() const {
        calculate();
        return swapBondYields_;
    }

    inline const std::vector<Time>& RendistatoCalculator::swapDurations() const {
        calculate();
        return swapBondDurations_;
    }

    inline ext::shared_ptr<VanillaSwap>
    RendistatoCalculator::equivalentSwap() const {
        calculate();
        return swaps_[equivalentSwapIndex_];
    }

    inline Rate RendistatoCalculator::equivalentSwapRate() const {
        calculate();
        return swapRates_[equivalentSwapIndex_];
    }

    inline Rate RendistatoCalculator::equivalentSwapYield() const {
        calculate();
        return swapBondYields_[equivalentSwapIndex_];
    }

    inline Time RendistatoCalculator::equivalentSwapDuration() const {
        calculate();
        return swapBondDurations_[equivalentSwapIndex_];
    }

    inline Time RendistatoCalculator::equivalentSwapLength() const {
        calculate();
        return swapLengths_[equivalentSwapIndex_];
    }

    inline Spread RendistatoCalculator::equivalentSwapSpread() const {
        return yield() - equivalentSwapRate();
    }

    inline Real RendistatoEquivalentSwapLengthQuote::value() const {
        return r_->equivalentSwapLength();
    }

    inline Real RendistatoEquivalentSwapSpreadQuote::value() const {
        return r_->equivalentSwapSpread();
    }

}

#endif