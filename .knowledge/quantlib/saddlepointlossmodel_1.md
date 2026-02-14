from 
        high to low,...
    */

    /* The treatment of recovery wont work with random recoveries, they should
    be passed to the conditional methods in the same way as the probabilities.
    */

    /*
    TO DO:
    -> Failing when the tranche upper loss limit goes over the max attainable 
        loss.

    - With 15 quadrature points things are OK but 25 gives me -1#IND000 errors 
            (over region around the EL I think) 
    - Silly bug when calling some methods on todays date (zero time). 
            ProbDef = 0 there
    - VaR <- tranched?????!
    - ESF <- tranched????!!
    - VaR split
    - ESF split?

    When introducing defaults; somewhere, (after an update?) there should be 
    a check that: copula_->basketSize() EQUALS remainingBasket_.size()
    */
    template<class CP> 
    class SaddlePointLossModel : public DefaultLossModel {
    public:
        explicit SaddlePointLossModel(
            const ext::shared_ptr<ConstantLossLatentmodel<CP> >& m)
            : copula_(m) { }
    protected:
        // ----------- Cumulants and derivatives auxiliary functions ---------

        /*! Returns the cumulant generating function (zero-th order 
        expansion term) conditional to the mkt factor:
            \f$ K = \sum_j ln(1-p_j + p_j e^{N_j \times lgd_j \times s}) \f$
        */
        Real CumulantGeneratingCond(
            const std::vector<Real>& invUncondProbs,
            Real lossFraction,// saddle pt
            const std::vector<Real>&  mktFactor) const;
        /*! Returns the first derivative of the cumulant generating function 
        (first order expansion term) conditional to the mkt factor:
           \f$ K1 = \sum_j \frac{p_j \times N_j \times LGD_j \times 
                e^{N_j \times LGD_j \times s}} \
                             {1-p_j + p_j e^{N_j \times LGD_j \times s}} \f$
           One of its properties is that its value at zero is the portfolio 
           expected loss (in fractional units). Its value at infinity is the 
           max attainable portfolio loss. To be understood conditional to the 
           market factor.
        */
        Real CumGen1stDerivativeCond(
            const std::vector<Real>& invUncondProbs,
            Real saddle, // in fract loss units... humm not really
            const std::vector<Real>&  mktFactor) const;
        /*! Returns the second derivative of the cumulant generating function 
        (first order expansion term) conditional to the mkt factor:
            \f$ K2 = \sum_j \frac{p_j \times (N_j \times LGD_j)^2 \times 
                e^{N_j \times LGD_j \times s}}
                             {1-p_j + p_j e^{N_j \times LGD_j \times s}}
                      - (\frac{p_j \times N_j \times LGD_j \times e^{N_j \times 
                      LGD_j \times s}}
                             {1-p_j + p_j e^{N_j \times LGD_j \times s}})^2 \f$
        */
        Real CumGen2ndDerivativeCond(
            const std::vector<Real>& invUncondProbs,
            Real saddle, 
            const std::vector<Real>&  mktFactor) const;
        Real CumGen3rdDerivativeCond(
            const std::vector<Real>& invUncondProbs,
            Real saddle, 
            const std::vector<Real>&  mktFactor) const;
        Real CumGen4thDerivativeCond(
            const std::vector<Real>& invUncondProbs,
            Real saddle, 
            const std::vector<Real>&  mktFactor) const ;
        /*! Returns the cumulant and second to fourth derivatives together.
          Included for optimization, most methods work on expansion of these 
          terms.
          Alternatively use a local private buffer member? */
        std::tuple<Real, Real, Real, Real> CumGen0234DerivCond(
            const std::vector<Real>& invUncondProbs,
            Real saddle, 
            const std::vector<Real>&  mktFactor) const;
        std::tuple<Real, Real> CumGen02DerivCond(
            const std::vector<Real>& invUncondProbs,
            Real saddle, 
            const std: