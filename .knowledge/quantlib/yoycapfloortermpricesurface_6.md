           nominalTS_->referenceDate(), baseDate, baseYoYRate,
                      yoyIndex()->frequency(), dayCounter(), YYhelpers);
        pYITS->recalculate();
        yoy_ = pYITS;   // store

        // check that helpers are repriced
        const Real eps = 1e-5;
        for (Size i=0; i<YYhelpers.size(); i++) {
            Rate original = atmYoYSwapRate( yoyOptionDateFromTenor(Period(i+1,Years)) );
            QL_REQUIRE(fabs(YYhelpers[i]->impliedQuote() - original) <eps,
                       "could not reprice helper "<< i
                       << ", data " << original
                       << ", implied quote " << YYhelpers[i]->impliedQuote()
            );
        }
    }

}


#endif