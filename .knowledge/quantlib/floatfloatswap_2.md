_; }

    inline std::vector<Real> FloatFloatSwap::gearing2() const { return gearing2_; }

    inline std::vector<Real> FloatFloatSwap::cappedRate1() const { return cappedRate1_; }

    inline std::vector<Real> FloatFloatSwap::cappedRate2() const { return cappedRate2_; }

    inline std::vector<Real> FloatFloatSwap::flooredRate1() const { return flooredRate1_; }

    inline std::vector<Real> FloatFloatSwap::flooredRate2() const { return flooredRate2_; }

    inline const DayCounter &FloatFloatSwap::dayCount1() const {
        return dayCount1_;
    }

    inline const DayCounter &FloatFloatSwap::dayCount2() const {
        return dayCount2_;
    }

    inline BusinessDayConvention FloatFloatSwap::paymentConvention1() const {
        return paymentConvention1_;
    }

    inline BusinessDayConvention FloatFloatSwap::paymentConvention2() const {
        return paymentConvention2_;
    }

    inline const Leg &FloatFloatSwap::leg1() const { return legs_[0]; }

    inline const Leg &FloatFloatSwap::leg2() const { return legs_[1]; }
}

#endif