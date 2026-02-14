nst Array&) const override { return low_; }

          private:
            Array low_, high_;
        };
      public:
        NonhomogeneousBoundaryConstraint(const Array& low, const Array& high)
        : Constraint(ext::shared_ptr<Constraint::Impl>(
              new NonhomogeneousBoundaryConstraint::Impl(low, high))) {}
    };

}

#endif
