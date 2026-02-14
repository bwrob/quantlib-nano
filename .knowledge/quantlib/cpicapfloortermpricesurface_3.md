}
                }
            }
        }

        // check that all cells are filled
        for (Size i = 0; i < cPriceB_.rows(); ++i) {
            for (Size j = 0; j < cPriceB_.columns(); ++j) {
                QL_REQUIRE(cPriceB_[i][j] != Null<Real>(),
                           "InterpolatedCPICapFloorTermPriceSurface: did not "
                           "fill call price matrix at ("
                               << i << "," << j << "), this is unexpected");
                QL_REQUIRE(fPriceB_[i][j] != Null<Real>(),
                           "InterpolatedCPICapFloorTermPriceSurface: did not "
                           "fill floor price matrix at ("
                               << i << "," << j << "), this is unexpected");
            }
        }

        cfMaturityTimes_.clear();
        for (Size i=0; i<cfMaturities_.size();i++) {
            cfMaturityTimes_.push_back(timeFromReference(cpiOptionDateFromTenor(cfMaturities_[i])));
        }

        capPrice_ = interpolator2d_.interpolate(cfMaturityTimes_.begin(),cfMaturityTimes_.end(),
                                                cfStrikes_.begin(), cfStrikes_.end(),
                                                cPriceB_
                                                );
        capPrice_.enableExtrapolation();

        floorPrice_ = interpolator2d_.interpolate(cfMaturityTimes_.begin(),cfMaturityTimes_.end(),
                                                  cfStrikes_.begin(), cfStrikes_.end(),
                                                  fPriceB_
                                                  );
        floorPrice_.enableExtrapolation();
    }

    //! remember that the strike uses the quoting convention
    template<class I2D>
    Real InterpolatedCPICapFloorTermPriceSurface<I2D>::
    price(const Date &d, Rate k) const {

        Rate atm = atmRate(d);
        return k > atm ? capPrice(d,k): floorPrice(d,k);
    }

    //! remember that the strike uses the quoting convention
    template<class I2D>
    Real InterpolatedCPICapFloorTermPriceSurface<I2D>::
    capPrice(const Date &d, Rate k) const {
        Time t = timeFromReference(d);
        return capPrice_(t,k);
    }

    //! remember that the strike uses the quoting convention
    template<class I2D>
    Real InterpolatedCPICapFloorTermPriceSurface<I2D>::
    floorPrice(const Date &d, Rate k) const {
        Time t = timeFromReference(d);
        return floorPrice_(t,k);
    }

    // inline definitions

    inline Period CPICapFloorTermPriceSurface::observationLag() const {
        return observationLag_;
    }

    inline Frequency CPICapFloorTermPriceSurface::frequency() const {
        return zeroInflationIndex()->frequency();
    }

    inline Date CPICapFloorTermPriceSurface::baseDate() const {
        return zeroInflationIndex()->zeroInflationTermStructure()->baseDate();
    }

    inline Rate CPICapFloorTermPriceSurface::baseRate() const {
        return baseRate_;
    }

    inline Real CPICapFloorTermPriceSurface::nominal() const {
        return nominal_;
    }

    inline BusinessDayConvention
    CPICapFloorTermPriceSurface::businessDayConvention() const {
        return bdc_;
    }

}

#endif
