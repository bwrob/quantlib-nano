    EndCriteria::Type endCriteria() const { return shortRateEndCriteria_; }

        //! Returns the problem values
        const Array& problemValues() const { return problemValues_; }

        //! Returns array of arguments on which calibration is done
        Array params() const;

        virtual void setParams(const Array& params);
        Integer functionEvaluation() const { return functionEvaluation_; }

      protected:
        virtual void generateArguments() {}
        std::vector<Parameter> arguments_;
        ext::shared_ptr<Constraint> constraint_;
        EndCriteria::Type shortRateEndCriteria_ = EndCriteria::None;
        Array problemValues_;
        Integer functionEvaluation_;

      private:
        //! Constraint imposed on arguments
        class PrivateConstraint;
        //! Calibration cost function class
        class CalibrationFunction;
    };

    //! Abstract short-rate model class
    /*! \ingroup shortrate */
    class ShortRateModel : public CalibratedModel {
      public:
        explicit ShortRateModel(Size nArguments);
        virtual ext::shared_ptr<Lattice> tree(const TimeGrid&) const = 0;
    };


    // inline definitions


    inline Real AffineModel::discountBondOption(Option::Type type,
                                                Real strike,
                                                Time maturity,
                                                Time,
                                                Time bondMaturity) const {
        return discountBondOption(type, strike, maturity, bondMaturity);
    }

    inline const ext::shared_ptr<Constraint>&
    CalibratedModel::constraint() const {
        return constraint_;
    }

    class CalibratedModel::PrivateConstraint : public Constraint {
      private:
        class Impl final : public Constraint::Impl {
          public:
            explicit Impl(const std::vector<Parameter>& arguments)
            : arguments_(arguments) {}

            bool test(const Array& params) const override {
                Size k=0;
                for (const auto& argument : arguments_) {
                    Size size = argument.size();
                    Array testParams(size);
                    for (Size j=0; j<size; j++, k++)
                        testParams[j] = params[k];
                    if (!argument.testParams(testParams))
                        return false;
                }
                return true;
            }

            Array upperBound(const Array& params) const override {
                Size k = 0, k2 = 0;
                Size totalSize = 0;
                for (const auto& argument : arguments_) {
                    totalSize += argument.size();
                }
                Array result(totalSize);
                for (const auto& argument : arguments_) {
                    Size size = argument.size();
                    Array partialParams(size);
                    for (Size j = 0; j < size; j++, k++)
                        partialParams[j] = params[k];
                    Array tmpBound = argument.constraint().upperBound(partialParams);
                    for (Size j = 0; j < size; j++, k2++)
                        result[k2] = tmpBound[j];
                }
                return result;
            }

            Array lowerBound(const Array& params) const override {
                Size k = 0, k2 = 0;
                Size totalSize = 0;
                for (const auto& argument : arguments_) {
                    totalSize += argument.size();
                }
                Array result(totalSize);
                for (const auto& argument : arguments_) {
                    Size size = argument.size();
                    Array partialParams(size);
                    for (Size j = 0; j < size; j++, k++)
                        partialParams[j] = params[k];
                    Array tmpBound = argument.constraint().lowerBound(partialParams);
                    for (Size j = 0; j < size; j++,