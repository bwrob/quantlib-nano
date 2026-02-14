eldCurve<C,I,B>::maxDate() const {
        calculate();
        return base_curve::maxDate();
    }

    template <class C, class I, template <class> class B>
    inline const std::vector<Time>& PiecewiseYieldCurve<C,I,B>::times() const {
        calculate();
        return base_curve::times();
    }

    template <class C, class I, template <class> class B>
    inline const std::vector<Date>& PiecewiseYieldCurve<C,I,B>::dates() const {
        calculate();
        return base_curve::dates();
    }

    template <class C, class I, template <class> class B>
    inline const std::vector<Real>& PiecewiseYieldCurve<C,I,B>::data() const {
        calculate();
        return base_curve::data();
    }

    template <class C, class I, template <class> class B>
    inline std::vector<std::pair<Date, Real> >
    PiecewiseYieldCurve<C,I,B>::nodes() const {
        calculate();
        return base_curve::nodes();
    }

    template <class C, class I, template <class> class B>
    inline void PiecewiseYieldCurve<C,I,B>::update() {

        // it dispatches notifications only if (!calculated_ && !frozen_)
        LazyObject::update();

        // do not use base_curve::update() as it would always notify observers

        // TermStructure::update() update part
        if (this->moving_)
            this->updated_ = false;

    }

    template <class C, class I, template <class> class B>
    inline
    DiscountFactor PiecewiseYieldCurve<C,I,B>::discountImpl(Time t) const {
        calculate();
        return base_curve::discountImpl(t);
    }

    template <class C, class I, template <class> class B>
    inline void PiecewiseYieldCurve<C,I,B>::performCalculations() const {
        // just delegate to the bootstrapper
        bootstrap_.calculate();
    }

}

#endif
