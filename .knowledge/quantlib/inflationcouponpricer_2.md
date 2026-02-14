inalTermStructure)
        : YoYInflationCouponPricer(capletVol, nominalTermStructure) {}
      protected:
        Real optionletPriceImp(Option::Type, Real strike, Real forward, Real stdDev) const override;
    };

}


#endif
