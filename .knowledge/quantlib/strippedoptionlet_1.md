etAtmRates_;
        std::vector<std::vector<Rate> > optionletStrikes_;

        std::vector<std::vector<Handle<Quote> > > optionletVolQuotes_;
        mutable std::vector<std::vector<Volatility> > optionletVolatilities_;
    };

}

#endif