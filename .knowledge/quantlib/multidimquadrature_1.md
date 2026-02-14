a 
        matrix too.
         */
        template<class RetType_T>
        RetType_T operator()(const std::function<RetType_T (
            const std::vector<Real>& arg)>& f) const 
        {
            return integrate<RetType_T>(f);
        }


        //---------------------------------------------------------
        /* Boost fails on MSVC2008 to recognise the return type when 
        calling op()  , its not boost, its me.... FIX ME*/

        // Declare, spezializations follow.
        template<class RetType_T>
        RetType_T integrate(const std::function<RetType_T (
            const std::vector<Real>& v1)>& f) const;

    private:
        /* The maximum number of dimensions of the integration variable domain
            A higher than this number of dimension would presumably be 
           impractical and another integration algorithm (MC) should be 
           considered.
           \to do Consider moving it to a library configuration variable.
        */
        static const Size maxDimensions_ = 15;

        //! \name Integration entry points generation
        //@{
        //! Recursive template methods to statically generate (at this 
        //    class construction time) handles to the integration entry points
        template<Size levelSpawn>
        void spawnFcts() const {
            integrationEntries_[levelSpawn-1] =
                [&](const std::function<Real (const std::vector<Real>&)>& f, Real x){
                    return scalarIntegrator<levelSpawn>(f, x);
                };
            integrationEntriesVR_[levelSpawn-1] =
                [&](const std::function<std::vector<Real>(const std::vector<Real>&)>& f, Real x){
                    return vectorIntegratorVR<levelSpawn>(f, x);
                };
            spawnFcts<levelSpawn-1>();
        }
        //@}

        //---------------------------------------------------------

        template <int intgDepth>
        Real scalarIntegrator(
            const std::function<Real (const std::vector<Real>& arg1)>& f,
            const Real mFctr) const 
        {
            varBuffer_[intgDepth-1] = mFctr;
            return integral_([&](Real x){ return scalarIntegrator<intgDepth-1>(f, x); });
        }

        template <int intgDepth>
        std::vector<Real> vectorIntegratorVR(
            const std::function<std::vector<Real>(const std::vector<Real>& arg1)>& f,
            const Real mFctr) const 
        {
            varBuffer_[intgDepth-1] = mFctr;
            return integralV_([&](Real x){ return vectorIntegratorVR<intgDepth-1>(f, x); });
        }

        // Same object for all dimensions poses problems when using the 
        //   parallelized integrals version.
        //! The actual integrators.
        GaussHermiteIntegration integral_;
        VectorIntegrator integralV_;

        //! Buffer to allow acces to integrations. We do not know at which 
        //    level/dimension we are going to start integration
        // \todo Declare typedefs for traits
        mutable std::vector<
        std::function<Real (std::function<Real (
            const std::vector<Real>& varg2)> f1, 
            const Real r3)> > integrationEntries_;
        mutable std::vector<
        std::function<std::vector<Real> (const std::function<std::vector<Real>(
            const std::vector<Real>& vvarg2)>& vf1, 
            const Real vr3)> > integrationEntriesVR_;

        Size dimension_;
        // integration veriable buffer
        mutable std::vector<Real> varBuffer_;
    };


    // Template specializations ---------------------------------------------

    template<>
    inline Real GaussianQuadMultidimIntegrator::operator()(
        const std::function<Real (const std::vector<Real>& v1)>& f) const
    {
        // integration entry level is selected now
        return integral_([&](Real x){ return integrationEntries_[dimension_-1](std::cref(f), x); });
    }

    // Scalar integrand version (merge with vector case?)
    template<>
    inlin