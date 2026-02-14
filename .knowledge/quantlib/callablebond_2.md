 Date(),
                              const CallabilitySchedule& putCallSchedule = {},
                              const Period& exCouponPeriod = Period(),
                              const Calendar& exCouponCalendar = Calendar(),
                              BusinessDayConvention exCouponConvention = Unadjusted,
                              bool exCouponEndOfMonth = false);
    };

    //! callable/puttable zero coupon bond
    /*! Callable zero coupon bond class.

        \ingroup instruments
    */
    class CallableZeroCouponBond : public CallableBond {
      public:
        CallableZeroCouponBond(Natural settlementDays,
                               Real faceAmount,
                               const Calendar& calendar,
                               const Date& maturityDate,
                               const DayCounter& dayCounter,
                               BusinessDayConvention paymentConvention = Following,
                               Real redemption = 100.0,
                               const Date& issueDate = Date(),
                               const CallabilitySchedule& putCallSchedule = {});
    };

}

#endif
