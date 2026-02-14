YieldTermStructure>& foreignRiskFreeTS,
            const Handle<YieldTermStructure>& domesticRiskFreeTS,
            const Handle<BlackVolTermStructure>& blackVolTS,
            const ext::shared_ptr<discretization>& d =
                  ext::shared_ptr<discretization>(new EulerDiscretization),
            bool forceDiscretization = false);
    };

}


#endif
