ower_[i] || newPoint[i] > upper_[i]){
					if(newPoint[i] < lower_[i]){
						newPoint[i] = upper_[i] + newPoint[i] - lower_[i];
					} else {
						newPoint[i] = lower_[i] + newPoint[i] - upper_[i];
					}
				} 
            }
        };
    private:
        std::mt19937 generator_;
        std::normal_distribution<Real> distribution_;
        Array lower_, upper_;
    };
    
    //! Gaussian Mirror Sampler
    /*! Sample from normal distribution, but constrained to lie within
     * .boundaries. If the value ends up beyond the boundary, the value
     * is reflected back.
    */
    class SamplerMirrorGaussian
    {
    public:
      SamplerMirrorGaussian(Array lower,
                            Array upper,
                            unsigned long seed = SeedGenerator::instance().get())
      : generator_(seed), distribution_(0.0, 1.0),
        lower_(std::move(lower)), upper_(std::move(upper)){};

        void operator()(Array &newPoint, const Array &currentPoint, const Array &temp) {
            QL_REQUIRE(newPoint.size() == currentPoint.size(), "Incompatible input");
            QL_REQUIRE(newPoint.size() == temp.size(), "Incompatible input");
            for (Size i = 0; i < currentPoint.size(); i++){
                newPoint[i] = currentPoint[i] + std::sqrt(temp[i]) * distribution_(generator_);
                while(newPoint[i] < lower_[i] || newPoint[i] > upper_[i]){
					if(newPoint[i] < lower_[i]){
						newPoint[i] = lower_[i] + lower_[i] - newPoint[i];
					} else {
						newPoint[i] = upper_[i] + upper_[i] - newPoint[i];
					}
				}
            }
        };
    private:
        std::mt19937 generator_;
        std::normal_distribution<Real> distribution_;
        Array lower_, upper_;
    };

    //! Cauchy Sampler
    /*!    Sample from cauchy distribution. This means that the parameter space
    must have support on the positive whole real line. For lower dimensions
    it could be faster than the Gaussian sampler, specially when combined
    with the Cauchy temperature.
    */
    class SamplerCauchy
    {
    public:
        explicit SamplerCauchy(unsigned long seed = SeedGenerator::instance().get()) :
            generator_(seed), distribution_(0.0, 1.0) {};

        void operator()(Array &newPoint, const Array &currentPoint, const Array &temp) {
            QL_REQUIRE(newPoint.size() == currentPoint.size(), "Incompatible input");
            QL_REQUIRE(newPoint.size() == temp.size(), "Incompatible input");
            for (Size i = 0; i < currentPoint.size(); i++)
                newPoint[i] = currentPoint[i] + temp[i] * distribution_(generator_);
        };
    protected:
        std::mt19937 generator_;
        std::cauchy_distribution<Real> distribution_;
    };

    //! Very Fast Annealing Sampler
    /*!    For consistency should be used with TemperatureVeryFastAnnealing.
    Requires that the parameter space be bounded above and below.
    */
    class SamplerVeryFastAnnealing
    {
    public:
      SamplerVeryFastAnnealing(Array lower,
                               Array upper,
                               unsigned long seed = SeedGenerator::instance().get())
        : lower_(std::move(lower)), upper_(std::move(upper)), generator_(seed) {
            QL_REQUIRE(lower_.size() == upper_.size(), "Incompatible input");
        };

        void operator()(Array &newPoint, const Array &currentPoint, const Array &temp) {
            QL_REQUIRE(newPoint.size() == currentPoint.size(), "Incompatible input");
            QL_REQUIRE(newPoint.size() == lower_.size(), "Incompatible input");
            QL_REQUIRE(newPoint.size() == temp.size(), "Incompatible input");
            for (Size i = 0; i < currentPoint.size(); i++) {
                newPoint[i] = lower_[i] - 1.0;
                while (newPoint[i] < lower_[i] || newPoint[i] > upper_[i]) {
                    Real draw = distribution_(generator_);
                    Real sign = static_cast<int>(0.5 < draw) - static_cast<int>(draw < 0.5);
         