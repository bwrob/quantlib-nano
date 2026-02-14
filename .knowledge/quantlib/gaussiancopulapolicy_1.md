        }
        /*! Returns the inverse of the cumulative distribution of the
        idiosyncratic factor (identically distributed for all latent variables)
        */
        Real inverseCumulativeZ(Probability p) const {
            return InverseCumulativeNormal::standard_value(p);
        }
        /*! Returns the inverse of the cumulative distribution of the
          systemic factor iFactor.
        */
        Real inverseCumulativeDensity(Probability p, Size iFactor) const {
            return InverseCumulativeNormal::standard_value(p);
        }
        //!
        //to use this (by default) version, the generator must be a uniform one.
        std::vector<Real> allFactorCumulInverter(const std::vector<Real>& probs) const {
            std::vector<Real> result;
            result.resize(probs.size());
            std::transform(probs.begin(), probs.end(), result.begin(),
                           [&](Real p){ return InverseCumulativeNormal::standard_value(p); });
            return result;
        }
    private:
        mutable Size numFactors_;
        // no op =
        static const NormalDistribution density_;
        static const CumulativeNormalDistribution cumulative_;
    };

}

#endif
