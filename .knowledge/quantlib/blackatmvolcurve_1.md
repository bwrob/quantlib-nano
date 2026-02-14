med; therefore, they must
            assume that extrapolation is required.
        */
        //@{
        //! spot at-the-money variance calculation
        virtual Real atmVarianceImpl(Time t) const = 0;
        //! spot at-the-money volatility calculation
        virtual Volatility atmVolImpl(Time t) const = 0;
        //@}
    };

}

#endif