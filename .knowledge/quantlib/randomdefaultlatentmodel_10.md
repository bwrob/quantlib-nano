       return model_->latentVarValue(factorsSample, iVar);
        }
        //allows statistics to know the portfolio size (could be moved to parent
        //invoking duck typing on the variable name or a handle to the basket)
        Size basketSize() const { return model_->size(); }
    private:
      void resetModel() override /*const*/ {
          /* Explore: might save recalculation if the basket is the same
          (some situations, like BC or control variates) in that case do not
          update, only reset the model's basket.
          */
          model_->resetBasket(this->basket_.currentLink());

          QL_REQUIRE(this->basket_->size() == model_->size(),
                     "Incompatible basket and model sizes.");
          QL_REQUIRE(recoveries_.size() == this->basket_->size(),
                     "Incompatible basket and recovery sizes.");
          // invalidate current calculations if any and notify observers
          // NOLINTNEXTLINE(bugprone-parent-virtual-call)
          LazyObject::update();
      }
        // This one and the buffer might be moved to the parent, only some
        //   dates might be specific to a particular model.
        // Default probabilities for each name at the time of the maximun
        //   horizon date. Cached for perf.
        mutable std::vector<Probability> horizonDefaultPs_;
    };





    template<class C, class URNG>
    void RandomDefaultLM<C, URNG>::nextSample(
        const std::vector<Real>& values) const
    {
        const ext::shared_ptr<Pool>& pool = this->basket_->pool();
        // starts with no events
        this->simsBuffer_.push_back(std::vector<defaultSimEvent> ());

        for(Size iName=0; iName<model_->size(); iName++) {
            Real latentVarSample =
                model_->latentVarValue(values, iName);
            Probability simDefaultProb =
               model_->cumulativeY(latentVarSample, iName);
            // If the default simulated lies before the max date:
            if (horizonDefaultPs_[iName] >= simDefaultProb) {
                const Handle<DefaultProbabilityTermStructure>& dfts =
                    pool->get(pool->names()[iName]).// use 'live' names
                    defaultProbability(this->basket_->defaultKeys()[iName]);
                // compute and store default time with respect to the
                //  curve ref date:
                Size dateSTride =
                    static_cast<Size>(Brent().solve(// casted from Real:
                        detail::Root(dfts, simDefaultProb),
                            accuracy_,0.,1.));
                   /*
                   // value if one approximates to a flat HR;
                   //   faster (>x2) but it introduces an error:..
                   // \todo: see how to include this 'polymorphically'.
                   // While not the case in pricing in risk metrics/real
                   //   probabilities the curves are often flat
                    static_cast<Size>(ceil(maxHorizon_ *
                                        std::log(1.-simDefaultProb)
                    /std::log(1.-data_.horizonDefaultPs_[iName])));
                   */
                this->simsBuffer_.back().push_back(defaultSimEvent(iName,
                    dateSTride));
               //emplace_back
            }
        /* Used to remove sims with no events. Uses less memory, faster
        post-statistics. But only if all names in the portfolio have low
        default probability, otherwise is more expensive and sim access has
        to be modified. However low probability is also an indicator that
        variance reduction is needed. */
        }
    }




    // Common usage typedefs (notice they vary in the multithread version)
    // ---------- Gaussian default generators options ------------------------
    /* Uses copula direct normal inversion and MT generator
    typedef RandomDefaultLM<GaussianCopulaPolicy,
        RandomSequenceGenerator<MersenneTwisterUniformRng> >
