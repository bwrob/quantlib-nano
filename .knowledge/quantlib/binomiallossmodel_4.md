1.) return dist.rbegin()->first;
        if(perc == 0.) return dist.begin()->first;
        auto itdist = dist.begin();
        while (itdist->second <= perc) ++itdist;
        Real valPlus = itdist->second;
        Real xPlus   = itdist->first;
        --itdist; //we're never 1st or last, because of tests above
        Real valMin  = itdist->second;
        Real xMin    = itdist->first;

        Real portfLoss = xPlus-(xPlus-xMin)*(valPlus-perc)/(valPlus-valMin);

        return 
            std::min(std::max(portfLoss - attachAmount_, 0.), 
                detachAmount_ - attachAmount_);
    }

    template< class LLM>
    Real BinomialLossModel<LLM>::expectedShortfall(const Date&d, 
        Real perctl) const 
    {
        //taken from recursive since we have the distribution in both cases.
        if(d == Settings::instance().evaluationDate()) return 0.;
            std::map<Real, Probability> distrib = lossDistribution(d);

            std::map<Real, Probability>::iterator 
                itNxt, itDist = distrib.begin();
            for(; itDist != distrib.end(); ++itDist)
                if(itDist->second >= perctl) break;
            itNxt = itDist;
            --itDist;

            // \todo: I could linearly triangulate the exact point and get 
            //    extra precission on the first(broken) period.
            if(itNxt != distrib.end()) { 
                Real lossNxt = std::min(std::max(itNxt->first - attachAmount_, 
                    0.), detachAmount_ - attachAmount_);
                Real lossHere = std::min(std::max(itDist->first - attachAmount_,
                    0.), detachAmount_ - attachAmount_);

                Real val =  lossNxt - (itNxt->second - perctl) * 
                    (lossNxt - lossHere) / (itNxt->second - itDist->second); 
                Real suma = (itNxt->second - perctl) * (lossNxt + val) * .5;
                ++itDist; ++itNxt;
                do{
                    lossNxt = std::min(std::max(itNxt->first - attachAmount_, 
                        0.), detachAmount_ - attachAmount_);
                    lossHere = std::min(std::max(itDist->first - attachAmount_, 
                        0.), detachAmount_ - attachAmount_);
                    suma += .5 * (lossHere + lossNxt) 
                        * (itNxt->second - itDist->second);
                    ++itDist; ++itNxt;
                }while(itNxt != distrib.end());
                return suma / (1.-perctl);
            }
            QL_FAIL("Binomial model fails to calculate ESF.");
    }

    // The standard use:
    typedef BinomialLossModel<GaussianConstantLossLM> GaussianBinomialLossModel;
    typedef BinomialLossModel<TConstantLossLM> TBinomialLossModel;

}

#endif