vate:
        SobolBrownianGenerator::Ordering ordering_;
        unsigned long seed_;
        SobolRsg::DirectionIntegers integers_;
    };

    class Burley2020SobolBrownianGenerator : public SobolBrownianGeneratorBase {
      public:
        Burley2020SobolBrownianGenerator(
            Size factors,
            Size steps,
            Ordering ordering,
            unsigned long seed = 42,
            SobolRsg::DirectionIntegers directionIntegers = SobolRsg::Jaeckel,
            unsigned long scrambleSeed = 43);

      private:
        const Burley2020SobolRsg::sample_type& nextSequence() override;
        InverseCumulativeRsg<Burley2020SobolRsg, InverseCumulativeNormal> generator_;
    };

    class Burley2020SobolBrownianGeneratorFactory : public BrownianGeneratorFactory {
      public:
        explicit Burley2020SobolBrownianGeneratorFactory(
            SobolBrownianGenerator::Ordering ordering,
            unsigned long seed = 42,
            SobolRsg::DirectionIntegers directionIntegers = SobolRsg::Jaeckel,
            unsigned long scrambleSeed = 43);
        ext::shared_ptr<BrownianGenerator> create(Size factors, Size steps) const override;

      private:
        SobolBrownianGenerator::Ordering ordering_;
        unsigned long seed_;
        SobolRsg::DirectionIntegers integers_;
        unsigned long scrambleSeed_;
    };

}


#endif