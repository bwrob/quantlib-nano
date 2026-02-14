on c(f_, s_, a, b_);
                return c(k1_) - c1_;
            }
            Real k0_, k1_, c0_, c1_, c0p_, c1p_;
            mutable Real s_, f_, b_;
        };

        struct sHelper {
            sHelper(Real k0, Real c0, Real c0p) : k0_(k0), c0_(c0), c0p_(c0p) {}
            Real operator()(Real s) const {
                s = std::max(s, 0.0);
                boost::math::normal_distribution<Real> normal;
                Real d20 = boost::math::quantile(normal, -c0p_);
                f_ = k0_ * std::exp(s * d20 + s * s / 2.0);
                QL_REQUIRE(f_ < QL_KAHALE_FMAX, "dummy"); // this is caught
                cFunction c(f_, s, 0.0, 0.0);
                return c(k0_) - c0_;
            }
            Real k0_, c0_, c0p_;
            mutable Real f_;
        };

        struct sHelper1 {
            sHelper1(Real k1, Real c0, Real c1, Real c1p)
                : k1_(k1), c0_(c0), c1_(c1), c1p_(c1p) {}
            Real operator()(Real s) const {
                s = std::max(s, 0.0);
                boost::math::normal_distribution<Real> normal;
                Real d21 = boost::math::quantile(normal, -c1p_);
                f_ = k1_ * std::exp(s * d21 + s * s / 2.0);
                QL_REQUIRE(f_ < QL_KAHALE_FMAX, "dummy"); // this is caught
                b_ = c0_ - f_;
                cFunction c(f_, s, 0.0, b_);
                return c(k1_) - c1_;
            }
            Real k1_, c0_, c1_, c1p_;
            mutable Real f_, b_;
        };

        KahaleSmileSection(const ext::shared_ptr<SmileSection>& source,
                           Real atm = Null<Real>(),
                           bool interpolate = false,
                           bool exponentialExtrapolation = false,
                           bool deleteArbitragePoints = false,
                           const std::vector<Real>& moneynessGrid = std::vector<Real>(),
                           Real gap = 1.0E-5,
                           int forcedLeftIndex = -1,
                           int forcedRightIndex = QL_MAX_INTEGER);

        Real minStrike() const override { return -shift(); }
        Real maxStrike() const override { return QL_MAX_REAL; }
        Real atmLevel() const override { return f_; }
        const Date& exerciseDate() const override { return source_->exerciseDate(); }
        Time exerciseTime() const override { return source_->exerciseTime(); }
        const DayCounter& dayCounter() const override { return source_->dayCounter(); }
        const Date& referenceDate() const override { return source_->referenceDate(); }
        VolatilityType volatilityType() const override { return source_->volatilityType(); }
        Real shift() const override { return source_->shift(); }

        Real leftCoreStrike() const { return k_[leftIndex_]; }
        Real rightCoreStrike() const { return k_[rightIndex_]; }

        std::pair<Size, Size> coreIndices() const {
            return std::make_pair(leftIndex_, rightIndex_);
        }

        Real optionPrice(Rate strike,
                         Option::Type type = Option::Call,
                         Real discount = 1.0) const override;

      protected:
        Volatility volatilityImpl(Rate strike) const override;

      private:
        Size index(Rate strike) const;
        void compute();
        ext::shared_ptr<SmileSection> source_;
        std::vector<Real> moneynessGrid_, k_, c_;
        Real f_;
        const Real gap_;
        Size leftIndex_, rightIndex_;
        std::vector<ext::shared_ptr<cFunction> > cFunctions_;
        const bool interpolate_, exponentialExtrapolation_;
        int forcedLeftIndex_, forcedRightIndex_;
        ext::shared_ptr<SmileSectionUtils> ssutils_;
    };
}

#endif