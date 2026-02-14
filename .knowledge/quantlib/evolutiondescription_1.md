volutionDescription& evolution,
                             const std::vector<Size>& numeraires);
    bool isInMoneyMarketPlusMeasure(const EvolutionDescription& evolution,
                                    const std::vector<Size>& numeraires,
                                    Size offset = 1);
    bool isInMoneyMarketMeasure(const EvolutionDescription& evolution,
                                const std::vector<Size>& numeraires);

    //! Terminal measure: the last bond is used as numeraire.
    std::vector<Size> terminalMeasure(const EvolutionDescription& evolution);

    /*! Offsetted discretely compounded money market account measure:
        for each step the offset-th unexpired bond is used as numeraire.
        When offset=0 the result is the usual discretely compounded money
        market account measure
    */
    std::vector<Size> moneyMarketPlusMeasure(const EvolutionDescription&,
                                             Size offset = 1);

    /*! Discretely compounded money market account measure:
        for each step the first unexpired bond is used as numeraire.
    */
    std::vector<Size> moneyMarketMeasure(const EvolutionDescription&);

}

#endif
