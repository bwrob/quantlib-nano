ize>(Brent().solve(// casted from Real:
                    detail::Root(dfts, simDefaultProb), accuracy_, 0., 1.));
                /*
                // value if one approximates to a flat HR; 
                //   faster (>x2) but it introduces an error:..
                // \todo: see how to include this 'polymorphically'. While
                //   not the case in pricing in risk metrics/real  
                //   probabilities the curves are often flat
                static_cast<Size>(ceil(maxHorizon_ * 
                                    std::log(1.-simDefaultProb)
                /std::log(1.-data_.horizonDefaultPs_[iName])));
                */
                // Determine the realized recovery rate:
                /* For this; 'conditionalRecovery' needs to compute the pdef on 
                the realized def event date from the simulation. Yet, this might
                have fallen between todays date and the default TS reference 
                date(usually a two day gap) To avoid requesting a negative time
                probability the date is moved to the TS date 
                Unless the gap is ridiculous this has no practical effect for 
                the RR value*/
                Date today = Settings::instance().evaluationDate();
                Date eventDate = today+Period(static_cast<Integer>(dateSTride), 
                    Days);
                if(eventDate<dfts->referenceDate()) 
                    eventDate = dfts->referenceDate();
                Real latentRRVarSample = 
                    copula_->latentRRVarValue(values, iName);
                Real recovery = 
                    copula_->conditionalRecovery(latentRRVarSample,
                        iName, eventDate);
                this->simsBuffer_.back().push_back(
                  defaultSimEvent(iName, dateSTride, recovery));
                //emplace_back
            }
        /* Used to remove sims with no events. Uses less memory, faster 
        post-statistics. But only if all names in the portfolio have low 
        default probability, otherwise is more expensive and sim access has 
        to be modified. However low probability is also an indicator that 
        variance reduction is needed. */
        //if(simsBuffer.back().empty()) {
        //    emptySims_++;// Size; intilzd to zero
        //    simsBuffer.pop_back();
        //}
        }
    }


    // Common uses: Not valid in multithread version.
    // ---------- Gaussian default generators options ------------------------
    /* Uses copula direct normal inversion and MT generator 
    typedef RandomLossLM<GaussianCopulaPolicy,
        RandomSequenceGenerator<MersenneTwisterUniformRng> >
            GaussianRandomLossLM;
    */
    /* Uses BoxMuller for gaussian generation, bypassing copula inversions
    typedef RandomLossLM<GaussianCopulaPolicy, RandomSequenceGenerator<
        BoxMullerGaussianRng<MersenneTwisterUniformRng> > >
            GaussianRandomLossLM;
    */
    /* Default case, uses the copula inversion directly and sobol sequence */
    typedef RandomLossLM<GaussianCopulaPolicy> GaussianRandomLossLM;

    // ---------- T default generators options ----------------------------
    /*
    typedef RandomLossLM<TCopulaPolicy, 
      RandomSequenceGenerator<MersenneTwisterUniformRng> > TRandomLossLM;
    */
    /*
    typedef RandomLossLM<TCopulaPolicy, 
        RandomSequenceGenerator<PolarStudentTRng<MersenneTwisterUniformRng> > >
            TRandomLossLM;
    */
    typedef RandomLossLM<TCopulaPolicy> TRandomLossLM;

}

#endif