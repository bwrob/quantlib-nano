e given discretization. This method can be
            overridden in derived classes which want to hard-code a
            particular discretization.
        */
        virtual Matrix stdDeviation(Time t0,
                                    const Array& x0,
                                    Time dt) const;
        /*! returns the covariance
            \f$ V(\mathrm{x}_{t_0 + \Delta t}
                | \mathrm{x}_{t_0} = \mathrm{x}_0) \f$
            of the process after a time interval \f$ \Delta t \f$
            according to the given discretization. This method can be
            overridden in derived classes which want to hard-code a
            particular discretization.
        */
        virtual Matrix covariance(Time t0,
                                  const Array& x0,
                                  Time dt) const;
        /*! returns the asset value after a time interval \f$ \Delta t
            \f$ according to the given discretization. By default, it
            returns
            \f[
            E(\mathrm{x}_0,t_0,\Delta t) +
            S(\mathrm{x}_0,t_0,\Delta t) \cdot \Delta \mathrm{w}
            \f]
            where \f$ E \f$ is the expectation and \f$ S \f$ the
            standard deviation.
        */
        virtual Array evolve(Time t0,
                             const Array& x0,
                             Time dt,
                             const Array& dw) const;
        /*! applies a change to the asset value. By default, it
            returns \f$ \mathrm{x} + \Delta \mathrm{x} \f$.
        */
        virtual Array apply(const Array& x0,
                            const Array& dx) const;
        //@}

        //! \name utilities
        //@{
        /*! returns the time value corresponding to the given date
            in the reference system of the stochastic process.

            \note As a number of processes might not need this
                  functionality, a default implementation is given
                  which raises an exception.
        */
        virtual Time time(const Date&) const;
        //@}

        //! \name Observer interface
        //@{
        void update() override;
        //@}
      protected:
        StochasticProcess() = default;
        explicit StochasticProcess(ext::shared_ptr<discretization>);
        ext::shared_ptr<discretization> discretization_;
    };


    //! 1-dimensional stochastic process
    /*! This class describes a stochastic process governed by
        \f[
            dx_t = \mu(t, x_t)dt + \sigma(t, x_t)dW_t.
        \f]
    */
    class StochasticProcess1D : public StochasticProcess {
      public:
        //! discretization of a 1-D stochastic process
        class discretization {
          public:
            virtual ~discretization() = default;
            virtual Real drift(const StochasticProcess1D&,
                               Time t0, Real x0, Time dt) const = 0;
            virtual Real diffusion(const StochasticProcess1D&,
                                   Time t0, Real x0, Time dt) const = 0;
            virtual Real variance(const StochasticProcess1D&,
                                  Time t0, Real x0, Time dt) const = 0;
        };
        //! \name 1-D stochastic process interface
        //@{
        //! returns the initial value of the state variable
        virtual Real x0() const = 0;
        //! returns the drift part of the equation, i.e. \f$ \mu(t, x_t) \f$
        virtual Real drift(Time t, Real x) const = 0;
        /*! \brief returns the diffusion part of the equation, i.e.
            \f$ \sigma(t, x_t) \f$
        */
        virtual Real diffusion(Time t, Real x) const = 0;
        /*! returns the expectation
            \f$ E(x_{t_0 + \Delta t} | x_{t_0} = x_0) \f$
            of the process after a time interval \f$ \Delta t \f$
            according to the given discretization. This method can be
            overridden in derived classes which want to hard-code a
            particular discretizati
