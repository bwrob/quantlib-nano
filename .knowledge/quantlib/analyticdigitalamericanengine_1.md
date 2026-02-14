           &engine):
        AnalyticDigitalAmericanEngine(engine) {}
        bool knock_in() const override { return false; }
    };

}


#endif
