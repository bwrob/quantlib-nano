rn NoArbSabrInterpolation(
            xBegin, xEnd, yBegin, t_, forward_, alpha_, beta_, nu_, rho_,
            alphaIsFixed_, betaIsFixed_, nuIsFixed_, rhoIsFixed_, vegaWeighted_,
            endCriteria_, optMethod_, errorAccept_, useMaxError_, maxGuesses_);
    }
    static const bool global = true;

  private:
    Time t_;
    Real forward_;
    Real alpha_, beta_, nu_, rho_;
    bool alphaIsFixed_, betaIsFixed_, nuIsFixed_, rhoIsFixed_;
    bool vegaWeighted_;
    const ext::shared_ptr<EndCriteria> endCriteria_;
    const ext::shared_ptr<OptimizationMethod> optMethod_;
    const Real errorAccept_;
    const bool useMaxError_;
    const Size maxGuesses_;
};
}

#endif