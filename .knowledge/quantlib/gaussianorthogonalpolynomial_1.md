sianOrthogonalPolynomial {
      public:
        Real mu_0() const override;
        Real alpha(Size i) const override;
        Real beta(Size i) const override;
        Real w(Real x) const override;
    };

}

#endif
