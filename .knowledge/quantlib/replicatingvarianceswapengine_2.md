 return process_->x0();
    }


    inline Time ReplicatingVarianceSwapEngine::residualTime() const {
        return process_->time(arguments_.maturityDate);
    }


    inline Rate ReplicatingVarianceSwapEngine::riskFreeRate() const {
        return process_->riskFreeRate()->zeroRate(residualTime(), Continuous,
                                                  NoFrequency, true);
    }


    inline
    DiscountFactor ReplicatingVarianceSwapEngine::riskFreeDiscount() const {
        return process_->riskFreeRate()->discount(residualTime());
    }

}


#endif