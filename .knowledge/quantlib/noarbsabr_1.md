bsorptionProbability() const { return absProb_; }

    private:
      Real p(Real f) const;
      Real forwardError(Real forward) const;
      const Real expiryTime_, externalForward_;
      const Real alpha_, beta_, nu_, rho_;
      Real absProb_, fmin_, fmax_;
      mutable Real forward_, numericalIntegralOverP_;
      mutable Real numericalForward_;
      ext::shared_ptr<GaussLobattoIntegral> integrator_;
      class integrand;
      class p_integrand;
};

namespace detail {

extern "C" const unsigned long sabrabsprob[1209600];

class D0Interpolator {
  public:
    D0Interpolator(Real forward, Real expiryTime, Real alpha, Real beta, Real nu, Real rho);
    Real operator()() const;

  private:
    Real phi(Real d0) const;
    Real d0(Real phi) const;
    const Real forward_, expiryTime_, alpha_, beta_, nu_, rho_, gamma_;
    Real sigmaI_;
    std::vector<Real> tauG_, sigmaIG_, rhoG_, nuG_, betaG_;
};

} // namespace detail
} // namespace QuantLib

#endif
