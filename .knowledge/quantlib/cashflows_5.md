  const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                              Date settlementDate = Date(),
                              Date npvDate = Date(),
                              Real accuracy = 1.0e-10,
                              Size maxIterations = 100,
                              Rate guess = 0.0);
        //@}

    };

}

#endif
