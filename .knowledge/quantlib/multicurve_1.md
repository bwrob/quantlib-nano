dBootstrappedCurve(RelinkableHandle<YieldTermStructure>& internalHandle,
                             ext::shared_ptr<YieldTermStructure>&& curve);

        Handle<YieldTermStructure>
        addNonBootstrappedCurve(RelinkableHandle<YieldTermStructure>& internalHandle,
                                ext::shared_ptr<YieldTermStructure>&& curve);

      private:
        Handle<YieldTermStructure> addCurve(RelinkableHandle<YieldTermStructure>& internalHandle,
                                            ext::shared_ptr<YieldTermStructure>&& curve);
        void update() override;
        ext::shared_ptr<MultiCurveBootstrap> multiCurveBootstrap_;
        std::vector<ext::shared_ptr<YieldTermStructure>> curves_;
    };
}

#endif