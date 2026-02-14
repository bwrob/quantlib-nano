 Real alpha = 1.0-(maturity-(Real)days);
                // generate swap
                Period lowerPeriod =
                    years * Years + months * Months;           //+days*Days;
                Period upperPeriod = lowerPeriod + 1 * Months; // 1*Days;
                ext::shared_ptr<SwapIndex> tmpIndexLower, tmpIndexUpper;
                tmpIndexLower = indexBase_->clone(lowerPeriod);
                tmpIndexUpper = indexBase_->clone(upperPeriod);
                ext::shared_ptr<VanillaSwap> swapLower =
                    tmpIndexLower->underlyingSwap(expiry_);
                ext::shared_ptr<VanillaSwap> swapUpper =
                    tmpIndexUpper->underlyingSwap(expiry_);
                // compute npv, delta, gamma
                Real npvm =
                    alpha * NPV(swapLower, fixedRate, nominal, -h_, type) +
                    (1.0 - alpha) *
                        NPV(swapUpper, fixedRate, nominal, -h_, type);
                Real npv =
                    alpha * NPV(swapLower, fixedRate, nominal, 0.0, type) +
                    (1.0 - alpha) *
                        NPV(swapUpper, fixedRate, nominal, 0.0, type);
                Real npvu =
                    alpha * NPV(swapLower, fixedRate, nominal, h_, type) +
                    (1.0 - alpha) *
                        NPV(swapUpper, fixedRate, nominal, h_, type);
                Real delta = (npvu - npvm) / (2.0 * h_);
                Real gamma = (npvu - 2.0 * npv + npvm) / (h_ * h_);

                // debug output global standard underlying npv
                // Real xtmp = -5.0;
                // std::cout << "globalStandardNpv;";
                // while (xtmp <= 5.0 + QL_EPSILON) {
                //     std::cout << alpha *NPV(swapLower, fixedRate, nominal, xtmp,
                //                             type) +
                //                      (1.0 - alpha) * NPV(swapUpper, fixedRate,
                //                                          nominal, xtmp, type)
                //               << ";";
                //     xtmp += 0.1;
                // }
                // std::cout << std::endl;
                // end debug output

                // return target function values
                Array res(3);
                res[0] = (npv - npv_) / delta_;
                res[1] = (delta - delta_) / delta_;
                res[2] = (gamma - gamma_) / gamma_;
                return res;
            }

            const Swap::Type type_;
            const ext::shared_ptr<Gaussian1dModel> mdl_;
            const ext::shared_ptr<SwapIndex> indexBase_;
            const Date expiry_;
            const Real maxMaturity_;
            const Real npv_, delta_, gamma_, h_;
        };
    };
}

#endif