<< d2 << ")");
            Time t = dc_.yearFraction(d1, d2, refStart, refEnd);
            return compoundFactor(t);
        }
        //@}

        //! \name implied rate calculations
        //@{

        //! implied interest rate for a given compound factor at a given time.
        /*! The resulting InterestRate has the day-counter provided as input.

            \warning Time must be measured using the day-counter provided
                     as input.
        */
        static InterestRate impliedRate(Real compound,
                                        const DayCounter& resultDC,
                                        Compounding comp,
                                        Frequency freq,
                                        Time t);

        //! implied rate for a given compound factor between two dates.
        /*! The resulting rate is calculated taking the required
            day-counting rule into account.
        */
        static InterestRate impliedRate(Real compound,
                                        const DayCounter& resultDC,
                                        Compounding comp,
                                        Frequency freq,
                                        const Date& d1,
                                        const Date& d2,
                                        const Date& refStart = Date(),
                                        const Date& refEnd = Date()) {
            QL_REQUIRE(d2>=d1,
                       "d1 (" << d1 << ") "
                       "later than d2 (" << d2 << ")");
            Time t = resultDC.yearFraction(d1, d2, refStart, refEnd);
            return impliedRate(compound, resultDC, comp, freq, t);
        }
        //@}

        //! \name equivalent rate calculations
        //@{

        //! equivalent interest rate for a compounding period t.
        /*! The resulting InterestRate shares the same implicit
            day-counting rule of the original InterestRate instance.

            \warning Time must be measured using the InterestRate's
                     own day counter.
        */
        InterestRate equivalentRate(Compounding comp,
                                    Frequency freq,
                                    Time t) const {
            return impliedRate(compoundFactor(t), dc_, comp, freq, t);
        }

        //! equivalent rate for a compounding period between two dates
        /*! The resulting rate is calculated taking the required
            day-counting rule into account.
        */
        InterestRate equivalentRate(const DayCounter& resultDC,
                                    Compounding comp,
                                    Frequency freq,
                                    Date d1,
                                    Date d2,
                                    const Date& refStart = Date(),
                                    const Date& refEnd = Date()) const {
            QL_REQUIRE(d2>=d1,
                       "d1 (" << d1 << ") "
                       "later than d2 (" << d2 << ")");
            Time t1 = dc_.yearFraction(d1, d2, refStart, refEnd);
            Time t2 = resultDC.yearFraction(d1, d2, refStart, refEnd);
            return impliedRate(compoundFactor(t1), resultDC, comp, freq, t2);
        }
        //@}
      private:
        Rate r_;
        DayCounter dc_;
        Compounding comp_;
        bool freqMakesSense_;
        Real freq_;
    };

    /*! \relates InterestRate */
    std::ostream& operator<<(std::ostream&,
                             const InterestRate&);

}

#endif