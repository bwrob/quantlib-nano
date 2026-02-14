 );
                }
            }
        }

        // Compute error in VaR split
        std::vector<Real> means, rangeUp, rangeDown;
        Real confidFactor = InverseCumulativeNormal()(0.5+confInterval/2.);
        for(Size iName=0; iName<numLiveNames; iName++) {
            means.push_back(splitStats[iName].mean());
            Real error = confidFactor * splitStats[iName].errorEstimate() ;
            rangeDown.push_back(means.back() - error);
            rangeUp.push_back(means.back() + error);
        }

        std::vector<std::vector<Real> > results;
        results.push_back(means);
        results.push_back(rangeDown);
        results.push_back(rangeUp);

        return results;
    }




    // --------- Time inversion solver target function: -----------------------

    /* It could be argued that this concept is part of the copula (more generic)
    In general when the modelled magnitude is parametric one can solve for
    inversion to get the parameter value for a given magnitude value (provided
    the modelled variable dependence in invertible). In this particular problem
    the parameter is Time and it is solved here where we are alredy in the
    context of default
    See default transition models for another instance of this inversion.
    Alternatively use the faster trick (flat HR) mentioned in the code or make
    the algorithm parametric on the type of interpolation in the default TS.
    */
    namespace detail {// not template dependent .....move it
        //! Utility for the numerical time solver
        class Root {
          public:
            /* See a faster algorithm (neeeds to locate the points) in
            D.O'KANE p.249 sect 13.5 */
            Root(const Handle<DefaultProbabilityTermStructure>& dts, Real pd)
            : dts_(dts), pd_(pd), curveRef_(dts->referenceDate()) {}
            /* The cast I am forcing here comes from the requirement of 1D
            solvers to take in a target (cost) function of Real domain. It could
            be possible to change the template arg F in the 1D solvers to a
            boost function and then use the (template arg) domain argument type
            of the function for use with the 'guess' and operator() ?
             */
            Real operator()(Real t) const {
                QL_REQUIRE (t >= 0.0, "t < 0");
                /* As long as this doesnt involve modifying a mutable member
                it should be thread safe (they are const methods and access is
                read only)
                */
                return dts_->defaultProbability(curveRef_ +
                    Period(static_cast<Integer>(t), Days), true) - pd_;
            }
          private:
            const Handle<DefaultProbabilityTermStructure> dts_;
            Real pd_;
            const Date curveRef_;
        };
    }

    /*
    ---------------------------------------------------------------------------
    ---------------------------------------------------------------------------
    */

    // move this one to a separte file?
    /*! Random default with deterministic recovery event type.\par
    Stores sims results in a bitfield buffer for lean memory storage.
    Although strictly speaking this is not guaranteed by the compiler it
    amounts to reducing the memory storage by half.
    Some computations, like conditional statistics, precise that all sims
    results be available.
    */
    template<class , class > class RandomDefaultLM;
    template<class copulaPolicy, class USNG>
    struct simEvent<RandomDefaultLM<copulaPolicy, USNG> > {
        simEvent(unsigned int n, unsigned int d)
        : nameIdx(n), dayFromRef(d){}
        unsigned int nameIdx : 16; // can index up to 65535 names
        unsigned int dayFromRef : 16; //indexes up to 65535 days ~179 years
        bool operator<(const simEvent& evt) const {
            return dayFromRef < evt.dayFromRef;
        }
    };

    /*! Default only latent model simulation with trivially fixed
