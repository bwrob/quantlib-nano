onst;

        Time time(const Date&) const override;

      private:
        Handle<YieldTermStructure> riskFreeRate_, dividendYield_;
        Handle<Quote> s0_;
        Real v0_, omega_, alpha_, beta_, gamma_, lambda_, daysPerYear_;
        Discretization discretization_;
    };

}


#endif