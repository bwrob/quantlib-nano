    bool inheritedVolatilityType_;
        VolatilityType volType_;
        Real shift1_, shift2_;

        mutable Real phi_, a_, b_, s1_, s2_, m1_, m2_, v1_, v2_, k_;
        mutable Real alpha_, psi_;
        mutable Option::Type optionType_;

        ext::shared_ptr<CmsCoupon> c1_, c2_;
    };
}

#endif
