_ / (1 + this->u_ * this->u_); }
        mp_real m1() const override {
            return 2*this->u_ / squared(1 + this->u_*this->u_);
        }

      private:
        const Real m0_;
    };
}

#endif