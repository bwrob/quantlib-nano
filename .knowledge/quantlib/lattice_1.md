 computeStatePrices(i);
        return statePrices_[i];
    }

    template <class Impl>
    inline Real TreeLattice<Impl>::presentValue(DiscretizedAsset& asset) const {
        Size i = t_.index(asset.time());
        return DotProduct(asset.values(), statePrices(i));
    }

    template <class Impl>
    inline void TreeLattice<Impl>::initialize(DiscretizedAsset& asset, Time t) const {
        Size i = t_.index(t);
        asset.time() = t;
        asset.reset(this->impl().size(i));
    }

    template <class Impl>
    inline void TreeLattice<Impl>::rollback(DiscretizedAsset& asset, Time to) const {
        partialRollback(asset,to);
        asset.adjustValues();
    }

    template <class Impl>
    void TreeLattice<Impl>::partialRollback(DiscretizedAsset& asset,
                                            Time to) const {

        Time from = asset.time();

        if (close(from,to))
            return;

        QL_REQUIRE(from > to,
                   "cannot roll the asset back to" << to
                   << " (it is already at t = " << from << ")");

        auto iFrom = Integer(t_.index(from));
        auto iTo = Integer(t_.index(to));

        for (Integer i=iFrom-1; i>=iTo; --i) {
            Array newValues(this->impl().size(i));
            this->impl().stepback(i, asset.values(), newValues);
            asset.time() = t_[i];
            asset.values() = newValues;
            // skip the very last adjustment
            if (i != iTo)
                asset.adjustValues();
        }
    }

    template <class Impl>
    void TreeLattice<Impl>::stepback(Size i, const Array& values,
                                     Array& newValues) const {
        #pragma omp parallel for
        for (long j=0; j<(long)this->impl().size(i); j++) {
            Real value = 0.0;
            for (Size l=0; l<n_; l++) {
                value += this->impl().probability(i,j,l) *
                         values[this->impl().descendant(i,j,l)];
            }
            value *= this->impl().discount(i,j);
            newValues[j] = value;
        }
    }

}


#endif