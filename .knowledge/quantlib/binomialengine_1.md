eldTermStructure>(
                new FlatForward(referenceDate, q, divdc)));
        Handle<BlackVolTermStructure> flatVol(
            ext::shared_ptr<BlackVolTermStructure>(
                new BlackConstantVol(referenceDate, volcal, v, voldc)));

        ext::shared_ptr<PlainVanillaPayoff> payoff =
            ext::dynamic_pointer_cast<PlainVanillaPayoff>(arguments_.payoff);
        QL_REQUIRE(payoff, "non-plain payoff given");

        Time maturity = rfdc.yearFraction(referenceDate, maturityDate);

        ext::shared_ptr<StochasticProcess1D> bs(
                         new GeneralizedBlackScholesProcess(
                                      process_->stateVariable(),
                                      flatDividends, flatRiskFree, flatVol));

        TimeGrid grid(maturity, timeSteps_);

        ext::shared_ptr<T> tree(new T(bs, maturity, timeSteps_,
                                        payoff->strike()));

        ext::shared_ptr<BlackScholesLattice<T> > lattice(
            new BlackScholesLattice<T>(tree, r, maturity, timeSteps_));

        DiscretizedVanillaOption option(arguments_, *process_, grid);

        option.initialize(lattice, maturity);

        // Partial derivatives calculated from various points in the
        // binomial tree
        // (see J.C.Hull, "Options, Futures and other derivatives", 6th edition, pp 397/398)

        // Rollback to third-last step, and get underlying prices (s2) &
        // option values (p2) at this point
        option.rollback(grid[2]);
        Array va2(option.values());
        QL_ENSURE(va2.size() == 3, "Expect 3 nodes in grid at second step");
        Real p2u = va2[2]; // up
        Real p2m = va2[1]; // mid
        Real p2d = va2[0]; // down (low)
        Real s2u = lattice->underlying(2, 2); // up price
        Real s2m = lattice->underlying(2, 1); // middle price
        Real s2d = lattice->underlying(2, 0); // down (low) price

        // calculate gamma by taking the first derivate of the two deltas
        Real delta2u = (p2u - p2m)/(s2u-s2m);
        Real delta2d = (p2m-p2d)/(s2m-s2d);
        Real gamma = (delta2u - delta2d) / ((s2u-s2d)/2);

        // Rollback to second-last step, and get option values (p1) at
        // this point
        option.rollback(grid[1]);
        Array va(option.values());
        QL_ENSURE(va.size() == 2, "Expect 2 nodes in grid at first step");
        Real p1u = va[1];
        Real p1d = va[0];
        Real s1u = lattice->underlying(1, 1); // up (high) price
        Real s1d = lattice->underlying(1, 0); // down (low) price

        Real delta = (p1u - p1d) / (s1u - s1d);

        // Finally, rollback to t=0
        option.rollback(0.0);
        Real p0 = option.presentValue();

        // Store results
        results_.value = p0;
        results_.delta = delta;
        results_.gamma = gamma;
        results_.theta = blackScholesTheta(process_,
                                           results_.value,
                                           results_.delta,
                                           results_.gamma);
    }

}


#endif
