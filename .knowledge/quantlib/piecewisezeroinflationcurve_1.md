name Observer interface
        //@{
        void update() override;
        //@}
      private:
        // methods
        void performCalculations() const override;
        Rate zeroRateImpl(Time t) const override;
        // data members
        std::vector<ext::shared_ptr<typename Traits::helper> > instruments_;
        Real accuracy_;
        BaseDateFunc baseDateFunc_;

        friend class Bootstrap<this_curve>;
        Bootstrap<this_curve> bootstrap_;
    };


    // inline and template definitions

    template <class I, template <class> class B, class T>
    inline Date PiecewiseZeroInflationCurve<I,B,T>::baseDate() const {
        if (baseDateFunc_)
            this->calculate();
        return base_curve::baseDate();
    }

    template <class I, template <class> class B, class T>
    inline Date PiecewiseZeroInflationCurve<I,B,T>::maxDate() const {
        this->calculate();
        return base_curve::maxDate();
    }

    template <class I, template <class> class B, class T>
    const std::vector<Time>& PiecewiseZeroInflationCurve<I,B,T>::times() const {
        calculate();
        return base_curve::times();
    }

    template <class I, template <class> class B, class T>
    const std::vector<Date>& PiecewiseZeroInflationCurve<I,B,T>::dates() const {
        calculate();
        return base_curve::dates();
    }

    template <class I, template <class> class B, class T>
    const std::vector<Real>& PiecewiseZeroInflationCurve<I,B,T>::data() const {
        calculate();
        return base_curve::rates();
    }

    template <class I, template <class> class B, class T>
    std::vector<std::pair<Date, Real> >
    PiecewiseZeroInflationCurve<I,B,T>::nodes() const {
        calculate();
        return base_curve::nodes();
    }

    template <class I, template <class> class B, class T>
    void PiecewiseZeroInflationCurve<I,B,T>::performCalculations() const {
        if (baseDateFunc_)
            const_cast<this_curve*>(this)->baseDate_ = baseDateFunc_();
        bootstrap_.calculate();
    }

    template <class I, template <class> class B, class T>
    Rate PiecewiseZeroInflationCurve<I,B,T>::zeroRateImpl(Time t) const {
        calculate();
        return base_curve::zeroRateImpl(t);
    }

    template <class I, template<class> class B, class T>
    void PiecewiseZeroInflationCurve<I,B,T>::update() {
        base_curve::update();
        LazyObject::update();
    }

}

#endif