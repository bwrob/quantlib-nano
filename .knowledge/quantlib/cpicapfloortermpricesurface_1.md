od &d, Rate k) const;
        virtual Real capPrice(const Period &d, Rate k) const;
        virtual Real floorPrice(const Period &d, Rate k) const;
        virtual Real price(const Date &d, Rate k) const = 0;
        virtual Real capPrice(const Date &d, Rate k) const = 0;
        virtual Real floorPrice(const Date &d, Rate k) const = 0;
        //@}

        virtual std::vector<Rate> strikes() const {return cfStrikes_;}
        virtual std::vector<Rate> capStrikes() const {return cStrikes_;}
        virtual std::vector<Rate> floorStrikes() const {return fStrikes_;}
        virtual std::vector<Period> maturities() const {return cfMaturities_;}

        virtual const Matrix &capPrices() const { return cPrice_; }
        virtual const Matrix &floorPrices() const { return fPrice_; }

        virtual Rate minStrike() const {return cfStrikes_.front();};
        virtual Rate maxStrike() const {return cfStrikes_.back();};
        virtual Date minDate() const {return referenceDate()+cfMaturities_.front();}// \TODO deal with index interpolation
        Date maxDate() const override { return referenceDate() + cfMaturities_.back(); }
        //@}

        virtual Date cpiOptionDateFromTenor(const Period& p) const;

      protected:
        virtual bool checkStrike(Rate K) {
            return ( minStrike() <= K && K <= maxStrike() );
        }
        virtual bool checkMaturity(const Date& d) {
            return ( minDate() <= d && d <= maxDate() );
        }

        ext::shared_ptr<ZeroInflationIndex> zii_;
        CPI::InterpolationType interpolationType_;
        Handle<YieldTermStructure> nominalTS_;
        // data
        std::vector<Rate> cStrikes_;
        std::vector<Rate> fStrikes_;
        std::vector<Period> cfMaturities_;
        mutable std::vector<Real> cfMaturityTimes_;
        Matrix cPrice_;
        Matrix fPrice_;
        // constructed
        mutable std::vector<Rate> cfStrikes_;
      private:
        Real nominal_;
        BusinessDayConvention bdc_;
        Period observationLag_;
        Rate baseRate_;
    };



    template<class Interpolator2D>
    class InterpolatedCPICapFloorTermPriceSurface
        : public CPICapFloorTermPriceSurface {
            public:
            InterpolatedCPICapFloorTermPriceSurface(Real nominal,
                                                Rate startRate,
                                                const Period &observationLag,
                                                const Calendar &cal,
                                                const BusinessDayConvention &bdc,
                                                const DayCounter &dc,
                                                const ext::shared_ptr<ZeroInflationIndex>& zii,
                                                CPI::InterpolationType interpolationType,
                                                const Handle<YieldTermStructure>& yts,
                                                const std::vector<Rate> &cStrikes,
                                                const std::vector<Rate> &fStrikes,
                                                const std::vector<Period> &cfMaturities,
                                                const Matrix &cPrice,
                                                const Matrix &fPrice,
                                                const Interpolator2D &interpolator2d = Interpolator2D());

            //! \name LazyObject interface
            //@{
            void performCalculations() const;
            //@}

            //! required to allow for method hiding
            //@{
            using CPICapFloorTermPriceSurface::price;
            using CPICapFloorTermPriceSurface::capPrice;
            using CPICapFloorTermPriceSurface::floorPrice;
            //@}

            //! remember that the strikes use the quoting convention
            //@{
            Real price(const Date& d, Rate k) const override;
            Real capPrice(const Date& d, Rate k) co
