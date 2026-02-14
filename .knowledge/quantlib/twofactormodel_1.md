xt::shared_ptr<ShortRateDynamics>& dynamics);

        DiscountFactor discount(Size i, Size index) const {
            Size modulo = tree1_->size(i);
            Size index1 = index % modulo;
            Size index2 = index / modulo;

            Real x = tree1_->underlying(i, index1);
            Real y = tree2_->underlying(i, index2);

            Rate r = dynamics_->shortRate(timeGrid()[i], x, y);
            return std::exp(-r*timeGrid().dt(i));
        }
      private:
        ext::shared_ptr<ShortRateDynamics> dynamics_;
    };

}


#endif