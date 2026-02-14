 k2++)
                        result[k2] = tmpBound[j];
                }
                return result;
            }

          private:
            const std::vector<Parameter>& arguments_;
        };
      public:
        explicit PrivateConstraint(const std::vector<Parameter>& arguments)
        : Constraint(ext::shared_ptr<Constraint::Impl>(
                                   new PrivateConstraint::Impl(arguments))) {}
    };

}

#endif