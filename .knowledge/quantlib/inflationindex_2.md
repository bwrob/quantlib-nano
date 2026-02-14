xings stored in the underlying index.
        */
        explicit YoYInflationIndex(
            const ext::shared_ptr<ZeroInflationIndex>& underlyingIndex,
            Handle<YoYInflationTermStructure> ts = {});

        /*! \deprecated Use the similar overload without the interpolated parameter.
                        Deprecated in version 1.38.
        */
        [[deprecated("Use the similar overload without the interpolated parameter")]]
        YoYInflationIndex(
            const ext::shared_ptr<ZeroInflationIndex>& underlyingIndex,
            bool interpolated,
            Handle<YoYInflationTermStructure> ts = {});

        //! Constructor for quoted year-on-year indices.
        /*! An index built with this constructor needs its past
            fixings (i.e., the past year-on-year values) to be stored
            via the `addFixing` or `addFixings` method.
        */
        YoYInflationIndex(
            const std::string& familyName,
            const Region& region,
            bool revised,
            Frequency frequency,
            const Period& availabilityLag,
            const Currency& currency,
            Handle<YoYInflationTermStructure> ts = {});

        /*! \deprecated Use the similar overload without the interpolated parameter.
                        Deprecated in version 1.38.
        */
        [[deprecated("Use the similar overload without the interpolated parameter")]]
        YoYInflationIndex(
            const std::string& familyName,
            const Region& region,
            bool revised,
            bool interpolated,
            Frequency frequency,
            const Period& availabilityLag,
            const Currency& currency,
            Handle<YoYInflationTermStructure> ts = {});
        //@}

        //! \name Index interface
        //@{
        /*! \warning the forecastTodaysFixing parameter (required by
                     the Index interface) is currently ignored.
        */
        Rate fixing(const Date& fixingDate, bool forecastTodaysFixing = false) const override;
        Real pastFixing(const Date& fixingDate) const override;
        //@}

        //! \name Other methods
        //@{
        Date lastFixingDate() const;
        bool interpolated() const;
        bool ratio() const;
        ext::shared_ptr<ZeroInflationIndex> underlyingIndex() const;
        Handle<YoYInflationTermStructure> yoyInflationTermStructure() const;

        ext::shared_ptr<YoYInflationIndex> clone(const Handle<YoYInflationTermStructure>& h) const;
        bool needsForecast(const Date& fixingDate) const;
        //@}

      protected:
        bool interpolated_;

      private:
        Rate forecastFixing(const Date& fixingDate) const;
        bool ratio_;
        ext::shared_ptr<ZeroInflationIndex> underlyingIndex_;
        Handle<YoYInflationTermStructure> yoyInflation_;
    };


    namespace detail::CPI {

        // Returns either CPI::Flat or CPI::Linear depending on the combination of index and
        // CPI::InterpolationType.
        QuantLib::CPI::InterpolationType
        effectiveInterpolationType(const QuantLib::CPI::InterpolationType& type);

        QuantLib::CPI::InterpolationType
        effectiveInterpolationType(const QuantLib::CPI::InterpolationType& type,
                                   const ext::shared_ptr<YoYInflationIndex>& index);

        // checks whether the combination of index and CPI::InterpolationType results
        // effectively in CPI::Linear
        bool isInterpolated(const QuantLib::CPI::InterpolationType& type);

        bool isInterpolated(const QuantLib::CPI::InterpolationType& type,
                            const ext::shared_ptr<YoYInflationIndex>& index);

    }


    // inline

    inline std::string InflationIndex::name() const {
        return name_;
    }

    inline std::string InflationIndex::familyName() const {
        return familyName_;
    }

    inline Region InflationIndex::region() const {
        return region_;
    }

    i