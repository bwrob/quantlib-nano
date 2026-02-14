  : public YoYInflationCapFloorEngine {
      public:
        YoYInflationBachelierCapFloorEngine(
                    const ext::shared_ptr<YoYInflationIndex>&,
                    const Handle<YoYOptionletVolatilitySurface>& vol,
                    const Handle<YieldTermStructure>& nominalTermStructure);
      protected:
        Real
        optionletImpl(Option::Type, Real strike, Real forward, Real stdDev, Real d) const override;
    };

}

#endif
