tion(const Array& x, Time t) const override;
        Size size_;
    };


    //! Spread fitting method helper
    /*! Fits a spread curve on top of a discount function according
        to the given parametric method
    */
    class SpreadFittingMethod
        : public FittedBondDiscountCurve::FittingMethod {
      public:
        SpreadFittingMethod(const ext::shared_ptr<FittingMethod>& method,
                            Handle<YieldTermStructure> discountCurve,
                            Real minCutoffTime = 0.0,
                            Real maxCutoffTime = QL_MAX_REAL);
        std::unique_ptr<FittedBondDiscountCurve::FittingMethod> clone() const override;
    protected:
      void init() override;

    private:
      Size size() const override;
      DiscountFactor discountFunction(const Array& x, Time t) const override;
      // underlying parametric method
      ext::shared_ptr<FittingMethod> method_;
      // adjustment in case underlying discount curve has different reference date
      DiscountFactor rebase_;
      // discount curve from on top of which the spread will be calculated
      Handle<YieldTermStructure> discountingCurve_;
    };
}


#endif