        //@}
        //! \name Observer interface
        //@{
        void update() override { notifyObservers(); }
        //@}
      private:
        std::vector<ext::shared_ptr<BTP> > btps_;
        std::vector<Real> outstandings_;
        std::vector<Handle<Quote> > quotes_;
        Real outstanding_;
        Size n_;
        std::vector<Real> weights_;
    };

    class RendistatoCalculator : public LazyObject {
      public:
        RendistatoCalculator(ext::shared_ptr<RendistatoBasket> basket,
                             ext::shared_ptr<Euribor> euriborIndex,
                             Handle<YieldTermStructure> discountCurve);
        //! \name Calculations
        //@{
        Rate yield() const;
        Time duration() const;
        // bonds
        const std::vector<Rate>& yields() const;
        const std::vector<Time>& durations() const;
        // swaps
        const std::vector<Time>& swapLengths() const;
        const std::vector<Rate>& swapRates() const;
        const std::vector<Rate>& swapYields() const;
        const std::vector<Time>& swapDurations() const;
        //@}
        //! \name Equivalent Swap proxy
        //@{
        ext::shared_ptr<VanillaSwap> equivalentSwap() const;
        Rate equivalentSwapRate() const;
        Rate equivalentSwapYield() const;
        Time equivalentSwapDuration() const;
        Time equivalentSwapLength() const;
        Spread equivalentSwapSpread() const;
        //@}
      protected:
        //! \name LazyObject interface
        //@{
        void performCalculations() const override;
        //@}
      private:
        ext::shared_ptr<RendistatoBasket> basket_;
        ext::shared_ptr<Euribor> euriborIndex_;
        Handle<YieldTermStructure> discountCurve_;

        mutable std::vector<Rate> yields_;
        mutable std::vector<Time> durations_;
        mutable Time duration_;
        mutable Size equivalentSwapIndex_;

        Size nSwaps_ = 15;
        mutable std::vector<ext::shared_ptr<VanillaSwap> > swaps_;
        std::vector<Time> swapLengths_;
        mutable std::vector<Time> swapBondDurations_;
        mutable std::vector<Rate> swapBondYields_, swapRates_;
    };

    //! RendistatoCalculator equivalent swap lenth Quote adapter
    class RendistatoEquivalentSwapLengthQuote : public Quote {
      public:
        RendistatoEquivalentSwapLengthQuote(ext::shared_ptr<RendistatoCalculator> r);
        Real value() const override;
        bool isValid() const override;

      private:
        ext::shared_ptr<RendistatoCalculator> r_;
    };

    //! RendistatoCalculator equivalent swap spread Quote adapter
    class RendistatoEquivalentSwapSpreadQuote : public Quote {
      public:
        RendistatoEquivalentSwapSpreadQuote(ext::shared_ptr<RendistatoCalculator> r);
        Real value() const override;
        bool isValid() const override;

      private:
        ext::shared_ptr<RendistatoCalculator> r_;
    };

    // inline

    inline Real CCTEU::accruedAmount(Date d) const {
        Real result = FloatingRateBond::accruedAmount(d);
        return ClosestRounding(5)(result);
    }

    inline Real BTP::accruedAmount(Date d) const {
        Real result = FixedRateBond::accruedAmount(d);
        return ClosestRounding(5)(result);
    }

    inline const std::vector<ext::shared_ptr<BTP> >&
    RendistatoBasket::btps() const {
        return btps_;
    }

    inline const std::vector<Handle<Quote> >&
    RendistatoBasket::cleanPriceQuotes() const {
        return quotes_;
    }

    inline Rate RendistatoCalculator::yield() const {
        return std::inner_product(basket_->weights().begin(),
                                  basket_->weights().end(),
                                  yields().begin(), Real(0.0));
    }

    inline Time RendistatoCalculator::duration() const {
        calculate();
        return duration_;
    }

    inline const std::vector<Rate>& RendistatoCalculator::yields() const {
        calculate();
        return yields_;
    }

  