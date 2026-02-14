           const typename copulaType::initTraits& ini =
                typename copulaType::initTraits());
        /*! Constructs a LM with an arbitrary number of latent variables
          depending only on one random factor but contributing to each latent
          variable through different weights.
            @param factorsWeight Ordering is factorWeights_[iVariable]
            @param ini Initialization variables. Trait type from the copula
              policy to allow for static policies (this solution needs to be
              revised, possibly drop the static policy and create a policy
              member in LatentModel)
        */
        explicit LatentModel(const std::vector<Real>& factorsWeight,
            const typename copulaType::initTraits& ini =
                typename copulaType::initTraits());
        /*! Constructs a LM with an arbitrary number of latent variables
          depending only on one random factor with the same weight for all
          latent variables.

            correlSqr is the weight, same for all.

            ini is a trait type from the copula policy, to allow for
            static policies (this solution needs to be revised,
            possibly drop the static policy and create a policy member
            in LatentModel)
        */
        explicit LatentModel(Real correlSqr,
                             Size nVariables,
                             const typename copulaType::initTraits& ini = typename copulaType::initTraits());
        /*! Constructs a LM with an arbitrary number of latent variables
          depending only on one random factor with the same weight for all
          latent variables. The weight is observed and this constructor is
          intended to be used when the model relates to a market value.

            singleFactorCorrel is the weight/mkt-factor, same for all.

            ini is a trait type from the copula policy, to allow for
            static policies (this solution needs to be revised,
            possibly drop the static policy and create a policy member
            in LatentModel)
        */
        explicit LatentModel(const Handle<Quote>& singleFactorCorrel,
            Size nVariables,
            const typename copulaType::initTraits& ini =
                typename copulaType::initTraits());

        //! Provides values of the factors \f$ a_{i,k} \f$
        const std::vector<std::vector<Real> >& factorWeights() const {
            return factorWeights_;
        }
        //! Provides values of the normalized idiosyncratic factors \f$ Z_i \f$
        const std::vector<Real>& idiosyncFctrs() const {return idiosyncFctrs_;}

        //! Latent variable correlations:
        Real latentVariableCorrel(Size iVar1, Size iVar2) const {
            // true for any normalized combination
            Real init = (iVar1 == iVar2 ?
                idiosyncFctrs_[iVar1] * idiosyncFctrs_[iVar1] : Real(0.));
            return std::inner_product(factorWeights_[iVar1].begin(),
                factorWeights_[iVar1].end(), factorWeights_[iVar2].begin(),
                    init);
        }
        //! \name Integration facility interface
        //@{
        /*! Integrates an arbitrary scalar function over the density domain(i.e.
         computes its expected value).
        */
        Real integratedExpectedValue(
            const std::function<Real(const std::vector<Real>& v1)>& f) const {
            // function composition: composes the integrand with the density
            //   through a product.
            return integration()->integrate(
                [&](const std::vector<Real>& x){ return copula_.density(x) * f(x); });
        }
        /*! Integrates an arbitrary vector function over the density domain(i.e.
         computes its expected value).
        */
        std::vector<Real> integratedExpectedValueV(
            // const std::function<std::vector<Real>(
            const std::function<std::vector<Real>(

