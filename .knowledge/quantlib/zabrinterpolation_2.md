d::move(optMethod)),
      errorAccept_(errorAccept), useMaxError_(useMaxError), maxGuesses_(maxGuesses) {}
    template <class I1, class I2>
    Interpolation interpolate(const I1 &xBegin, const I1 &xEnd,
                              const I2 &yBegin) const {
        return ZabrInterpolation<Evaluation>(
            xBegin, xEnd, yBegin, t_, forward_, alpha_, beta_, nu_, rho_,
            gamma_, alphaIsFixed_, betaIsFixed_, nuIsFixed_, rhoIsFixed_,
            gammaIsFixed_, vegaWeighted_, endCriteria_, optMethod_,
            errorAccept_, useMaxError_, maxGuesses_);
    }
    static const bool global = true;

  private:
    Time t_;
    Real forward_;
    Real alpha_, beta_, nu_, rho_, gamma_;
    bool alphaIsFixed_, betaIsFixed_, nuIsFixed_, rhoIsFixed_, gammaIsFixed_;
    bool vegaWeighted_;
    const ext::shared_ptr<EndCriteria> endCriteria_;
    const ext::shared_ptr<OptimizationMethod> optMethod_;
    const Real errorAccept_;
    const bool useMaxError_;
    const Size maxGuesses_;
};
}

#endif