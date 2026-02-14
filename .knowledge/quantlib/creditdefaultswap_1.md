                                  scheduled current coupon at the start 
                                    of the contract. The rebate date is not
                                    provided but computed to be two days after
                                    protection start.
            @param tradeDate  The contract's trade date. It will be used with the \p cashSettlementDays to determine 
                              the date on which the cash settlement amount is paid. If not given, the trade date is 
                              guessed from the protection start date and \p schedule date generation rule.
            @param cashSettlementDays  The number of business days from \p tradeDate to cash settlement date.
        */
        CreditDefaultSwap(Protection::Side side,
                          Real notional,
                          Rate spread,
                          const Schedule& schedule,
                          BusinessDayConvention paymentConvention,
                          const DayCounter& dayCounter,
                          bool settlesAccrual = true,
                          bool paysAtDefaultTime = true,
                          const Date& protectionStart = Date(),
                          ext::shared_ptr<Claim> = ext::shared_ptr<Claim>(),
                          const DayCounter& lastPeriodDayCounter = DayCounter(),
                          bool rebatesAccrual = true,
                          const Date& tradeDate = Date(),
                          Natural cashSettlementDays = 3);
        //! CDS quoted as upfront and running spread
        /*! @param side  Whether the protection is bought or sold.
            @param notional  Notional value
            @param upfront Upfront in fractional units.
            @param spread Running spread in fractional units.
            @param schedule  Coupon schedule.
            @param paymentConvention  Business-day convention for
                                      payment-date adjustment.
            @param dayCounter  Day-count convention for accrual.
            @param settlesAccrual Whether or not the accrued coupon is
                                  due in the event of a default.
            @param paysAtDefaultTime If set to true, any payments
                                     triggered by a default event are
                                     due at default time. If set to
                                     false, they are due at the end of
                                     the accrual period.
            @param protectionStart  The first date where a default event will trigger the contract. 
                                    Before the CDS Big Bang 2009, this was typically trade date (T) + 1 calendar day.
                                    After the CDS Big Bang 2009, protection is typically effective immediately i.e. on 
                                    trade date so this is what should be entered for protection start.
                                    Notice that there is no default lookback period and protection start here. 
                                    In the way it determines the dirty amount it is more like the trade execution date.
            @param upfrontDate Settlement date for the upfront and accrual 
                                    rebate (if any) payments.
                                    Typically T+3, this is also the default 
                                    value.
            @param lastPeriodDayCounter Day-count convention for accrual in last period
            @param rebatesAccrual  The protection seller pays the accrued 
                                    scheduled current coupon at the start 
                                    of the contract. The rebate date is not
                                    provided but computed to be two days after
                                    protection start.
            @param tradeDate  The contract's trade date. It will be used with 