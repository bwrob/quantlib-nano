st Real c5_;
        static const Real c6_;
        static const Real c7_;
        static const Real c8_;
    };

    //! Maddock's Inverse cumulative normal distribution class
    /*! Given x between zero and one as
        the integral value of a gaussian normal distribution
        this class provides the value y such that
        formula here ...

        From the boost documentation:
         These functions use a rational approximation devised by
         John Maddock to calculate an initial approximation to the
         result that is accurate to ~10^-19, then only if that has
         insufficient accuracy compared to the epsilon for type double,
         do we clean up the result using Halley iteration.
    */
    class MaddockInverseCumulativeNormal {
      public:
        MaddockInverseCumulativeNormal(Real average = 0.0,
                                       Real sigma   = 1.0);
        Real operator()(Real x) const;

      private:
        const Real average_, sigma_;
    };

    //! Maddock's cumulative normal distribution class
    class MaddockCumulativeNormal {
      public:
        MaddockCumulativeNormal(Real average = 0.0,
                                       Real sigma   = 1.0);
        Real operator()(Real x) const;

      private:
        const Real average_, sigma_;
    };


    // inline definitions

    inline NormalDistribution::NormalDistribution(Real average,
                                                  Real sigma)
    : average_(average), sigma_(sigma) {

        QL_REQUIRE(sigma_>0.0,
                   "sigma must be greater than 0.0 ("
                   << sigma_ << " not allowed)");

        normalizationFactor_ = M_SQRT_2*M_1_SQRTPI/sigma_;
        derNormalizationFactor_ = sigma_*sigma_;
        denominator_ = 2.0*derNormalizationFactor_;
    }

    inline Real NormalDistribution::operator()(Real x) const {
        Real deltax = x-average_;
        Real exponent = -(deltax*deltax)/denominator_;
        // debian alpha had some strange problem in the very-low range
        return exponent <= -690.0 ? 0.0 :  // exp(x) < 1.0e-300 anyway
            Real(normalizationFactor_*std::exp(exponent));
    }

    inline Real NormalDistribution::derivative(Real x) const {
        return ((*this)(x) * (average_ - x)) / derNormalizationFactor_;
    }

    inline CumulativeNormalDistribution::CumulativeNormalDistribution(
                                                 Real average, Real sigma)
    : average_(average), sigma_(sigma) {

        QL_REQUIRE(sigma_>0.0,
                   "sigma must be greater than 0.0 ("
                   << sigma_ << " not allowed)");
    }

    inline Real CumulativeNormalDistribution::derivative(Real x) const {
        Real xn = (x - average_) / sigma_;
        return gaussian_(xn) / sigma_;
    }

    inline InverseCumulativeNormal::InverseCumulativeNormal(
                                                 Real average, Real sigma)
    : average_(average), sigma_(sigma) {

        QL_REQUIRE(sigma_>0.0,
                   "sigma must be greater than 0.0 ("
                   << sigma_ << " not allowed)");
    }

    inline MoroInverseCumulativeNormal::MoroInverseCumulativeNormal(
                                                 Real average, Real sigma)
    : average_(average), sigma_(sigma) {

        QL_REQUIRE(sigma_>0.0,
                   "sigma must be greater than 0.0 ("
                   << sigma_ << " not allowed)");
    }

}


#endif
