otionals_;
    }

    inline Real Basket::cumulatedLoss() const {
        return this->evalDateSettledLoss_;
    }

    inline Real Basket::settledLoss() const {
        return evalDateSettledLoss_;
    }

    inline const std::vector<DefaultProbKey>&
        Basket::remainingDefaultKeys() const
    {
        return evalDateLiveKeys_;
    }

}


#endif
