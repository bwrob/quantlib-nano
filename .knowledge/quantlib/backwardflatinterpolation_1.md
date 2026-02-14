];
                return primitive_[i] + dx*this->yBegin_[i+1];
            }
            Real derivative(Real) const override { return 0.0; }
            Real secondDerivative(Real) const override { return 0.0; }

          private:
            std::vector<Real> primitive_;
        };

    }

}

#endif
