al y, Real marketOpenFraction) :
            GarmanKlassOpenClose<GarmanKlassSimpleSigma>(y,
                                                         marketOpenFraction,
                                                         0.5) {};
    };


    class ParkinsonSigma :
        public GarmanKlassAbstract {
    public:
        ParkinsonSigma(Real y) :
            GarmanKlassAbstract(y) {};
    protected:
      Real calculatePoint(const IntervalPrice& p) override {
          Real u = std::log(p.high() / p.open());
          Real d = std::log(p.low() / p.open());
          return (u - d) * (u - d) / 4.0 / std::log(2.0);
      }
    };


    class GarmanKlassSigma3 :
        public GarmanKlassOpenClose<ParkinsonSigma> {
    public:
        GarmanKlassSigma3(Real y, Real marketOpenFraction) :
            GarmanKlassOpenClose<ParkinsonSigma>(y,
                                                 marketOpenFraction,
                                                 0.17) {};
    };



    class GarmanKlassSigma4 :
        public GarmanKlassAbstract {
    public:
        GarmanKlassSigma4(Real y) :
            GarmanKlassAbstract(y) {};
    protected:
      Real calculatePoint(const IntervalPrice& p) override {
          Real u = std::log(p.high() / p.open());
          Real d = std::log(p.low() / p.open());
          Real c = std::log(p.close() / p.open());
          return 0.511 * (u - d) * (u - d) - 0.019 * (c * (u + d) - 2 * u * d) - 0.383 * c * c;
      }
    };

    class GarmanKlassSigma5 :
        public GarmanKlassAbstract {
    public:
        GarmanKlassSigma5(Real y) :
            GarmanKlassAbstract(y) {};
    protected:
      Real calculatePoint(const IntervalPrice& p) override {
          Real u = std::log(p.high() / p.open());
          Real d = std::log(p.low() / p.open());
          Real c = std::log(p.close() / p.open());
          return 0.5 * (u - d) * (u - d) - (2.0 * std::log(2.0) - 1.0) * c * c;
      }
    };

    class GarmanKlassSigma6 :
        public GarmanKlassOpenClose<GarmanKlassSigma4> {
    public:
        GarmanKlassSigma6(Real y, Real marketOpenFraction) :
        GarmanKlassOpenClose<GarmanKlassSigma4>(y,
                                                marketOpenFraction,
                                                0.012) {};
    };
}


#endif
