ay required");
        #endif
        Matrix m(1, 1, variance(t0, x0[0], dt));
        return m;
    }

    inline Array StochasticProcess1D::evolve(Time t0, const Array& x0,
                                             Time dt, const Array& dw) const {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(x0.size() == 1, "1-D array required");
        QL_REQUIRE(dw.size() == 1, "1-D array required");
        #endif
        Array a(1, evolve(t0,x0[0],dt,dw[0]));
        return a;
    }

    inline Array StochasticProcess1D::apply(const Array& x0,
                                            const Array& dx) const {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(x0.size() == 1, "1-D array required");
        QL_REQUIRE(dx.size() == 1, "1-D array required");
        #endif
        Array a(1, apply(x0[0],dx[0]));
        return a;
    }

}


#endif
