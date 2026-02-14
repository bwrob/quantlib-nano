ion{
      public:
        LPP3HestonExpansion(Real kappa, Real theta, Real sigma, Real v0, Real rho, Real term);
        Real impliedVolatility(Real strike, Real forward) const override;

      private:
        Real coeffs[4];
        Real ekt, e2kt, e3kt, e4kt;
        Real z0(Real t, Real kappa, Real theta,
                Real delta, Real y, Real rho) const;
        Real z1(Real t, Real kappa, Real theta,
                Real delta, Real y, Real rho) const;
        Real z2(Real t, Real kappa, Real theta,
                Real delta, Real y, Real rho) const;
        Real z3(Real t, Real kappa, Real theta,
                Real delta, Real y, Real rho) const;
    };

    /*! Small-time expansion from
        "The small-time smile and term structure of implied volatility
        under the Heston model" M Forde, A Jacquier, R Lee - SIAM
        Journal on Financial Mathematics, 2012 - SIAM
    */
    class FordeHestonExpansion : public HestonExpansion {
      public:
        FordeHestonExpansion(Real kappa, Real theta, Real sigma, Real v0, Real rho, Real term);
        Real impliedVolatility(Real strike, Real forward) const override;

      private:
        Real coeffs[5];
    };

}


#endif
