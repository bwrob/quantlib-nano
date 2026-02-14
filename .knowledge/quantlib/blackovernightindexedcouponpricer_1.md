iveCap, bool dailyCapFloor) const override;
    private:
        Real optionletRateGlobal(Option::Type optionType, Real effStrike) const;
        Real optionletRateLocal(Option::Type optionType, Real effStrike) const;

        Real gearing_;
        ext::shared_ptr<IborIndex> index_;
        Real swapletRate_, forwardRate_;
    };

}

#endif