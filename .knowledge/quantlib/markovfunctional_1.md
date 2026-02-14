umerical errors in very long term calibrations.
      The former point is addressed by smile pretreatment options. The latter point
      may be tackled by higher values for the numerical parameters possibly
      together with NTL high precision computing.

      When using a shifted lognormal smile input the lower rate bound is adjusted
      by the shift so that a lower bound of 0.0 always corresponds to the lower
      bound of the shifted distribution.

      If a custom smile is used, this will take full responsibility of inverting
      digital prices to market rates, so digitalGap, marketRateAccuracy,
      lowerRateBound, upperRateBound are irrelavant and the smile moneyness
      checkpoints are only used for the debug model output in this setup.
    */

    class MarkovFunctional : public Gaussian1dModel, public CalibratedModel {

      public:

        class CustomSmileSection : public SmileSection {
        public:
          virtual Real inverseDigitalCall(Real price, Real discount = 1.0) const = 0;
        };

        class CustomSmileFactory {
        public:
          virtual ~CustomSmileFactory() = default;
          virtual ext::shared_ptr<CustomSmileSection>
          smileSection(const ext::shared_ptr<SmileSection>& source, Real atm) const = 0;
        };

        struct ModelSettings {

            // NoPayoffExtrapolation overrides ExtrapolatePayoffFlat
            enum Adjustments {
                AdjustNone = 0,
                AdjustDigitals = 1 << 0,
                AdjustYts = 1 << 1,
                ExtrapolatePayoffFlat = 1 << 2,
                NoPayoffExtrapolation = 1 << 3,
                KahaleSmile = 1 << 4,
                SmileExponentialExtrapolation = 1 << 5,
                KahaleInterpolation = 1 << 6,
                SmileDeleteArbitragePoints = 1 << 7,
                SabrSmile = 1 << 8,
                CustomSmile = 1 << 9
            };

            ModelSettings() : adjustments_(KahaleSmile | SmileExponentialExtrapolation) {}

            ModelSettings(Size yGridPoints,
                          Real yStdDevs,
                          Size gaussHermitePoints,
                          Real digitalGap,
                          Real marketRateAccuracy,
                          Real lowerRateBound,
                          Real upperRateBound,
                          int adjustments,
                          std::vector<Real> smileMoneyCheckpoints = std::vector<Real>(),
                          ext::shared_ptr<CustomSmileFactory> customSmileFactory =
                              ext::shared_ptr<CustomSmileFactory>())
            : yGridPoints_(yGridPoints), yStdDevs_(yStdDevs),
              gaussHermitePoints_(gaussHermitePoints), digitalGap_(digitalGap),
              marketRateAccuracy_(marketRateAccuracy), lowerRateBound_(lowerRateBound),
              upperRateBound_(upperRateBound), adjustments_(adjustments),
              smileMoneynessCheckpoints_(std::move(smileMoneyCheckpoints)),
              customSmileFactory_(std::move(customSmileFactory)) {}

            void validate() {

                if ((adjustments_ & KahaleInterpolation) != 0)
                    addAdjustment(KahaleSmile);

                if ((adjustments_ & KahaleSmile) != 0 &&
                    (adjustments_ & SmileDeleteArbitragePoints) != 0) {
                    addAdjustment(KahaleInterpolation);
                }

                QL_REQUIRE((adjustments_ & SabrSmile) == 0 ||
                           (adjustments_ & KahaleSmile) == 0 ||
                           (adjustments_ & CustomSmile) == 0
                           ,
                           "Only one of KahaleSmile, SabrSmile and CustomSmile"
                           "can be specified at the same time");
                QL_REQUIRE(yGridPoints_ > 0, "At least one grid point ("
                                                 << yGridPoints_
                                                 << ") for the state process "
          