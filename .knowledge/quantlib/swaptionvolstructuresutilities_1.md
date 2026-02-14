ors.options[0] = Period(1, Years);
            tenors.options[1] = Period(10, Years);
            tenors.options[2] = Period(30, Years);
            tenors.swaps.resize(3);
            tenors.swaps[0] = Period(2, Years);
            tenors.swaps[1] = Period(10, Years);
            tenors.swaps[2] = Period(30, Years);
            strikeSpreads.resize(5);
            strikeSpreads[0] = -0.020;
            strikeSpreads[1] = -0.005;
            strikeSpreads[2] = +0.000;
            strikeSpreads[3] = +0.005;
            strikeSpreads[4] = +0.020;
            volSpreads = Matrix(tenors.options.size()*tenors.swaps.size(), strikeSpreads.size());
            volSpreads[0][0] = 0.0599; volSpreads[0][1] = 0.0049;
            volSpreads[0][2] = 0.0000;
            volSpreads[0][3] =-0.0001; volSpreads[0][4] = 0.0127;
            volSpreads[1][0] = 0.0729; volSpreads[1][1] = 0.0086;
            volSpreads[1][2] = 0.0000;
            volSpreads[1][3] =-0.0024; volSpreads[1][4] = 0.0098;
            volSpreads[2][0] = 0.0738; volSpreads[2][1] = 0.0102;
            volSpreads[2][2] = 0.0000;
            volSpreads[2][3] =-0.0039; volSpreads[2][4] = 0.0065;
            volSpreads[3][0] = 0.0465; volSpreads[3][1] = 0.0063;
            volSpreads[3][2] = 0.0000;
            volSpreads[3][3] =-0.0032; volSpreads[3][4] =-0.0010;
            volSpreads[4][0] = 0.0558; volSpreads[4][1] = 0.0084;
            volSpreads[4][2] = 0.0000;
            volSpreads[4][3] =-0.0050; volSpreads[4][4] =-0.0057;
            volSpreads[5][0] = 0.0576; volSpreads[5][1] = 0.0083;
            volSpreads[5][2] = 0.0000;
            volSpreads[5][3] =-0.0043; volSpreads[5][4] = -0.0014;
            volSpreads[6][0] = 0.0437; volSpreads[6][1] = 0.0059;
            volSpreads[6][2] = 0.0000;
            volSpreads[6][3] =-0.0030; volSpreads[6][4] =-0.0006;
            volSpreads[7][0] = 0.0533; volSpreads[7][1] = 0.0078;
            volSpreads[7][2] = 0.0000;
            volSpreads[7][3] =-0.0045; volSpreads[7][4] =-0.0046;
            volSpreads[8][0] = 0.0545; volSpreads[8][1] = 0.0079;
            volSpreads[8][2] = 0.0000;
            volSpreads[8][3] =-0.0042; volSpreads[8][4] =-0.0020;
            volSpreadsHandle = std::vector<std::vector<Handle<Quote> > >(tenors.options.size()*tenors.swaps.size());
            for (Size i=0; i<tenors.options.size()*tenors.swaps.size(); i++){
                volSpreadsHandle[i] = std::vector<Handle<Quote> >(strikeSpreads.size());
                for (Size j=0; j<strikeSpreads.size(); j++) {
                    // every handle must be reassigned, as the ones created by
                    // default are all linked together.
                    volSpreadsHandle[i][j] = Handle<Quote>(ext::shared_ptr<Quote>(new
                        SimpleQuote(volSpreads[i][j])));
                }
            }
        };
    };


 /*   static void setupCubeUtilities() {
        conventions_.calendar = TARGET();
        conventions_.optionBdc = Following;
        conventions_.dayCounter = Actual365Fixed();
        atm_.setMarketData();
        cube_.setMarketData();
        atmVolMatrix_ = RelinkableHandle<SwaptionVolatilityStructure>(
            ext::shared_ptr<SwaptionVolatilityStructure>(new
                SwaptionVolatilityMatrix(conventions_.calendar,
                                         atm_.tenors.options,
                                         atm_.tenors.swaps,
                                         atm_.volsHandle,
                                         conventions_.dayCounter,
                                         conventions_.optionBdc)));
    }*/

}

#endif
