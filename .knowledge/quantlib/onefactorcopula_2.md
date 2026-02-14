ribution integral(const F& f,
                              const std::vector<Real>& nominals,
                              const std::vector<Real>& probabilities) const {
            calculate();

            Distribution dist(f.buckets(), 0.0, f.maximum());
            for (Size i = 0; i < steps(); i++) {
                std::vector<Real> conditional
                    = conditionalProbability(probabilities, m(i));
                Distribution d = f(nominals, conditional);
                for (Size j = 0; j < dist.size(); j++)
                    dist.addDensity(j, d.density(j) * densitydm(i));
            }
            return dist;
        }

        /*! Check moments (unit norm, zero mean and unit variance) of
            the distributions of M, Z, and Y by numerically
            integrating the respective density.  Parameter tolerance
            is the maximum tolerable absolute error.
        */
        int checkMoments(Real tolerance) const;

      protected:
        Handle<Quote> correlation_;
        mutable Real max_;
        mutable Size steps_;
        mutable Real min_;

        // Tabulated numerical solution of the cumulated distribution of Y
        mutable std::vector<Real> y_;
        mutable std::vector<Real> cumulativeY_;

        //private:
        // utilities for simple Euler integrations over the density of M
        Size steps() const;

        // i not used yet, might allow varying grid size
        // for the copula integration in the future
        Real dm(Size i) const;

        Real m(Size i) const;
        Real densitydm(Size i) const;
    };

    inline Real OneFactorCopula::correlation() const {
        calculate();
        return correlation_->value();
    }

    inline Size OneFactorCopula::steps() const {
        return steps_;
    }

    inline Real OneFactorCopula::dm(Size) const {
        return (max_ - min_)/ steps_;
    }

    inline Real OneFactorCopula::m(Size i) const {
        QL_REQUIRE(i < steps_, "index out of range");
        return min_ + dm(i) * i + dm(i) / 2;
    }

    inline Real OneFactorCopula::densitydm(Size i) const {
        QL_REQUIRE(i < steps_, "index out of range");
        return density(m(i)) * dm(i);
    }

}

#endif