      static const Size requiredPoints = 2;
        static const Size dataSizeAdjustment = 1;

        ConvexMonotone(Real quadraticity = 0.3,
                       Real monotonicity = 0.7,
                       bool forcePositive = true)
        : quadraticity_(quadraticity), monotonicity_(monotonicity),
          forcePositive_(forcePositive) {}

        template <class I1, class I2>
        Interpolation interpolate(const I1& xBegin, const I1& xEnd,
                                  const I2& yBegin) const {
            return ConvexMonotoneInterpolation<I1,I2>(xBegin, xEnd, yBegin,
                                                      quadraticity_,
                                                      monotonicity_,
                                                      forcePositive_,
                                                      false);
        }

        template <class I1, class I2>
        Interpolation localInterpolate(const I1& xBegin, const I1& xEnd,
                                       const I2& yBegin, Size localisation,
                                       Interpolation& prevInterpolation,
                                       Size finalSize) const {
            Size length = std::distance(xBegin, xEnd);
            if (length - localisation == 1) { // the first time this
                                              // function is called
                if (length == finalSize) {
                    return ConvexMonotoneInterpolation<I1,I2>(xBegin, xEnd,
                                                              yBegin,
                                                              quadraticity_,
                                                              monotonicity_,
                                                              forcePositive_,
                                                              false);
                } else {
                    return ConvexMonotoneInterpolation<I1,I2>(xBegin, xEnd,
                                                              yBegin,
                                                              quadraticity_,
                                                              monotonicity_,
                                                              forcePositive_,
                                                              true);
                }
            }

            ConvexMonotoneInterpolation<I1,I2> interp(prevInterpolation);
            if (length == finalSize) {
                return ConvexMonotoneInterpolation<I1,I2>(
                                                 xBegin, xEnd, yBegin,
                                                 quadraticity_,
                                                 monotonicity_,
                                                 forcePositive_,
                                                 false,
                                                 interp.getExistingHelpers());
            } else {
                return ConvexMonotoneInterpolation<I1,I2>(
                                                 xBegin, xEnd, yBegin,
                                                 quadraticity_,
                                                 monotonicity_,
                                                 forcePositive_,
                                                 true,
                                                 interp.getExistingHelpers());
            }
        }
      private:
        Real quadraticity_, monotonicity_;
        bool forcePositive_;
    };


    namespace detail {

        class SectionHelper {
          public:
            virtual ~SectionHelper() = default;
            virtual Real value(Real x) const = 0;
            virtual Real primitive(Real x) const = 0;
            virtual Real fNext() const = 0;
        };

        //the first value in the y-vector is ignored.
        template <class I1, class I2>
        class ConvexMonotoneImpl final : public Interpolation::templateI
