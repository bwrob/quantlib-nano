 and survivals
      */
      /*
        Note: curve extrapolation has a different meaning on different curve
          types; for matched to market structures the credit market curves
          would be requested for extrapolation; for affine models on top of
          a static term structure it is this one that will be required for
          extrapolation.
       */
      Probability conditionalSurvivalProbability(const Date& dFwd,
                                                 const Date& dTgt,
                                                 Real yVal,
                                                 bool extrapolate = false) const {
          return conditionalSurvivalProbability(timeFromReference(dFwd), timeFromReference(dTgt),
                                                yVal, extrapolate);
        }
        Probability conditionalSurvivalProbability(
                Time tFwd, Time tgt, Real yVal,
                bool extrapolate = false) const
        {
            #if defined(QL_EXTRA_SAFETY_CHECKS)
                QL_REQUIRE(tgt >= tFwd, "Incorrect dates ordering.");
            #endif
            checkRange(tFwd, extrapolate);
            checkRange(tgt, extrapolate);

            // \todo ADD JUMPS TREATMENT

            return conditionalSurvivalProbabilityImpl(tFwd, tgt, yVal);
        }
        //@}
        // DefaultTermStructure interface
        using DefaultProbabilityTermStructure::hazardRate;
        Rate hazardRate(Time t, bool extrapolate = false) const {
            checkRange(t, extrapolate);
            return hazardRateImpl(t);
        }
    protected:
        //! \name DefaultProbabilityTermStructure implementation
        //@{
      Probability survivalProbabilityImpl(Time) const override;
      Real defaultDensityImpl(Time) const override;
      //@}
      // avoid call super
      // \todo addd date overload
      virtual Probability conditionalSurvivalProbabilityImpl(Time tFwd, Time tgt, Real yVal) const;

      // HazardRateStructure interface
      Real hazardRateImpl(Time) const override {
          // no deterministic component
          return 0.;
      }

        ext::shared_ptr<OneFactorAffineModel> model_;
    };

    inline Probability
        OneFactorAffineSurvivalStructure::survivalProbabilityImpl(
        Time t) const
    {
        Real initValHR =
            model_->dynamics()->shortRate(0.,
                model_->dynamics()->process()->x0());

        return model_->discountBond(0., t, initValHR);
    }

    inline Probability
        OneFactorAffineSurvivalStructure::conditionalSurvivalProbabilityImpl(
            Time tFwd, Time tgt, Real yVal) const {
        return model_->discountBond(tFwd, tgt, yVal);
    }

    inline Real
        OneFactorAffineSurvivalStructure::defaultDensityImpl(Time t) const {
        Real initValHR =
            model_->dynamics()->shortRate(0.,
                model_->dynamics()->process()->x0());;

        return hazardRateImpl(t)*survivalProbabilityImpl(t) /
            model_->discountBond(0., t, initValHR);
    }
}

#endif
