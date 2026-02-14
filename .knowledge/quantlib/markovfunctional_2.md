                                          "discretization must be "
                                                    "given");
                QL_REQUIRE(yStdDevs_ > 0.0,
                           "Multiple of standard deviations covered by state "
                           "process discretization ("
                               << yStdDevs_ << ") must be positive");
                QL_REQUIRE(gaussHermitePoints_ > 0,
                           "Number of gauss hermite integration points ("
                               << gaussHermitePoints_ << ") must be positive");
                QL_REQUIRE(digitalGap_ > 0.0, "Digital gap ("
                                                  << digitalGap_
                                                  << ") must be positive");
                QL_REQUIRE(marketRateAccuracy_ > 0.0,
                           "Market rate accuracy (" << marketRateAccuracy_
                                                    << ") must be positive");
                QL_REQUIRE(
                    (adjustments_ & KahaleSmile) == 0 || lowerRateBound_ == 0.0,
                    "If Kahale extrapolation is used, the lower rate bound ("
                        << lowerRateBound_ << ") must be zero.");
                QL_REQUIRE(
                    lowerRateBound_ < upperRateBound_,
                    "Lower rate bound ("
                        << lowerRateBound_
                        << ") must be strictly less than upper rate bound ("
                        << upperRateBound_ << ")");
                QL_REQUIRE(((adjustments_ & CustomSmile) == 0) ||
                           customSmileFactory_,
                           "missing CustomSmileFactoy");
            }

            ModelSettings &withYGridPoints(Size n) {
                yGridPoints_ = n;
                return *this;
            }
            ModelSettings &withYStdDevs(Real s) {
                yStdDevs_ = s;
                return *this;
            }
            ModelSettings &withGaussHermitePoints(Size n) {
                gaussHermitePoints_ = n;
                return *this;
            }
            ModelSettings &withDigitalGap(Real d) {
                digitalGap_ = d;
                return *this;
            }
            ModelSettings &withMarketRateAccuracy(Real a) {
                marketRateAccuracy_ = a;
                return *this;
            }
            ModelSettings &withUpperRateBound(Real u) {
                upperRateBound_ = u;
                return *this;
            }
            ModelSettings &withLowerRateBound(Real l) {
                lowerRateBound_ = l;
                return *this;
            }
            ModelSettings &withAdjustments(int a) {
                adjustments_ = a;
                return *this;
            }
            ModelSettings &addAdjustment(int a) {
                adjustments_ |= a;
                return *this;
            }
            ModelSettings &removeAdjustment(int a) {
                adjustments_ &= ~a;
                return *this;
            }
            ModelSettings &withSmileMoneynessCheckpoints(const std::vector<Real>& m) {
                smileMoneynessCheckpoints_ = m;
                return *this;
            }
            ModelSettings &withCustomSmileFactory(const ext::shared_ptr<CustomSmileFactory>& f) {
                customSmileFactory_ = f;
                return *this;
            }

            Size yGridPoints_ = 64;
            Real yStdDevs_ = 7.0;
            Size gaussHermitePoints_ = 32;
            Real digitalGap_ = 1E-5, marketRateAccuracy_ = 1E-7;
            Real lowerRateBound_ = 0.0, upperRateBound_ = 2.0;
            int adjustments_;
            std::vector<Real> smileMoneynessCheckpoints_;
            ext::shared_ptr<CustomSmileFactory> customSmileFactory_;
        };

        struct CalibrationPoint {
            bool isCaplet_;
            Period tenor_;
            std::vector<Date> paymentDates_;
            std::vector<