          const ext::shared_ptr<IborIndex>& iborIdx = ext::shared_ptr<IborIndex>()) const;

    Real swapRate(const Date& fixing,
                  const Period& tenor,
                  const Date& referenceDate = Date(),
                  Real y = 0.0,
                  const ext::shared_ptr<SwapIndex>& swapIdx = ext::shared_ptr<SwapIndex>()) const;

    Real
    swapAnnuity(const Date& fixing,
                const Period& tenor,
                const Date& referenceDate = Date(),
                Real y = 0.0,
                const ext::shared_ptr<SwapIndex>& swapIdx = ext::shared_ptr<SwapIndex>()) const;

    /*! Computes the integral
    \f[ {2\pi}^{-0.5} \int_{a}^{b} p(x) \exp{-0.5*x*x} \mathrm{d}x \f]
    with
    \f[ p(x) = ax^4+bx^3+cx^2+dx+e \f].
    */
    static Real
    gaussianPolynomialIntegral(Real a, Real b, Real c, Real d, Real e, Real x0, Real x1);

    /*! Computes the integral
    \f[ {2\pi}^{-0.5} \int_{a}^{b} p(x) \exp{-0.5*x*x} \mathrm{d}x \f]
    with
    \f[ p(x) = a(x-h)^4+b(x-h)^3+c(x-h)^2+d(x-h)+e \f].
    */
    static Real gaussianShiftedPolynomialIntegral(
        Real a, Real b, Real c, Real d, Real e, Real h, Real x0, Real x1);

    /*! Generates a grid of values for the standardized state variable $y$
       at time $T$
        conditional on $y(t)=y$, covering yStdDevs standard deviations
       consisting of
        2*gridPoints+1 points */

    Array yGrid(Real yStdDevs, int gridPoints, Real T = 1.0, Real t = 0, Real y = 0) const;

  private:
    // It is of great importance for performance reasons to cache underlying
    // swaps generated from indexes. In addition the indexes may only be given
    // as templates for the conventions with the tenor replaced by the actual
    // one later on.

    struct CachedSwapKey {
        const ext::shared_ptr<SwapIndex> index;
        const Date fixing;
        const Period tenor;
        bool operator==(const CachedSwapKey &o) const {
            return index->name() == o.index->name() && fixing == o.fixing &&
                   tenor == o.tenor;
        }
    };

    struct CachedSwapKeyHasher {
        std::size_t operator()(CachedSwapKey const &x) const {
            std::size_t seed = 0;
            boost::hash_combine(seed, x.index->name());
            boost::hash_combine(seed, x.fixing.serialNumber());
            boost::hash_combine(seed, x.tenor.length());
            boost::hash_combine(seed, x.tenor.units());
            return seed;
        }
    };

    mutable std::unordered_map<CachedSwapKey, ext::shared_ptr<VanillaSwap>, CachedSwapKeyHasher> swapCache_;

  protected:
    // we let derived classes register with the termstructure
    Gaussian1dModel(const Handle<YieldTermStructure> &yieldTermStructure)
        : TermStructureConsistentModel(yieldTermStructure) {
        registerWith(Settings::instance().evaluationDate());
    }

    virtual Real numeraireImpl(Time t, Real y, const Handle<YieldTermStructure>& yts) const = 0;

    virtual Real
    zerobondImpl(Time T, Time t, Real y, const Handle<YieldTermStructure>& yts) const = 0;

    void performCalculations() const override {
        evaluationDate_ = Settings::instance().evaluationDate();
        enforcesTodaysHistoricFixings_ =
            Settings::instance().enforcesTodaysHistoricFixings();
    }

    void generateArguments() {
        calculate();
        notifyObservers();
    }

    // retrieve underlying swap from cache if possible, otherwise
    // create it and store it in the cache
    ext::shared_ptr<VanillaSwap>
    underlyingSwap(const ext::shared_ptr<SwapIndex> &index,
                   const Date &expiry, const Period &tenor) const {

        CachedSwapKey k = {index, expiry, tenor};
        auto i = swapCache_.find(k);
        if (i == swapCache_.end()) {
            ext::shared_ptr<VanillaSwap> underlying =
                index->clone(tenor)->underlyingSwap(expiry);
            swapCache_.insert(std::make_pair(k, underlying));
            return underlying;
    