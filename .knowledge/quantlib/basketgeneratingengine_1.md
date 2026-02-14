        virtual const Date underlyingLastDate() const = 0;

        virtual const Array initialGuess(const Date &expiry) const = 0; // return (nominal,
                                                                        // maturity, rate)

      private:

        const Handle<Gaussian1dModel> onefactormodel_;
        const Handle<Quote> oas_;
        const Handle<YieldTermStructure> discountCurve_;

        class MatchHelper : public CostFunction {
          public:
            MatchHelper(const Swap::Type type,
                        const Real npv,
                        const Real delta,
                        const Real gamma,
                        ext::shared_ptr<Gaussian1dModel> model,
                        ext::shared_ptr<SwapIndex> indexBase,
                        const Date& expiry,
                        const Real maxMaturity,
                        const Real h)
            : type_(type), mdl_(std::move(model)), indexBase_(std::move(indexBase)),
              expiry_(expiry), maxMaturity_(maxMaturity), npv_(npv), delta_(delta), gamma_(gamma),
              h_(h) {}

            Real NPV(const ext::shared_ptr<VanillaSwap>& swap,
                     Real fixedRate,
                     Real nominal,
                     Real y,
                     int type) const {
                Real npv = 0.0;
                for (const auto& i : swap->fixedLeg()) {
                    ext::shared_ptr<FixedRateCoupon> c =
                        ext::dynamic_pointer_cast<FixedRateCoupon>(i);
                    npv -=
                        fixedRate * c->accrualPeriod() * nominal *
                        mdl_->zerobond(c->date(), expiry_, y,
                                       indexBase_->discountingTermStructure());
                }
                for (const auto& i : swap->floatingLeg()) {
                    ext::shared_ptr<IborCoupon> c = ext::dynamic_pointer_cast<IborCoupon>(i);
                    npv +=
                        mdl_->forwardRate(c->fixingDate(), expiry_, y,
                                          c->iborIndex()) *
                        c->accrualPeriod() * nominal *
                        mdl_->zerobond(c->date(), expiry_, y,
                                       indexBase_->discountingTermStructure());
                }
                return (Real)type * npv;
            }

            Real value(const Array& v) const override {
                Array vals = values(v);
                Real res = 0.0;
                for (Real val : vals) {
                    res += val * val;
                }
                return std::sqrt(res / vals.size());
            }

            Array values(const Array& v) const override {
                // transformations
                int type = type_; // start with same type as non standard
                                  // underlying (1 means payer, -1 receiver)
                Real nominal = std::fabs(v[0]);
                if (v[0] < 0.0)
                    type *= -1;
                Real maturity = std::min(std::fabs(v[1]), maxMaturity_);

                Real fixedRate = v[2]; // allow for negative rates explicitly
                // (though it might not be reasonable for calibration depending
                // on the model to calibrate and the market instrument quotation)
                Size years = (Size)std::floor(maturity);
                maturity -= (Real)years;
                maturity *= 12.0;
                Size months = (Size)std::floor(maturity);
                Real alpha = 1.0 - (maturity - (Real)months);
                if (years == 0 && months == 0) {
                    months = 1;  // ensure a maturity of at least one month ...
                    alpha = 1.0; // ... but in this case only look at the lower
                                 // maturity swap
                }
                // maturity -= (Real)months; maturity *= 365.25;
                // Size days = (Size)std::floor(maturity);
                //
