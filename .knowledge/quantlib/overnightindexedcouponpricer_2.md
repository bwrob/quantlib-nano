 floorletRate([[maybe_unused]] Rate effectiveCap, [[maybe_unused]] bool dailyCapFloor) const override {
          QL_FAIL("ArithmeticAveragedOvernightIndexedCouponPricer::floorletRate(Rate, bool) not implemented");
        }
        Rate averageRate(const Date& date) const override;
      protected:
        Real convAdj1(Time ts, Time te) const;
        Real convAdj2(Time ts, Time te) const;
        bool byApprox_;
        Real mrs_;
        Real vol_;
    };
}

#endif