const override;
        //@}
        // methods
        Probability survivalProbabilityImpl(Time) const override;
        Real defaultDensityImpl(Time) const override;
        Real hazardRateImpl(Time) const override;
        // data members
        std::vector<ext::shared_ptr<typename Traits::helper> > instruments_;
        Real accuracy_;

        // bootstrapper classes are declared as friend to manipulate
        // the curve data. They might be passed the data instead, but
        // it would increase the complexity---which is high enough
        // already.
        friend class Bootstrap<this_curve>;
        Bootstrap<this_curve> bootstrap_;
    };


    // inline definitions

    template <class C, class I, template <class> class B>
    inline Date PiecewiseDefaultCurve<C,I,B>::maxDate() const {
        calculate();
        return base_curve::maxDate();
    }

    template <class C, class I, template <class> class B>
    inline const std::vector<Time>&
    PiecewiseDefaultCurve<C,I,B>::times() const {
        calculate();
        return base_curve::times();
    }

    template <class C, class I, template <class> class B>
    inline const std::vector<Date>&
    PiecewiseDefaultCurve<C,I,B>::dates() const {
        calculate();
        return base_curve::dates();
    }

    template <class C, class I, template <class> class B>
    inline const std::vector<Real>&
    PiecewiseDefaultCurve<C,I,B>::data() const {
        calculate();
        return this->data_;
    }

    template <class C, class I, template <class> class B>
    inline std::vector<std::pair<Date, Real> >
    PiecewiseDefaultCurve<C,I,B>::nodes() const {
        calculate();
        return base_curve::nodes();
    }

    template <class C, class I, template <class> class B>
    inline void PiecewiseDefaultCurve<C,I,B>::update() {
        // it dispatches notifications only if (!calculated_ && !frozen_)
        LazyObject::update();

        // do not use base_curve::update() as it would always notify observers

        // TermStructure::update() update part
        if (this->moving_)
            this->updated_ = false;
    }

    template <class C, class I, template <class> class B>
    inline Probability
    PiecewiseDefaultCurve<C,I,B>::survivalProbabilityImpl(Time t) const {
        calculate();
        return base_curve::survivalProbabilityImpl(t);
    }

    template <class C, class I, template <class> class B>
    inline Real PiecewiseDefaultCurve<C,I,B>::defaultDensityImpl(Time t) const {
        calculate();
        return base_curve::defaultDensityImpl(t);
    }

    template <class C, class I, template <class> class B>
    inline Real PiecewiseDefaultCurve<C,I,B>::hazardRateImpl(Time t) const {
        calculate();
        return base_curve::hazardRateImpl(t);
    }

    template <class C, class I, template <class> class B>
    inline void PiecewiseDefaultCurve<C,I,B>::performCalculations() const {
        // just delegate to the bootstrapper
        bootstrap_.calculate();
    }

}

#endif