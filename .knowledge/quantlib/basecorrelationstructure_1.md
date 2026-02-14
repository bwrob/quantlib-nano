n(Real, Real);

      void checkTrancheTenors() const;
      void checkLosses() const;
      void initializeTrancheTimes() const;
      void checkInputs(Size volRows, Size volsColumns) const;
      void registerWithMarketData();

      void update() override;
      void updateMatrix() const;

      // TermStructure interface
      Date maxDate() const override { return trancheDates_.back(); }
      Real correlation(const Date& d, Real lossLevel, bool extrapolate = false) const {
          return correlation(timeFromReference(d), lossLevel, extrapolate);
        }
        Real correlation(Time t, Real lossLevel, 
            bool extrapolate = false) const 
        {
            return interpolation_(t, lossLevel, true);
        }
    private:
        std::vector<std::vector<Handle<Quote> > > correlHandles_;
        mutable Matrix correlations_;
        Interpolation2D interpolation_;
        Size nTrancheTenors_,
            nLosses_;
        std::vector<Period> tenors_;
        mutable std::vector<Real> lossLevel_;
        mutable std::vector<Date> trancheDates_;
        mutable std::vector<Time> trancheTimes_;
    };

    // ----------------------------------------------------------------------

    template <class I2D_T>
    void BaseCorrelationTermStructure<I2D_T>::checkTrancheTenors() const {
        QL_REQUIRE(tenors_[0]>0*Days,
                   "first tranche tenor is negative (" <<
                   tenors_[0] << ")");
        for (Size i=1; i<nTrancheTenors_; ++i)
            QL_REQUIRE(tenors_[i]>tenors_[i-1],
                       "non increasing tranche tenor: " << io::ordinal(i) <<
                       " is " << tenors_[i-1] << ", " << io::ordinal(i+1) <<
                       " is " << tenors_[i]);
    }

    template <class I2D_T>
    void BaseCorrelationTermStructure<I2D_T>::checkLosses() const {
        QL_REQUIRE(lossLevel_[0]>0.,
                   "first loss level is negative (" <<
                   lossLevel_[0] << ")");
        QL_REQUIRE(lossLevel_[0] <= 1.,
            "First loss level larger than 100% (" << lossLevel_[0] <<")");
        for (Size i=1; i<nLosses_; ++i) {
            QL_REQUIRE(lossLevel_[i]>lossLevel_[i-1],
                       "non increasing losses: " << io::ordinal(i) <<
                       " is " << lossLevel_[i-1] << ", " << io::ordinal(i+1) <<
                       " is " << lossLevel_[i]);
        QL_REQUIRE(lossLevel_[i] <= 1.,
            "Loss level " << i << " larger than 100% (" << lossLevel_[i] <<")");
        }
    }

    template <class I2D_T>
    void BaseCorrelationTermStructure<I2D_T>::initializeTrancheTimes() const {
        for (Size i=0; i<nTrancheTenors_; ++i)
            trancheTimes_[i] = timeFromReference(trancheDates_[i]);
    }

    template <class I2D_T>
    void BaseCorrelationTermStructure<I2D_T>::checkInputs(Size volRows,
                                               Size volsColumns) const {
        QL_REQUIRE(nLosses_==volRows,
                   "mismatch between number of loss levels (" <<
                   nLosses_ << ") and number of rows (" << volRows <<
                   ") in the correl matrix");
        QL_REQUIRE(nTrancheTenors_==volsColumns,
                   "mismatch between number of tranche tenors (" <<
                   nTrancheTenors_ << ") and number of columns (" << 
                   volsColumns << ") in the correl matrix");
    }

    template <class I2D_T>
    void BaseCorrelationTermStructure<I2D_T>::registerWithMarketData()
    {
        for (Size i=0; i<correlHandles_.size(); ++i)
            for (Size j=0; j<correlHandles_.front().size(); ++j)
                registerWith(correlHandles_[i][j]);
    }

    template <class I2D_T>
    void BaseCorrelationTermStructure<I2D_T>::update() {
        updateMatrix();
        TermStructure::update();
    }

    template <class I2D_T>
    void BaseCorrelationTermStructure<I2D_T>::updateMatrix() const {
        for (Size i=0; i<correlHandles_.size(); ++i)
            for