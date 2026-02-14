explicit TabulatedGaussLegendre(Size n = 20) { order(n); }
        template <class F>
        Real operator() (const F& f) const {
            QL_ASSERT(w_ != nullptr, "Null weights");
            QL_ASSERT(x_ != nullptr, "Null abscissas");
            Size startIdx;
            Real val;

            const Size isOrderOdd = order_ & 1;

            if (isOrderOdd) {
              QL_ASSERT((n_>0), "assume at least 1 point in quadrature");
              val = w_[0]*f(x_[0]);
              startIdx=1;
            } else {
              val = 0.0;
              startIdx=0;
            }

            for (Size i=startIdx; i<n_; ++i) {
                val += w_[i]*f( x_[i]);
                val += w_[i]*f(-x_[i]);
            }
            return val;
        }

        void order(Size);
        Size order() const { return order_; }

      private:
        Size order_;

        const Real* w_;
        const Real* x_;
        Size  n_;

        static const Real w6[3];
        static const Real x6[3];
        static const Size n6;

        static const Real w7[4];
        static const Real x7[4];
        static const Size n7;

        static const Real w12[6];
        static const Real x12[6];
        static const Size n12;

        static const Real w20[10];
        static const Real x20[10];
        static const Size n20;
    };

}

#endif