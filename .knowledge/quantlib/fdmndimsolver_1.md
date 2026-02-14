m()[i]);
        }

        for (const auto& iter : *solverDesc.mesher->layout()) {
            initialValues_[iter.index()] = solverDesc_.calculator
                                ->avgInnerValue(iter, solverDesc.maturity);

            const std::vector<Size>& c = iter.coordinates();
            for (Size i=0; i < N; ++i) {
                if ((std::accumulate(c.begin(), c.end(), 0UL) - c[i]) == 0U) {
                    x_[i].push_back(solverDesc.mesher->location(iter, i));
                }
            }
        }

        f_ = ext::shared_ptr<data_table>(new data_table(x_));
    }


    template <Size N> inline
    void FdmNdimSolver<N>::performCalculations() const {
        Array rhs(initialValues_.size());
        std::copy(initialValues_.begin(), initialValues_.end(), rhs.begin());

        FdmBackwardSolver(op_, solverDesc_.bcSet, conditions_, schemeDesc_)
                 .rollback(rhs, solverDesc_.maturity, 0.0,
                           solverDesc_.timeSteps, solverDesc_.dampingSteps);

        for (const auto& iter : *solverDesc_.mesher->layout()) {
            setValue(*f_, iter.coordinates(), rhs[iter.index()]);
        }

        interp_ = ext::shared_ptr<MultiCubicSpline<N> >(
            new MultiCubicSpline<N>(x_, *f_, extrapolation_));
    }


    template <Size N> inline
    Real FdmNdimSolver<N>::thetaAt(const std::vector<Real>& x) const {
        if (conditions_->stoppingTimes().front() == 0.0)
            return Null<Real>();

        calculate();
        const Array& rhs = thetaCondition_->getValues();

        data_table f(x_);

        for (const auto& iter : *solverDesc_.mesher->layout()) {
            setValue(f, iter.coordinates(), rhs[iter.index()]);
        }

        return (MultiCubicSpline<N>(x_, f)(x)
                        - interpolateAt(x)) / thetaCondition_->getTime();
    }

    template <Size N> inline
    Real FdmNdimSolver<N>::interpolateAt(const std::vector<Real>& x) const {
        calculate();

        return (*interp_)(x);
    }

    template <Size N> inline
    void FdmNdimSolver<N>::setValue(data_table& f,
                                    const std::vector<Size>& x, Real value) {
        FdmNdimSolver<N-1>::setValue(f[x[x.size()-N]], x, value);
    }

    template <> inline
    void FdmNdimSolver<1>::setValue(data_table& f,
                                    const std::vector<Size>& x, Real value) {
        f[x.back()] = value;
    }
}

#endif
