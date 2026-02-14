yCounter = model_->termStructure()->dayCounter();
            Time forwardMeasureTime =
                dayCounter.yearFraction(referenceDate,
                                        arguments_.endDates.back());
            return ext::shared_ptr<path_pricer_type>(
                     new detail::HullWhiteCapFloorPricer(arguments_, model_,
                                                         forwardMeasureTime));
        }

        TimeGrid timeGrid() const {

            Date referenceDate = model_->termStructure()->referenceDate();
            DayCounter dayCounter = model_->termStructure()->dayCounter();

            // only add future fixing times...
            std::vector<Time> times;
            for (Size i=0; i<arguments_.fixingDates.size(); i++) {
                if (arguments_.fixingDates[i] > referenceDate)
                    times.push_back(
                          dayCounter.yearFraction(referenceDate,
                                                  arguments_.fixingDates[i]));
            }
            // ...and maturity.
            times.push_back(
                        dayCounter.yearFraction(referenceDate,
                                                arguments_.endDates.back()));
            return TimeGrid(times.begin(), times.end());
        }

        ext::shared_ptr<path_generator_type> pathGenerator() const {

            Handle<YieldTermStructure> curve = model_->termStructure();
            Date referenceDate = curve->referenceDate();
            DayCounter dayCounter = curve->dayCounter();

            Time forwardMeasureTime =
                dayCounter.yearFraction(referenceDate,
                                        arguments_.endDates.back());
            Array parameters = model_->params();
            Real a = parameters[0], sigma = parameters[1];
            ext::shared_ptr<HullWhiteForwardProcess> process(
                                new HullWhiteForwardProcess(curve, a, sigma));
            process->setForwardMeasureTime(forwardMeasureTime);

            TimeGrid grid = this->timeGrid();
            typename RNG::rsg_type generator =
                RNG::make_sequence_generator(grid.size()-1,seed_);
            return ext::shared_ptr<path_generator_type>(
                             new path_generator_type(process, grid, generator,
                                                     brownianBridge_));
        }
    };



    //! Monte Carlo Hull-White cap-floor engine factory
    template <class RNG = PseudoRandom, class S = Statistics>
    class MakeMCHullWhiteCapFloorEngine {
      public:
        MakeMCHullWhiteCapFloorEngine(ext::shared_ptr<HullWhite>);
        // named parameters
        MakeMCHullWhiteCapFloorEngine& withBrownianBridge(bool b = true);
        MakeMCHullWhiteCapFloorEngine& withSamples(Size samples);
        MakeMCHullWhiteCapFloorEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCHullWhiteCapFloorEngine& withMaxSamples(Size samples);
        MakeMCHullWhiteCapFloorEngine& withSeed(BigNatural seed);
        MakeMCHullWhiteCapFloorEngine& withAntitheticVariate(bool b = true);
        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<HullWhite> model_;
        bool antithetic_ = false;
        Size samples_, maxSamples_;
        Real tolerance_;
        bool brownianBridge_ = false;
        BigNatural seed_ = 0;
    };


    // inline definitions

    template <class RNG, class S>
    inline MakeMCHullWhiteCapFloorEngine<RNG, S>::MakeMCHullWhiteCapFloorEngine(
        ext::shared_ptr<HullWhite> model)
    : model_(std::move(model)), samples_(Null<Size>()), maxSamples_(Null<Size>()),
      tolerance_(Null<Real>()) {}

    template <class RNG, class S>
    inline MakeMCHullWhiteCapFloorEngine<RNG,S>&
    MakeMCHullWhiteCapFloorEngine<RNG,S>::withSamples(Size samples) {
        QL_REQUIRE(tolerance_ == Null<Real>(),
                   "tolerance already set");
      