              const std::vector<T>& y1,
                                                     const Real x1,
                                                     const Real x2) {
        Size n = y1.size();
        std::vector<T> y(y1);
        std::vector<Real> yScale(n);
        Real x = x1;
        Real h = h1_* (x1<=x2 ? 1 : -1);
        Real hnext,hdid;

        for (Size nstp=1; nstp<=ADAPTIVERK_MAXSTP; nstp++) {
            std::vector<T> dydx=ode(x,y);
            for (Size i=0;i<n;i++)
                yScale[i] = std::abs(y[i])+std::abs(dydx[i]*h)+ADAPTIVERK_TINY;
            if ((x+h-x2)*(x+h-x1) > 0.0)
                h=x2-x;
            rkqs(y,dydx,x,h,eps_,yScale,hdid,hnext,ode);

            if ((x-x2)*(x2-x1) >= 0.0)
                return y;

            if (std::fabs(hnext) <= hmin_)
                QL_FAIL("Step size (" << hnext << ") too small ("
                        << hmin_ << " min) in AdaptiveRungeKutta");
            h=hnext;
        }
        QL_FAIL("Too many steps (" << ADAPTIVERK_MAXSTP
                << ") in AdaptiveRungeKutta");
    }

    namespace detail {

        template <class T>
        struct OdeFctWrapper {
            typedef typename AdaptiveRungeKutta<T>::OdeFct1d OdeFct1d;
            explicit OdeFctWrapper(const OdeFct1d& ode1d)
            : ode1d_(ode1d) {}
            std::vector<T> operator()(const Real x, const std::vector<T>& y) {
                std::vector<T> res(1,ode1d_(x,y[0]));
                return res;
            }
            const OdeFct1d& ode1d_;
        };

    }

    template<class T>
    T AdaptiveRungeKutta<T>::operator()(const OdeFct1d& ode,
                                        const T y1,
                                        const Real x1,
                                        const Real x2) {
        return operator()(detail::OdeFctWrapper<T>(ode),
                          std::vector<T>(1,y1),x1,x2)[0];
    }

    template<class T>
    void AdaptiveRungeKutta<T>::rkqs(std::vector<T>& y,
                                     const std::vector<T>& dydx,
                                     Real& x,
                                     const Real htry,
                                     const Real eps,
                                     const std::vector<Real>& yScale,
                                     Real& hdid,
                                     Real& hnext,
                                     const OdeFct& derivs) {
        Size n=y.size();
        Real errmax,xnew;
        std::vector<T> yerr(n),ytemp(n);

        Real h=htry;

        for(;;) {
            rkck(y,dydx,x,h,ytemp,yerr,derivs);
            errmax=0.0;
            for (Size i=0;i<n;i++)
                errmax=std::max(errmax,std::abs(yerr[i]/yScale[i]));
            errmax/=eps;
            if (errmax>1.0) {
                Real htemp1 = ADAPTIVERK_SAFETY*h*std::pow(errmax,ADAPTIVERK_PSHRINK);
                Real htemp2 = h / 10;
                // These would be std::min and std::max, of course,
                // but VC++14 had problems inlining them and caused
                // the wrong results to be calculated.  The problem
                // seems to be fixed in update 3, but let's keep this
                // implementation for compatibility.
                Real max_positive = htemp1 > htemp2 ? htemp1 : htemp2;
                Real max_negative = htemp1 < htemp2 ? htemp1 : htemp2;
                h = ((h >= 0.0) ? max_positive : max_negative);
                xnew=x+h;
                if (xnew==x)
                    QL_FAIL("Stepsize underflow (" << h << " at x = " << x
                            << ") in AdaptiveRungeKutta::rkqs");
                continue;
            } else {
                if (errmax>ADAPTIVERK_ERRCON)
                    hnext=ADAPTIVERK_SAFETY*h*std::pow(errmax,ADAPTIVERK_PGROW);
                else
                    hnext=5.0*h;
                x+=(hdid=h);
                for (Size i=0;i<n;i++)
                    y[i]=ytemp[i];
