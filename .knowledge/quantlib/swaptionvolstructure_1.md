e volatility for a given option date and swap length
        Volatility volatility(const Date& optionDate,
                              Time swapLength,
                              Rate strike,
                              bool extrapolate = false) const;
        //! returns the volatility for a given option time and swap length
        Volatility volatility(Time optionTime,
                              Time swapLength,
                              Rate strike,
                              bool extrapolate = false) const;

        //! returns the Black variance for a given option tenor and swap tenor
        Real blackVariance(const Period& optionTenor,
                           const Period& swapTenor,
                           Rate strike,
                           bool extrapolate = false) const;
        //! returns the Black variance for a given option date and swap tenor
        Real blackVariance(const Date& optionDate,
                           const Period& swapTenor,
                           Rate strike,
                           bool extrapolate = false) const;
        //! returns the Black variance for a given option time and swap tenor
        Real blackVariance(Time optionTime,
                           const Period& swapTenor,
                           Rate strike,
                           bool extrapolate = false) const;
        //! returns the Black variance for a given option tenor and swap length
        Real blackVariance(const Period& optionTenor,
                           Time swapLength,
                           Rate strike,
                           bool extrapolate = false) const;
        //! returns the Black variance for a given option date and swap length
        Real blackVariance(const Date& optionDate,
                           Time swapLength,
                           Rate strike,
                           bool extrapolate = false) const;
        //! returns the Black variance for a given option time and swap length
        Real blackVariance(Time optionTime,
                           Time swapLength,
                           Rate strike,
                           bool extrapolate = false) const;

        //! returns the shift for a given option tenor and swap tenor
        Real shift(const Period& optionTenor,
                   const Period& swapTenor,
                   bool extrapolate = false) const;
        //! returns the shift for a given option date and swap tenor
        Real shift(const Date& optionDate,
                   const Period& swapTenor,
                   bool extrapolate = false) const;
        //! returns the shift for a given option time and swap tenor
        Real shift(Time optionTime,
                   const Period& swapTenor,
                   bool extrapolate = false) const;
        //! returns the shift for a given option tenor and swap length
        Real shift(const Period& optionTenor,
                   Time swapLength,
                   bool extrapolate = false) const;
        //! returns the shift for a given option date and swap length
        Real shift(const Date& optionDate,
                   Time swapLength,
                   bool extrapolate = false) const;
        //! returns the shift for a given option time and swap length
        Real shift(Time optionTime,
                   Time swapLength,
                   bool extrapolate = false) const;

        //! returns the smile for a given option tenor and swap tenor
        ext::shared_ptr<SmileSection> smileSection(const Period& optionTenor,
                                                     const Period& swapTenor,
                                                     bool extr = false) const;
        //! returns the smile for a given option date and swap tenor
        ext::shared_ptr<SmileSection> smileSection(const Date& optionDate,
                                                     const Period& swapTenor,
                                                     bo
