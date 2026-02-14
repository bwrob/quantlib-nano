smileSectionImpl(Time) const=0;
        //@}
    };

    // inline definitions

    inline ext::shared_ptr<SmileSection>
    BlackVolSurface::smileSection(const Period& p,
                                  bool extrapolate) const {
        return smileSection(optionDateFromTenor(p), extrapolate);
    }

    inline ext::shared_ptr<SmileSection>
    BlackVolSurface::smileSection(const Date& d,
                                  bool extrapolate) const {
        return smileSection(timeFromReference(d), extrapolate);
    }

    inline ext::shared_ptr<SmileSection>
    BlackVolSurface::smileSection(Time t,
                                  bool extrapolate) const {
        checkRange(t, extrapolate);
        return smileSectionImpl(t);
    }

}

#endif
