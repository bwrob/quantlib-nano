   #ifndef QL_PATCH_SOLARIS

    /* class template specializations. I havent use CRTP type cast directly
    because the signature of the integrators is different, grid integration
    needs the domain. */
    template<> class IntegrationBase<GaussianQuadMultidimIntegrator> : 
    public GaussianQuadMultidimIntegrator, public LMIntegration {
    public:
        IntegrationBase(Size dimension, Size order) 
        : GaussianQuadMultidimIntegrator(dimension, order) {}
        Real integrate(const std::function<Real(const std::vector<Real>& arg)>& f) const override {
            return GaussianQuadMultidimIntegrator::integrate<Real>(f);
        }
        std::vector<Real> integrateV(
            const std::function<std::vector<Real>(const std::vector<Real>& arg)>& f)
            const override {
            return GaussianQuadMultidimIntegrator::integrate<std::vector<Real>>(f);
        }
        ~IntegrationBase() override = default;
    };

    #endif

    template<> class IntegrationBase<MultidimIntegral> : 
        public MultidimIntegral, public LMIntegration {
    public:
        IntegrationBase(
            const std::vector<ext::shared_ptr<Integrator> >& integrators, 
            Real a, Real b) 
        : MultidimIntegral(integrators), 
          a_(integrators.size(),a), b_(integrators.size(),b) {}
        Real integrate(const std::function<Real(const std::vector<Real>& arg)>& f) const override {
            return MultidimIntegral::operator()(f, a_, b_);
        }
        // vector version here....
        ~IntegrationBase() override = default;
        const std::vector<Real> a_, b_;
    };

    // Intended to replace OneFactorCopula

    /*!
    \brief Generic multifactor latent variable model.\par
        In this model set up one considers latent (random) variables 
        \f$ Y_i \f$ described by:
        \f[
        \begin{array}{ccccc}
        Y_1 & = & \sum_k M_k a_{1,k} & + \sqrt{1-\sum_k a_{1,k}^2} Z_1 & 
            \sim \Phi_{Y_1}\nonumber \\
        ... & = &      ... & ...   & \nonumber \\
        Y_i & = & \sum_k M_k a_{i,k} & + \sqrt{1-\sum_k a_{i,k}^2} Z_i & 
            \sim \Phi_{Y_i}\nonumber \\
        ... & = &      ... & ...   & \nonumber \\
        Y_N & = & \sum_k M_k a_{N,k} & + \sqrt{1-\sum_k a_{N,k}^2} Z_N & 
            \sim \Phi_{Y_N}
        \end{array}
        \f]
        where the systemic \f$ M_k \f$ and idiosyncratic \f$ Z_i \f$ (this last 
        one known as error term in some contexts) random variables have 
        independent zero-mean unit-variance distributions. A restriction of the 
        model implemented here is that the N idiosyncratic variables all follow 
        the same probability law \f$ \Phi_Z(z)\f$ (but they are still 
        independent random variables) Also the model is normalized 
        so that: \f$-1\leq a_{i,k} \leq 1\f$ (technically the \f$Y_i\f$ are 
        convex linear combinations). The correlation between \f$Y_i\f$ and 
        \f$Y_j\f$ is then \f$\sum_k a_{i,k} a_{j,k}\f$. 
        \f$\Phi_{Y_i}\f$ denotes the cumulative distribution function of 
        \f$Y_i\f$ which in general differs for each latent variable.\par
        In its single factor set up this model is usually employed in derivative
        pricing and it is best to use it through integration of the desired 
        statistical properties of the model; in its multifactorial version (with
        typically around a dozen factors) it is used in the context of portfolio
        risk metrics; because of the number of variables it is best to opt for a
        simulation to compute model properties/magnitudes. 
        For this reason this class template provides a random factor sample 
        interface and an integration interface that will be instantiated by 
        derived concrete models as needed. The class is neutral on the 
        integration and random generation algorithms\par
        The latent variables are typically treated as unobservable magnitudes 
        and they serve