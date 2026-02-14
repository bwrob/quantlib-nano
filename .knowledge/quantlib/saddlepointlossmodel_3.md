of a loss fraction of
            the the tranched portfolio.

            The trancheLossFract parameter is the fraction over the
            tranche notional and must be in [0,1].
        */
        Probability probOverLossCond( 
            const std::vector<Real>& invUncondProbs,
            Real trancheLossFract, 
            const std::vector<Real>& mktFactor) const;
        Probability probOverLossPortfCond1stOrder(
            const std::vector<Real>& invUncondProbs,
            Real loss, 
            const std::vector<Real>& mktFactor) const;
    public:
      Probability probOverLoss(const Date& d, Real trancheLossFract) const override;

      std::map<Real, Probability> lossDistribution(const Date& d) const override;

    protected:
        /*! 
            Probability of having losses in the portfolio due to default 
            events equal or larger than a given absolute loss value on a 
            given date conditional to the latent model factor.
            The integral expression on the expansion is the first order 
            integration as presented in several references, see for instance; 
            equation 8 in R.Martin, K.Thompson, and C. Browne 's 
            'Taking to the Saddle', Risk Magazine, June 2001, page 91

            The passed loss is in absolute value.
        */
        Probability probOverLossPortfCond(
            const std::vector<Real>& invUncondProbs,
            Real loss, 
            const std::vector<Real>& mktFactor) const;
    public:
        Probability probOverPortfLoss(const Date& d, Real loss) const;
        Real expectedTrancheLoss(const Date& d) const override;

      protected:
        /*!
        Probability density of having losses in the total portfolio (untranched)
        due to default events equal to a given value on a given date conditional
        to the latent model factor.
        Based on the integrals of the expected shortfall. 
        */
        Probability probDensityCond(const std::vector<Real>& invUncondProbs,
            Real loss, const std::vector<Real>& mktFactor) const;
    public:
        Probability probDensity(const Date& d, Real loss) const;
    protected:
        std::vector<Real> splitLossCond(
            const std::vector<Real>& invUncondProbs,
            Real loss, std::vector<Real> mktFactor) const;
        Real expectedShortfallFullPortfolioCond(
            const std::vector<Real>& invUncondProbs,
            Real lossPerc, const std::vector<Real>& mktFactor) const;
        Real expectedShortfallTrancheCond(
            const std::vector<Real>& invUncondProbs,
            Real lossPerc, Probability percentile, 
            const std::vector<Real>& mktFactor) const;
        std::vector<Real> expectedShortfallSplitCond(
            const std::vector<Real>& invUncondProbs,
            Real lossPerc, const std::vector<Real>& mktFactor) const;
    public:
        /*! Sensitivities of the individual names to a given portfolio loss 
            value due to defaults. It returns ratios to the total structure 
            notional, which aggregated add up to the requested loss value.
            Notice then that it refers to the total portfolio, not the tranched
            basket.
            \todo  Fix this.
            \par
            see equation 8 in <b>VAR: who contributes and how much?</b> by 
            R.Martin, K.Thompson, and C. Browne in Risk Magazine, August 2001

            The passed loss is the loss amount level at which we want
            to request the sensitivity. Equivalent to a percentile.
        */
      std::vector<Real> splitVaRLevel(const Date& date, Real loss) const override;
      Real expectedShortfall(const Date& d, Probability percentile) const override;

    protected:
        Real conditionalExpectedLoss(
            const std::vector<Real>& invUncondProbs,
            const std::vector<Real>& mktFactor) const;
        Real conditionalExpectedTrancheLoss(
            const std::vector<Real>& invUncond