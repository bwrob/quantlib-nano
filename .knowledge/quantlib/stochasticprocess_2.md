on.
        */
        virtual Real expectation(Time t0, Real x0, Time dt) const;
        /*! returns the standard deviation
            \f$ S(x_{t_0 + \Delta t} | x_{t_0} = x_0) \f$
            of the process after a time interval \f$ \Delta t \f$
            according to the given discretization. This method can be
            overridden in derived classes which want to hard-code a
            particular discretization.
        */
        virtual Real stdDeviation(Time t0, Real x0, Time dt) const;
        /*! returns the variance
            \f$ V(x_{t_0 + \Delta t} | x_{t_0} = x_0) \f$
            of the process after a time interval \f$ \Delta t \f$
            according to the given discretization. This method can be
            overridden in derived classes which want to hard-code a
            particular discretization.
        */
        virtual Real variance(Time t0, Real x0, Time dt) const;
        /*! returns the asset value after a time interval \f$ \Delta t
            \f$ according to the given discretization. By default, it
            returns
            \f[
            E(x_0,t_0,\Delta t) + S(x_0,t_0,\Delta t) \cdot \Delta w
            \f]
            where \f$ E \f$ is the expectation and \f$ S \f$ the
            standard deviation.
        */
        virtual Real evolve(Time t0, Real x0, Time dt, Real dw) const;
        /*! applies a change to the asset value. By default, it
            returns \f$ x + \Delta x \f$.
        */
        virtual Real apply(Real x0, Real dx) const;
        //@}
      protected:
        StochasticProcess1D() = default;
        explicit StochasticProcess1D(ext::shared_ptr<discretization>);
        ext::shared_ptr<discretization> discretization_;
      private:
        // StochasticProcess interface implementation
        Size size() const override;
        Array initialValues() const override;
        Array drift(Time t, const Array& x) const override;
        Matrix diffusion(Time t, const Array& x) const override;
        Array expectation(Time t0, const Array& x0, Time dt) const override;
        Matrix stdDeviation(Time t0, const Array& x0, Time dt) const override;
        Matrix covariance(Time t0, const Array& x0, Time dt) const override;
        Array evolve(Time t0, const Array& x0, Time dt, const Array& dw) const override;
        Array apply(const Array& x0, const Array& dx) const override;
    };


    // inline definitions

    inline Size StochasticProcess1D::size() const {
        return 1;
    }

    inline Array StochasticProcess1D::initialValues() const {
        Array a(1, x0());
        return a;
    }

    inline Array StochasticProcess1D::drift(Time t, const Array& x) const {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(x.size() == 1, "1-D array required");
        #endif
        Array a(1, drift(t, x[0]));
        return a;
    }

    inline Matrix StochasticProcess1D::diffusion(Time t, const Array& x) const {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(x.size() == 1, "1-D array required");
        #endif
        Matrix m(1, 1, diffusion(t, x[0]));
        return m;
    }

    inline Array StochasticProcess1D::expectation(
                                    Time t0, const Array& x0, Time dt) const {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(x0.size() == 1, "1-D array required");
        #endif
        Array a(1, expectation(t0, x0[0], dt));
        return a;
    }

    inline Matrix StochasticProcess1D::stdDeviation(
                                    Time t0, const Array& x0, Time dt) const {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(x0.size() == 1, "1-D array required");
        #endif
        Matrix m(1, 1, stdDeviation(t0, x0[0], dt));
        return m;
    }

    inline Matrix StochasticProcess1D::covariance(
                                    Time t0, const Array& x0, Time dt) const {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(x0.size() == 1, "1-D arr