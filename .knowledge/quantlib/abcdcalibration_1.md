 private:
        // optimization method used for fitting
        mutable EndCriteria::Type abcdEndCriteria_;
        ext::shared_ptr<EndCriteria> endCriteria_;
        ext::shared_ptr<OptimizationMethod> optMethod_;
        mutable std::vector<Real> weights_;
        bool vegaWeighted_;
        //! Parameters
        std::vector<Real> times_, blackVols_;
    };

}

#endif