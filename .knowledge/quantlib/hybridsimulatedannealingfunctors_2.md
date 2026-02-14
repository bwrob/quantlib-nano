           Real y = sign*temp[i] * (std::pow(1.0 + 1.0 / temp[i],
                                                      std::abs(2 * draw - 1.0)) - 1.0);
                    newPoint[i] = currentPoint[i] + y*(upper_[i] - lower_[i]);
                }
            }
        };
    private:
        Array lower_, upper_;
        std::mt19937 generator_;
        std::uniform_real_distribution<Real> distribution_;
    };

    //! Always Downhill Probability
    /*!    Only points that improve on the current solution are accepted.
    Depending on the problem, this makes it very unlikely that the
    optimizer will be able to escape a local optimum.
    */
    struct ProbabilityAlwaysDownhill {
        bool operator()(Real currentValue, Real newValue, const Array &temp) {
            return currentValue > newValue; //return true if new value is lower than old value
        }
    };

    //! Boltzmann Probability
    /*!    The probability of accepting a new point is sampled from a Boltzmann distribution.
    A point is accepted if \f$ \frac{1}{1+exp(-(current-new)/T)} > u \f$
    where \f$ u \f$ is drawn from a uniform distribution.
    */
    class ProbabilityBoltzmann {
    public:
        explicit ProbabilityBoltzmann(unsigned long seed = SeedGenerator::instance().get()) : generator_(seed) {};

        bool operator()(Real currentValue, Real newValue, const Array &temp) {
            Real temperature = *std::max_element(temp.begin(), temp.end());
            return (1.0 / (1.0 + exp((newValue - currentValue) / temperature))) > distribution_(generator_);
        }
    private:
        std::mt19937 generator_;
        std::uniform_real_distribution<Real> distribution_;
    };
    //! Boltzmann Downhill Probability
    /*!    Similarly to the Boltzmann Probability, but if new < current, then the point is
    always accepted.
    */
    class ProbabilityBoltzmannDownhill
    {
    public:
        explicit ProbabilityBoltzmannDownhill(unsigned long seed = SeedGenerator::instance().get()) : generator_(seed) {};

        bool operator()(Real currentValue, Real newValue, const Array &temp) {
            if (newValue < currentValue)
                return true;
            Real mTemperature = *std::max_element(temp.begin(), temp.end());
            return (1.0 / (1.0 + exp((newValue - currentValue) / mTemperature))) > distribution_(generator_);
        }
    private:
        std::mt19937 generator_;
        std::uniform_real_distribution<Real> distribution_;
    };
    //! Temperature Boltzmann
    /*!    For use with the Gaussian sampler
    */
    class TemperatureBoltzmann {
    public:
        TemperatureBoltzmann(Real initialTemp, Size dimension)
            : initialTemp_(dimension, initialTemp) {}
        void operator()(Array &newTemp, const Array &currTemp, const Array &steps) {
            QL_REQUIRE(currTemp.size() == initialTemp_.size(), "Incompatible input");
            QL_REQUIRE(currTemp.size() == newTemp.size(), "Incompatible input");
            for (Size i = 0; i < initialTemp_.size(); i++)
                newTemp[i] = initialTemp_[i] / std::log(steps[i]);
        }
    private:
        Array initialTemp_;
    };
    //! Temperature Cauchy
    /*!    For use with the Cauchy sampler
    */
    class TemperatureCauchy {
    public:
        TemperatureCauchy(Real initialTemp, Size dimension)
            : initialTemp_(dimension, initialTemp) {}
        void operator()(Array &newTemp, const Array &currTemp, const Array &steps) {
            QL_REQUIRE(currTemp.size() == initialTemp_.size(), "Incompatible input");
            QL_REQUIRE(currTemp.size() == newTemp.size(), "Incompatible input");
            for (Size i = 0; i < initialTemp_.size(); i++)
                newTemp[i] = initialTemp_[i] / steps[i];
        }
    private:
        Array initialTemp_;
    };

    class TemperatureCauchy1D {
    public:
        TemperatureCauchy1D(Real initialTemp, Size dimension) :
            inverseN_(1.0 / dimension),
            ini