ion_;
    }

    inline Size FlatVol::numberOfRates() const {
        return initialRates_.size();
    }

    inline Size FlatVol::numberOfFactors() const {
        return numberOfFactors_;
    }

    inline Size FlatVol::numberOfSteps() const {
        return numberOfSteps_;
    }

    inline const Matrix& FlatVol::pseudoRoot(Size i) const {
        QL_REQUIRE(i<numberOfSteps_,
                   "the index " << i << " is invalid: it must be less than "
                   "number of steps (" << numberOfSteps_ << ")");
        return pseudoRoots_[i];
    }
}

#endif