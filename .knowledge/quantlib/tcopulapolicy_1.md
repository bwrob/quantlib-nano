back());
        }
        /*! Probability density of a given realization of values of the systemic
          factors (remember they are independent).
          Intended to be used in numerical integration of an arbitrary function 
          depending on those values.
        */
        Probability density(const std::vector<Real>& m) const {
    #if defined(QL_EXTRA_SAFETY_CHECKS)
            QL_REQUIRE(m.size() == distributions_.size()-1, 
                "Incompatible sample and latent model sizes");
    #endif
            Real prodDensities = 1.;
            for(Size i=0; i<m.size(); i++) 
                prodDensities *= boost::math::pdf(distributions_[i], 
                    m[i] /varianceFactors_[i]) /varianceFactors_[i];
                 // accumulate lambda
            return prodDensities;
        }
        /*! Returns the inverse of the cumulative distribution of the (modelled) 
          latent variable (as indexed by iVariable). Involves the convolution
          of the factors' distributions.
        */
        Real inverseCumulativeY(Probability p, Size iVariable) const {
    #if defined(QL_EXTRA_SAFETY_CHECKS)
            QL_REQUIRE(iVariable < latentVarsCumul_.size(), 
                "Latent variable index out of bounds.");
    #endif
            return latentVarsInverters_[iVariable](p);
        }
        /*! Returns the inverse of the cumulative distribution of the 
        idiosincratic factor. The LM here is limited to all idiosincratic 
        factors following the same distribution.
        */
        Real inverseCumulativeZ(Probability p) const {
            return boost::math::quantile(distributions_.back(), p)
                * varianceFactors_.back();
        }
        /*! Returns the inverse of the cumulative distribution of the 
          systemic factor iFactor.
        */
        Real inverseCumulativeDensity(Probability p, Size iFactor) const {
    #if defined(QL_EXTRA_SAFETY_CHECKS)
            QL_REQUIRE(iFactor < distributions_.size()-1, 
                "Random factor variable index out of bounds.");
    #endif
            return boost::math::quantile(distributions_[iFactor], p)
                * varianceFactors_[iFactor];
        }
        //to use this (by default) version, the generator must be a uniform one.
        std::vector<Real> allFactorCumulInverter(const std::vector<Real>& probs) const;
    private:
        mutable std::vector<boost::math::students_t_distribution<Real> > distributions_;
        mutable std::vector<Real> varianceFactors_;
        mutable std::vector<CumulativeBehrensFisher> latentVarsCumul_;
        mutable std::vector<InverseCumulativeBehrensFisher> latentVarsInverters_;
    };

}

#endif