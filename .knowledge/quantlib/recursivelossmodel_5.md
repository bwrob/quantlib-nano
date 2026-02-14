   //const Date& date,
        const std::vector<Real>& mktFactor) const 
    {
        std::map<Real, Probability> pIndepDistrib =
            conditionalLossDistrib(pDefDate, mktFactor);

        std::vector<Real> results;
        auto distIt = pIndepDistrib.begin();
        while(distIt != pIndepDistrib.end()) {
            //Real loss = distIt->first * loss_unit_
            //                    ;
            //loss = std::max(std::min(loss,
            //    results_.xMax)-results_.xMin, 0.);
            //expLoss += loss * distIt->second;

            results.push_back(distIt->second);
             ++distIt;
        }
        return results;
    }

}

#endif