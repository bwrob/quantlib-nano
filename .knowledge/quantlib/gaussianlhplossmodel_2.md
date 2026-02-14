> notionals = basket_->remainingNotionals(d);
            Real denominator = std::inner_product(notionals.begin(),
                notionals.end(), probs.begin(), Real(0.));
            if(denominator == 0.) return 0.;

            std::transform(notionals.begin(), notionals.end(), probs.begin(),
                notionals.begin(), std::multiplies<>());

            return std::inner_product(recoveries.begin(), recoveries.end(),
                notionals.begin(), Real(0.)) / denominator;
        }

    private:
        // cached
        mutable Real sqrt1minuscorrel_;

        Handle<Quote> correl_;
        std::vector<Handle<RecoveryRateQuote> > rrQuotes_;
        // calculation buffers

        /* The problem with defining a fixed average recovery on a portfolio
        with uneven exposures is that it does not preserve portfolio
        moments like the expected loss. To achieve it one should define the
        averarage recovery with a time dependence:
        $\hat{R}(t) = \frac{\sum_i R_i N_i P_i(t)}{\sum_i N_i P_i(t)}$
        But the date dependence increases significantly the calculations cost.
        Notice that this problem dissapears if the recoveries are all equal.
        */

        Real beta_;
        BivariateCumulativeNormalDistribution biphi_;
        static CumulativeNormalDistribution const phi_;
    };

}

#endif

#endif
