ptr<CashFlow>(new
                    DigitalCouponType(
                             underlying,
                             detail::get(callStrikes, i, Null<Real>()),
                             callPosition,
                             isCallATMIncluded,
                             detail::get(callDigitalPayoffs, i, Null<Real>()),
                             detail::get(putStrikes, i, Null<Real>()),
                             putPosition,
                             isPutATMIncluded,
                             detail::get(putDigitalPayoffs, i, Null<Real>()),
                             replication, nakedOption)));
            }
        }
        return leg;
    }

}

#endif
