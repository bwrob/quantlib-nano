      bool interpolated,
            const Handle<YoYInflationTermStructure>& ts = {})
        : YoYInflationIndex("YY_HICPXT",
                            EURegion(),
                            false,
                            interpolated,
                            Monthly,
                            Period(1, Months),
                            EURCurrency(),
                            ts) {}

        QL_DEPRECATED_ENABLE_WARNING
    };

}


#endif
