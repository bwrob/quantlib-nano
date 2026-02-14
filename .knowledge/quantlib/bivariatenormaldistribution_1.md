(Real a, Real b) const;
      private:
        Real correlation_;
        CumulativeNormalDistribution cumnorm_;
    };

    //! default bivariate implementation
    typedef BivariateCumulativeNormalDistributionWe04DP
                                        BivariateCumulativeNormalDistribution;

}


#endif