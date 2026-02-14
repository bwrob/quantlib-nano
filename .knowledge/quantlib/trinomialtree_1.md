 Real TrinomialTree::Branching::probability(Size index,
                                                      Size branch) const {
        return probs_[branch][index];
    }

    inline Size TrinomialTree::Branching::size() const {
        return jMax_ - jMin_ + 1;
    }

    inline Integer TrinomialTree::Branching::jMin() const {
        return jMin_;
    }

    inline Integer TrinomialTree::Branching::jMax() const {
        return jMax_;
    }

    inline void TrinomialTree::Branching::add(Integer k,
                                              Real p1, Real p2, Real p3) {
        // store
        k_.push_back(k);
        probs_[0].push_back(p1);
        probs_[1].push_back(p2);
        probs_[2].push_back(p3);
        // maintain invariants
        kMin_ = std::min(kMin_, k);
        jMin_ = kMin_ - 1;
        kMax_ = std::max(kMax_, k);
        jMax_ = kMax_ + 1;
    }

}


#endif