      process_->riskFreeRate()->discount(dividends_[i]->date());
        }
        QL_REQUIRE(s0 > 0.0,
            "negative value after subtracting dividends");

        // binomial trees with constant coefficient
        Handle<Quote> underlying(ext::shared_ptr<Quote>(new SimpleQuote(s0)));
        Handle<YieldTermStructure> flatRiskFree(ext::shared_ptr<YieldTermStructure>(
            new FlatForward(referenceDate, riskFreeRate, rfdc)));
        Handle<YieldTermStructure> flatDividends(
            ext::shared_ptr<YieldTermStructure>(new FlatForward(referenceDate, q, divdc)));
        Handle<BlackVolTermStructure> flatVol(ext::shared_ptr<BlackVolTermStructure>(
            new BlackConstantVol(referenceDate, volcal, v, voldc)));

        Time maturity = rfdc.yearFraction(arguments_.settlementDate, maturityDate);
        Real strike = arguments_.redemption / arguments_.conversionRatio ;

        ext::shared_ptr<GeneralizedBlackScholesProcess> bs(
            new GeneralizedBlackScholesProcess(underlying, flatDividends, flatRiskFree, flatVol));
        ext::shared_ptr<T> tree(new T(bs, maturity, timeSteps_, strike));

        Real creditSpread = creditSpread_->value();

        ext::shared_ptr<Lattice> lattice(new TsiveriotisFernandesLattice<T>(
            tree, riskFreeRate, maturity, timeSteps_, creditSpread, v, q));

        DiscretizedConvertible convertible(arguments_, bs, dividends_, creditSpread_, TimeGrid(maturity, timeSteps_));

        convertible.initialize(lattice, maturity);
        convertible.rollback(0.0);
        results_.value = results_.settlementValue = convertible.presentValue();
        QL_ENSURE(results_.value < std::numeric_limits<Real>::max(),
                  "floating-point overflow on tree grid");
    }

}


#endif