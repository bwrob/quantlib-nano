lue);
                return x_;
            }
        private:
            USNG sequenceGen_;// copy, we might be mutithreaded
            mutable sample_type x_;
            // no copies
            const copulaType& copula_;
        };
        //@}
    protected:
        /* \todo Move integrator traits like number of quadrature points, 
        integration domain dimensions, etc to the copula through a static 
        member function. Since they depend on the nature of the probability 
        density distribution thats where they belong.
        This is why theres one factory per copula policy template parameter 
        (even if this is not used...yet)
        */
        class IntegrationFactory {
        public:
            static ext::shared_ptr<LMIntegration> createLMIntegration(
                Size dimension, 
                LatentModelIntegrationType::LatentModelIntegrationType type = 
                    #ifndef QL_PATCH_SOLARIS
                    LatentModelIntegrationType::GaussianQuadrature)
                    #else
                    LatentModelIntegrationType::Trapezoid)
                    #endif
            {
                switch(type) {
                    #ifndef QL_PATCH_SOLARIS
                    case LatentModelIntegrationType::GaussianQuadrature:
                        return 
                            ext::make_shared<
                            IntegrationBase<GaussianQuadMultidimIntegrator> >(
                                dimension, 25);
                    #endif
                    case LatentModelIntegrationType::Trapezoid:
                        {
                        std::vector<ext::shared_ptr<Integrator> > integrals;
                        integrals.reserve(dimension);
                        for(Size i=0; i<dimension; i++)
                            integrals.push_back(
                            ext::make_shared<TrapezoidIntegral<Default> >(
                                1.e-4, 20));
                        /* This integration domain is tailored for the T 
                        distribution; it is too wide for normals or Ts of high
                        order. 
                        \todo This needs to be solved by having the copula to 
                        provide the integration traits for any integration 
                        algorithm since it is the copula that knows the relevant
                        domain for its density distributions. Also to be able to
                        block integrations which will fail; like a quadrature  
                        here in some cases.
                        */
                        return 
                          ext::make_shared<IntegrationBase<MultidimIntegral> >
                               (integrals, -35., 35.);
                        }
                    default:
                        QL_FAIL("Unknown latent model integration type.");
                }
            }
        private:
          IntegrationFactory() = default;
        };
        //@}


    public:
        // model size, number of latent variables modelled
        Size size() const {return nVariables_;}
        //! Number of systemic factors.
        Size numFactors() const {return nFactors_;}
        //! Number of total free random factors; systemic and idiosyncratic.
        Size numTotalFactors() const { return nVariables_ + nFactors_; }

        /*! Constructs a LM with an arbitrary number of latent variables
          and factors given by the dimensions of the passed matrix.
            @param factorsWeights Ordering is factorWeights_[iVar][iFactor]
            @param ini Initialization variables. Trait type from the copula 
              policy to allow for static policies (this solution needs to be 
              revised, possibly drop the static policy and create a policy 
              member in LatentModel)
        */
        explicit LatentModel(
            const std::vector<std::vector<Real> >& factorsWeights, 
 