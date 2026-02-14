Buckets_; }
        Real maximum() const override { return maximum_; }

      private:
        Size nBuckets_;
        Real maximum_;
        Size simulations_;
        long seed_;
        Real epsilon_;
    };

}

#endif