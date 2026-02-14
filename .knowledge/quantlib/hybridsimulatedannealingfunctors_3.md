tialTemp_(dimension, initialTemp) {}
        void operator()(Array &newTemp, const Array &currTemp, const Array &steps) {
            QL_REQUIRE(currTemp.size() == initialTemp_.size(), "Incompatible input");
            QL_REQUIRE(currTemp.size() == newTemp.size(), "Incompatible input");
            for (Size i = 0; i < initialTemp_.size(); i++)
                newTemp[i] = initialTemp_[i] / std::pow(steps[i], inverseN_);
        }
    private:
        Real inverseN_;
        Array initialTemp_;
    };

    class TemperatureExponential {
    public:
        TemperatureExponential(Real initialTemp, Size dimension, Real power = 0.95)
            : initialTemp_(dimension, initialTemp), power_(power) {}
        void operator()(Array &newTemp, const Array &currTemp, const Array &steps) {
            QL_REQUIRE(currTemp.size() == initialTemp_.size(), "Incompatible input");
            QL_REQUIRE(currTemp.size() == newTemp.size(), "Incompatible input");
            for (Size i = 0; i < initialTemp_.size(); i++)
                newTemp[i] = initialTemp_[i] * std::pow(power_, steps[i]);
        }
    private:
        Array initialTemp_;
        Real power_;
    };
    //! Temperature Very Fast Annealing
    /*!    For use with the Very Fast Annealing sampler
    */
    class TemperatureVeryFastAnnealing {
    public:
        TemperatureVeryFastAnnealing(Real initialTemp, Real finalTemp, Real maxSteps, Size dimension)
            :inverseN_(1.0 / dimension), initialTemp_(dimension, initialTemp),
            finalTemp_(dimension, finalTemp), exponent_(dimension, 0.0) {
            Real coeff = std::pow(maxSteps, -inverseN_);
            for (Size i = 0; i < initialTemp_.size(); i++)
                exponent_[i] = -std::log(finalTemp_[i] / initialTemp_[i])*coeff;
        }
        void operator()(Array &newTemp, const Array &currTemp, const Array &steps) {
            QL_REQUIRE(currTemp.size() == initialTemp_.size(), "Incompatible input");
            QL_REQUIRE(currTemp.size() == newTemp.size(), "Incompatible input");
            for (Size i = 0; i < initialTemp_.size(); i++)
                newTemp[i] = initialTemp_[i] * exp(-exponent_[i] * std::pow(steps[i], inverseN_));
        }
    private:
        Real inverseN_;
        Array initialTemp_, finalTemp_, exponent_;
    };
    //! Reannealing Trivial
    /*!    No reannealing is performed
    */
    struct ReannealingTrivial {
        ReannealingTrivial() = default;
        ;
        void setProblem(Problem &P) {};
        void operator()(Array & steps, const Array &currentPoint,
            Real aCurrentValue, const Array & currTemp) {};
    };
    //! Reannealing Finite Difference
    /*!    In multidimensional problems, different dimensions might have different
    sensitivities, and might have dimensions on which the solution is rather
    insensitive. If possible, the search should concentrate more on the more
    sensitive dimensions, therefore a reannealing schedule might raise the
    temperature seen by those more fruitful dimensions so as to allow for more
    movement along the dimensions of interest
    */
    class ReannealingFiniteDifferences {
    public:
      ReannealingFiniteDifferences(Real initialTemp,
                                   Size dimension,
                                   const Array& lower = Array(),
                                   const Array& upper = Array(),
                                   Real stepSize = 1e-7,
                                   Real minSize = 1e-10,
                                   Real functionTol = 1e-10)
      : stepSize_(stepSize), minSize_(minSize), functionTol_(functionTol), N_(dimension),
        lower_(lower), upper_(upper), initialTemp_(dimension, initialTemp),
        bounded_(dimension, 1.0) {
          if (!lower.empty() && !upper.empty()) {
              QL_REQUIRE(lower.size() == N_, "Incompatible input");
              QL_REQUIRE(upper.size() == N_, "Incompatible input");
              bound_ = true;

