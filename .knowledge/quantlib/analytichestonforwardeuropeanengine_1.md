to generate P1, P2 (fall back on this
        // when reset time is very close, to avoid numerical issues with tReset=0s)
        std::pair<Real, Real> calculateP1P2(Time t,
                                            Handle<Quote>& St,
                                            Real K,
                                            Real ratio,
                                            Real phiRightLimit = 100) const;

        // Integrate P1, P2 over te propagator function to calculate forward-start price
        std::pair<Real, Real> calculateP1P2Hat(Time tenor,
                                               Time resetTime,
                                               Real K,
                                               Real ratio,
                                               Real phiRightLimit = 100,
                                               Real nuRightLimit = 2.0) const;

    };
}

#endif