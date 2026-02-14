on.nextSequence();
                    Model().guess(guess, this->paramIsFixed_, this->forward_,
                                  this->t_, s.value, this->addParams_);
                    for (Size i = 0; i < this->paramIsFixed_.size(); ++i)
                        if (this->paramIsFixed_[i])
                            guess[i] = this->params_[i];
                }

                Array inversedTransformatedGuess(Model().inverse(
                    guess, this->paramIsFixed_, this->params_, this->forward_));

                ProjectedCostFunction constrainedXABRError(
                    costFunction, inversedTransformatedGuess,
                    this->paramIsFixed_);

                Array projectedGuess(
                    constrainedXABRError.project(inversedTransformatedGuess));

                NoConstraint constraint;
                Problem problem(constrainedXABRError, constraint,
                                projectedGuess);
                tmpEndCriteria = optMethod_->minimize(problem, *endCriteria_);
                Array projectedResult(problem.currentValue());
                Array transfResult(
                    constrainedXABRError.include(projectedResult));

                Array result = Model().direct(transfResult, this->paramIsFixed_,
                                              this->params_, this->forward_);
                tmpInterpolationError = useMaxError_ ? interpolationMaxError()
                                                     : interpolationError();

                if (tmpInterpolationError < bestError) {
                    bestError = tmpInterpolationError;
                    bestParameters = result;
                    this->XABREndCriteria_ = tmpEndCriteria;
                }

            } while (++iterations < maxGuesses_ &&
                     tmpInterpolationError > errorAccept_);

            for (Size i = 0; i < bestParameters.size(); ++i)
                this->params_[i] = bestParameters[i];

            this->error_ = interpolationError();
            this->maxError_ = interpolationMaxError();
        }
    }

    Real value(Real x) const override { return this->modelInstance_->volatility(x, volatilityType_); }

    Real primitive(Real) const override { QL_FAIL("XABR primitive not implemented"); }
    Real derivative(Real) const override { QL_FAIL("XABR derivative not implemented"); }
    Real secondDerivative(Real) const override { QL_FAIL("XABR secondDerivative not implemented"); }

    // calculate total squared weighted difference (L2 norm)
    Real interpolationSquaredError() const {
        Real error, totalError = 0.0;
        I1 x = this->xBegin_;
        I2 y = this->yBegin_;
        auto w = this->weights_.begin();
        for (; x != this->xEnd_; ++x, ++y, ++w) {
            error = (value(*x) - *y);
            totalError += error * error * (*w);
        }
        return totalError;
    }

    // calculate weighted differences
    Array interpolationErrors() const {
        Array results(this->xEnd_ - this->xBegin_);
        I1 x = this->xBegin_;
        Array::iterator r = results.begin();
        I2 y = this->yBegin_;
        auto w = this->weights_.begin();
        for (; x != this->xEnd_; ++x, ++r, ++w, ++y) {
            *r = (value(*x) - *y) * std::sqrt(*w);
        }
        return results;
    }

    Real interpolationError() const {
        Size n = this->xEnd_ - this->xBegin_;
        Real squaredError = interpolationSquaredError();
        return std::sqrt(n * squaredError / (n==1 ? 1 : (n - 1)));
    }

    Real interpolationMaxError() const {
        Real error, maxError = QL_MIN_REAL;
        I1 i = this->xBegin_;
        I2 j = this->yBegin_;
        for (; i != this->xEnd_; ++i, ++j) {
            error = std::fabs(value(*i) - *j);
            maxError = std::max(maxError, error);
        }
        return maxError;
    }

  private:
    class XABRError : public CostFunction {
      public:
        explicit XABRError(XABRInterpolationImpl *