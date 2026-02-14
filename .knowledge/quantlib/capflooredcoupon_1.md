d spread = 0.0,
                  Rate cap = Null<Rate>(),
                  Rate floor = Null<Rate>(),
                  const Date& refPeriodStart = Date(),
                  const Date& refPeriodEnd = Date(),
                  const DayCounter& dayCounter = DayCounter(),
                  bool isInArrears = false,
                  const Date& exCouponDate = Date())
        : CappedFlooredCoupon(ext::shared_ptr<FloatingRateCoupon>(new
            IborCoupon(paymentDate, nominal, startDate, endDate, fixingDays,
                       index, gearing, spread, refPeriodStart, refPeriodEnd,
                       dayCounter, isInArrears, exCouponDate)), cap, floor) {}

        void accept(AcyclicVisitor& v) override {
            auto* v1 = dynamic_cast<Visitor<CappedFlooredIborCoupon>*>(&v);
            if (v1 != nullptr)
                v1->visit(*this);
            else
                CappedFlooredCoupon::accept(v);
        }
    };

    class CappedFlooredCmsCoupon : public CappedFlooredCoupon {
      public:
        CappedFlooredCmsCoupon(
                  const Date& paymentDate,
                  Real nominal,
                  const Date& startDate,
                  const Date& endDate,
                  Natural fixingDays,
                  const ext::shared_ptr<SwapIndex>& index,
                  Real gearing = 1.0,
                  Spread spread= 0.0,
                  const Rate cap = Null<Rate>(),
                  const Rate floor = Null<Rate>(),
                  const Date& refPeriodStart = Date(),
                  const Date& refPeriodEnd = Date(),
                  const DayCounter& dayCounter = DayCounter(),
                  bool isInArrears = false,
                  const Date& exCouponDate = Date())
        : CappedFlooredCoupon(ext::shared_ptr<FloatingRateCoupon>(new
            CmsCoupon(paymentDate, nominal, startDate, endDate, fixingDays,
                      index, gearing, spread, refPeriodStart, refPeriodEnd,
                      dayCounter, isInArrears, exCouponDate)), cap, floor) {}

        void accept(AcyclicVisitor& v) override {
            auto* v1 = dynamic_cast<Visitor<CappedFlooredCmsCoupon>*>(&v);
            if (v1 != nullptr)
                v1->visit(*this);
            else
                CappedFlooredCoupon::accept(v);
        }
    };

}

#endif