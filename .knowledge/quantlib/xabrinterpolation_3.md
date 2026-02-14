xabr) : xabr_(xabr) {}

        Real value(const Array& x) const override {
            const Array y = Model().direct(x, xabr_->paramIsFixed_,
                                           xabr_->params_, xabr_->forward_);
            for (Size i = 0; i < xabr_->params_.size(); ++i)
                xabr_->params_[i] = y[i];
            xabr_->updateModelInstance();
            return xabr_->interpolationSquaredError();
        }

        Array values(const Array& x) const override {
            const Array y = Model().direct(x, xabr_->paramIsFixed_,
                                           xabr_->params_, xabr_->forward_);
            for (Size i = 0; i < xabr_->params_.size(); ++i)
                xabr_->params_[i] = y[i];
            xabr_->updateModelInstance();
            return xabr_->interpolationErrors();
        }

      private:
        XABRInterpolationImpl *xabr_;
    };
    ext::shared_ptr<EndCriteria> endCriteria_;
    ext::shared_ptr<OptimizationMethod> optMethod_;
    const Real errorAccept_;
    const bool useMaxError_;
    const Size maxGuesses_;
    bool vegaWeighted_;
    NoConstraint constraint_;
    VolatilityType volatilityType_;
};

} // namespace QuantLib

#endif
