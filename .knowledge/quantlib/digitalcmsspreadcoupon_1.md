edule schedule_;
        ext::shared_ptr<SwapSpreadIndex> index_;
        std::vector<Real> notionals_;
        DayCounter paymentDayCounter_;
        BusinessDayConvention paymentAdjustment_ = Following;
        std::vector<Natural> fixingDays_;
        std::vector<Real> gearings_;
        std::vector<Spread> spreads_;
        bool inArrears_ = false;
        std::vector<Rate> callStrikes_, callPayoffs_;
        Position::Type longCallOption_ = Position::Long;
        bool callATM_ = false;
        std::vector<Rate> putStrikes_, putPayoffs_;
        Position::Type longPutOption_ = Position::Long;
        bool putATM_ = false;
        ext::shared_ptr<DigitalReplication> replication_;
        bool nakedOption_;
    };

}


#endif