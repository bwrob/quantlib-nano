        }
        //! \name Inspectors
        //@{
        Real a() const { return coeffs().a_; }
        Real b() const { return coeffs().b_; }
        Real c() const { return coeffs().c_; }
        Real d() const { return coeffs().d_; }
        std::vector<Real> k() const { return coeffs().k_; }
        Real rmsError() const { return coeffs().error_; }
        Real maxError() const { return coeffs().maxError_; }
        EndCriteria::Type endCriteria(){ return coeffs().abcdEndCriteria_; }
        template <class I1>
        Real k(Time t, const I1& xBegin, const I1& xEnd) const {
            LinearInterpolation li(xBegin, xEnd, (coeffs().k_).begin());
            return li(t);
        }
      private:
        const detail::AbcdCoeffHolder& coeffs() const {
          return *dynamic_cast<detail::AbcdCoeffHolder*>(impl_.get());
        }
    };

    //! %Abcd interpolation factory and traits
    /*! \ingroup interpolations */
    class Abcd {
      public:
        Abcd(Real a,
             Real b,
             Real c,
             Real d,
             bool aIsFixed,
             bool bIsFixed,
             bool cIsFixed,
             bool dIsFixed,
             bool vegaWeighted = false,
             ext::shared_ptr<EndCriteria> endCriteria = ext::shared_ptr<EndCriteria>(),
             ext::shared_ptr<OptimizationMethod> optMethod = ext::shared_ptr<OptimizationMethod>())
        : a_(a), b_(b), c_(c), d_(d), aIsFixed_(aIsFixed), bIsFixed_(bIsFixed), cIsFixed_(cIsFixed),
          dIsFixed_(dIsFixed), vegaWeighted_(vegaWeighted), endCriteria_(std::move(endCriteria)),
          optMethod_(std::move(optMethod)) {}
        template <class I1, class I2>
        Interpolation interpolate(const I1& xBegin, const I1& xEnd,
                                  const I2& yBegin) const {
            return AbcdInterpolation(xBegin, xEnd, yBegin,
                                     a_, b_, c_, d_,
                                     aIsFixed_, bIsFixed_,
                                     cIsFixed_, dIsFixed_,
                                     vegaWeighted_,
                                     endCriteria_, optMethod_);
        }
        static const bool global = true;
      private:
        Real a_, b_, c_, d_;
        bool aIsFixed_, bIsFixed_, cIsFixed_, dIsFixed_;
        bool vegaWeighted_;
        const ext::shared_ptr<EndCriteria> endCriteria_;
        const ext::shared_ptr<OptimizationMethod> optMethod_;
    };

}

#endif
