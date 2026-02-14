bution do not depend
            on values produced by any engine prior to invoking reset.
        */
        void reset() { }

        //! Returns the value of the pdf for x
        Real operator()(Real x) const{
            using std::pow;
            if(x < xm_) return 0.0;
            return alpha_*pow(xm_/x, alpha_)/x;
        }

        /*!    Returns a random variate distributed according to the
            levy flight distribution.
        */
        template<class Engine>
        Real operator()(Engine& eng) const {
            using std::pow;
            return xm_*pow(std::uniform_real_distribution<Real>(0.0, 1.0)(eng), -1.0/alpha_);
        }

        /*!    Returns a random variate distributed according to the
            levy flight with parameters specified by parm
        */
        template<class Engine>
        Real operator()(Engine& eng, const param_type& parm) const {
            return LevyFlightDistribution (parm)(eng);
        }

    private:
        Real xm_;
        Real alpha_;
    };

}

#endif
