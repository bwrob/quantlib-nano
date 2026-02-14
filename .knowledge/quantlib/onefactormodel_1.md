h);
        }
        void setSpread(Spread spread)
        {
            spread_=spread;
        }
      private:
        ext::shared_ptr<TrinomialTree> tree_;
        ext::shared_ptr<ShortRateDynamics> dynamics_;
        class Helper;
        Spread spread_;
    };

    //! Single-factor affine base class
    /*! Single-factor models with an analytical formula for discount bonds
        should inherit from this class. They must then implement the
        functions \f$ A(t,T) \f$ and \f$ B(t,T) \f$ such that
        \f[
            P(t, T, r_t) = A(t,T)e^{ -B(t,T) r_t}.
        \f]

        \ingroup shortrate
    */
    class OneFactorAffineModel : public OneFactorModel,
                                 public AffineModel {
      public:
        explicit OneFactorAffineModel(Size nArguments)
        : OneFactorModel(nArguments) {}

        Real discountBond(Time now, Time maturity, Array factors) const override {
            return discountBond(now, maturity, factors[0]);
        }

        Real discountBond(Time now, Time maturity, Rate rate) const {
            return A(now, maturity)*std::exp(-B(now, maturity)*rate);
        }

        DiscountFactor discount(Time t) const override;

      protected:
        virtual Real A(Time t, Time T) const = 0;
        virtual Real B(Time t, Time T) const = 0;
    };

}

#endif