_REQUIRE(!triggered(s0), "barrier touched");

        DayCounter rfdc  = process_->riskFreeRate()->dayCounter();
        DayCounter divdc = process_->dividendYield()->dayCounter();
        DayCounter voldc = process_->blackVolatility()->dayCounter();
        Calendar volcal = process_->blackVolatility()->calendar();

        Volatility v = process_->blackVolatility()->blackVol(
            arguments_.exercise->lastDate(), s0);
        Date maturityDate = arguments_.exercise->lastDate();
        Rate r = process_->riskFreeRate()->zeroRate(maturityDate,
            rfdc, Continuous, NoFrequency);
        Rate q = process_->dividendYield()->zeroRate(maturityDate,
            divdc, Continuous, NoFrequency);
        Date referenceDate = process_->riskFreeRate()->referenceDate();

        // binomial trees with constant coefficient
        Handle<YieldTermStructure> flatRiskFree(
            ext::shared_ptr<YieldTermStructure>(
                new FlatForward(referenceDate, r, rfdc)));
        Handle<YieldTermStructure> flatDividends(
            ext::shared_ptr<YieldTermStructure>(
                new FlatForward(referenceDate, q, divdc)));
        Handle<BlackVolTermStructure> flatVol(
            ext::shared_ptr<BlackVolTermStructure>(
                new BlackConstantVol(referenceDate, volcal, v, voldc)));

        Time maturity = rfdc.yearFraction(referenceDate, maturityDate);

        ext::shared_ptr<StochasticProcess1D> bs(
                         new GeneralizedBlackScholesProcess(
                                      process_->stateVariable(),
                                      flatDividends, flatRiskFree, flatVol));

        // correct timesteps to ensure a (local) minimum, using Boyle and Lau
        // approach. See Journal of Derivatives, 1/1994,
        // "Bumping up against the barrier with the binomial method"
        // Note: this approach works only for CoxRossRubinstein lattices, so
        // is disabled if T is not a CoxRossRubinstein or derived from it.
        Size optimum_steps = timeSteps_;
        if (std::is_base_of_v<CoxRossRubinstein, T> &&
            maxTimeSteps_ > timeSteps_ && s0 > 0 && arguments_.barrier > 0) {
            Real divisor;
            if (s0 > arguments_.barrier)
               divisor = std::pow(std::log(s0 / arguments_.barrier), 2);
            else
               divisor = std::pow(std::log(arguments_.barrier / s0), 2);
            if (!close(divisor,0)) {
                for (Size i=1; i < timeSteps_ ; ++i) {
                    Size optimum = Size(( i*i * v*v * maturity) / divisor);
                    if (timeSteps_ < optimum) {
                        optimum_steps = optimum;
                        break; // found first minimum with iterations>=timesteps
                    }
                }
            }

            if (optimum_steps > maxTimeSteps_) 
               optimum_steps = maxTimeSteps_; // too high, limit
        }

        TimeGrid grid(maturity, optimum_steps);

        ext::shared_ptr<T> tree(new T(bs, maturity, optimum_steps,
                                        payoff->strike()));

        ext::shared_ptr<BlackScholesLattice<T> > lattice(
            new BlackScholesLattice<T>(tree, r, maturity, optimum_steps));

        D option(arguments_, *process_, grid);
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
        Real s2m = lattice->underlyi