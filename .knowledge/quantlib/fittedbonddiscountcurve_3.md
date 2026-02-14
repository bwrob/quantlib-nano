tion routine
        ext::shared_ptr<FittingCost> costFunction_;
      private:
        // curve optimization called here- adjust optimization parameters here
        void calculate();
        // array of normalized (duration) weights, one for each bond helper
        Array weights_;
        // array of l2 penalties one for each parameter
        Array l2_;
        // whether or not the weights should be calculated internally
        bool calculateWeights_;
        // total number of iterations used in the optimization routine
        // (possibly including gradient evaluations)
        Integer numberOfIterations_;
        // final value for the minimized cost function
        Real costValue_;
        // error code returned by OptimizationMethod::minimize()
        EndCriteria::Type errorCode_ = EndCriteria::None;
        // optimization method to be used, if none provided use Simplex
        ext::shared_ptr<OptimizationMethod> optimizationMethod_;
        // optimization constraint, if none provided use NoConstraint
        Constraint constraint_;
        // flat extrapolation of instantaneous forward before / after cutoff
        Real minCutoffTime_, maxCutoffTime_;
    };

    // inline

    inline Size FittedBondDiscountCurve::numberOfBonds() const {
        return bondHelpers_.size();
    }

    inline Date FittedBondDiscountCurve::maxDate() const {
        calculate();
        return maxDate_;
    }

    inline const FittedBondDiscountCurve::FittingMethod&
    FittedBondDiscountCurve::fitResults() const {
        calculate();
        return *fittingMethod_;
    }

    inline void FittedBondDiscountCurve::update() {
        YieldTermStructure::update();
        LazyObject::update();
    }

    inline void FittedBondDiscountCurve::setup() {
        for (auto& bondHelper : bondHelpers_)
            registerWith(bondHelper);
    }

    inline DiscountFactor FittedBondDiscountCurve::discountImpl(Time t) const {
        calculate();
        return fittingMethod_->discount(fittingMethod_->solution_, t);
    }

    inline Integer
    FittedBondDiscountCurve::FittingMethod::numberOfIterations() const {
        return numberOfIterations_;
    }

    inline
    Real FittedBondDiscountCurve::FittingMethod::minimumCostValue() const {
        return costValue_;
    }

    inline 
    EndCriteria::Type FittedBondDiscountCurve::FittingMethod::errorCode() const {
        return errorCode_;
    }

    inline Array FittedBondDiscountCurve::FittingMethod::solution() const {
        return solution_;
    }
    
    inline bool FittedBondDiscountCurve::FittingMethod::constrainAtZero() const {
        return constrainAtZero_;
    }
    
    inline Array FittedBondDiscountCurve::FittingMethod::weights() const {
        return weights_;
    }

    inline Array FittedBondDiscountCurve::FittingMethod::l2() const {
        return l2_;
    }

    inline ext::shared_ptr<OptimizationMethod> 
    FittedBondDiscountCurve::FittingMethod::optimizationMethod() const {
        return optimizationMethod_;
    }

    inline const Constraint& FittedBondDiscountCurve::FittingMethod::constraint() const {
        return constraint_;
    }

    inline DiscountFactor FittedBondDiscountCurve::FittingMethod::discount(const Array& x, Time t) const {
        if (t < minCutoffTime_) {
            // flat fwd extrapolation before min cutoff time
            return std::exp(std::log(discountFunction(x, minCutoffTime_)) / minCutoffTime_ * t);
        } else if (t > maxCutoffTime_) {
            // flat fwd extrapolation after max cutoff time
            return discountFunction(x, maxCutoffTime_) *
                   std::exp((std::log(discountFunction(x, maxCutoffTime_ + 1E-4)) -
                             std::log(discountFunction(x, maxCutoffTime_))) *
                            1E4 * (t - maxCutoffTime_));
        } else {
            return discountFunction(x, t);
        }
    }
}

#endif