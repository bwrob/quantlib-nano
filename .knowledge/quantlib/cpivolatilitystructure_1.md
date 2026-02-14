nce(const Period& optionTenor,
                                         Rate strike,
                                         const Period &obsLag = Period(-1,Days),
                                         bool extrapolate = false) const;
        //@}

        //! \name Inspectors
        //@{
        /*! The term structure observes with a lag that is usually
            different from the availability lag of the index.  An
            inflation rate is given, by default, for the maturity
            requested assuming this lag.
        */
        virtual Period observationLag() const { return observationLag_; }
        virtual Frequency frequency() const { return frequency_; }
        virtual bool indexIsInterpolated() const {
            return indexIsInterpolated_;
        }
        virtual Date baseDate() const;
        //! base date will be in the past because of observation lag
        virtual Time timeFromBase(const Date &date,
                                  const Period& obsLag = Period(-1,Days)) const;
        // acts as zero time value for boostrapping
        virtual Volatility baseLevel() const {
            QL_REQUIRE(baseLevel_ != Null<Volatility>(),
                       "Base volatility, for baseDate(), not set.");
            return baseLevel_;
        }
        //@}

        //! \name Limits
        //@{
        //! the minimum strike for which the term structure can return vols
        Real minStrike() const override = 0;
        //! the maximum strike for which the term structure can return vols
        Real maxStrike() const override = 0;
        //@}
      protected:
        virtual void checkRange(const Date&, Rate strike, bool extrapolate) const;
        virtual void checkRange(Time, Rate strike, bool extrapolate) const;

        /*! Implements the actual volatility surface calculation in
            derived classes e.g. bilinear interpolation.  N.B. does
            not derive the surface.
        */
        virtual Volatility volatilityImpl(Time length,
                                          Rate strike) const = 0;

        mutable Volatility baseLevel_;
        // so you do not need an index
        Period observationLag_;
        Frequency frequency_;
        bool indexIsInterpolated_;
    };

}

#endif