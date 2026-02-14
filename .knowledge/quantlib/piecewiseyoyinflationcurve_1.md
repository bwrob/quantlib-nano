culate();
        return base_curve::times();
    }

    template <class I, template <class> class B, class T>
    const std::vector<Date>& PiecewiseYoYInflationCurve<I,B,T>::dates() const {
        calculate();
        return base_curve::dates();
    }

    template <class I, template <class> class B, class T>
    const std::vector<Real>& PiecewiseYoYInflationCurve<I,B,T>::data() const {
        calculate();
        return base_curve::data();
    }

    template <class I, template <class> class B, class T>
    std::vector<std::pair<Date, Real> >
    PiecewiseYoYInflationCurve<I,B,T>::nodes() const {
        calculate();
        return base_curve::nodes();
    }

    template <class I, template <class> class B, class T>
    void PiecewiseYoYInflationCurve<I,B,T>::performCalculations() const {
        bootstrap_.calculate();
    }

    template <class I, template <class> class B, class T>
    Rate PiecewiseYoYInflationCurve<I,B,T>::yoyRateImpl(Time t) const {
        calculate();
        return base_curve::yoyRateImpl(t);
    }

    template <class I, template <class> class B, class T>
    void PiecewiseYoYInflationCurve<I,B,T>::update() {
        base_curve::update();
        LazyObject::update();
    }

}

#endif