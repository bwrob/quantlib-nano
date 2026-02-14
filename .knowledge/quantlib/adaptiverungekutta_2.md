
                break;
            }
        }
    }

    template <class T>
    void AdaptiveRungeKutta<T>::rkck(const std::vector<T>& y,
                                     const std::vector<T>& dydx,
                                     Real x,
                                     const Real h,
                                     std::vector<T>& yout,
                                     std::vector<T> &yerr,
                                     const OdeFct& derivs) {

        Size n=y.size();
        std::vector<T> ak2(n),ak3(n),ak4(n),ak5(n),ak6(n),ytemp(n);

        // first step
        for (Size i=0;i<n;i++)
            ytemp[i]=y[i]+b21*h*dydx[i];

        // second step
        ak2=derivs(x+a2*h,ytemp);
        for (Size i=0;i<n;i++)
            ytemp[i]=y[i]+h*(b31*dydx[i]+b32*ak2[i]);

        // third step
        ak3=derivs(x+a3*h,ytemp);
        for (Size i=0;i<n;i++)
            ytemp[i]=y[i]+h*(b41*dydx[i]+b42*ak2[i]+b43*ak3[i]);

        // fourth step
        ak4=derivs(x+a4*h,ytemp);
        for (Size i=0;i<n;i++)
            ytemp[i]=y[i]+h*(b51*dydx[i]+b52*ak2[i]+b53*ak3[i]+b54*ak4[i]);

        // fifth step
        ak5=derivs(x+a5*h,ytemp);
        for (Size i=0;i<n;i++)
            ytemp[i]=y[i]+h*(b61*dydx[i]+b62*ak2[i]+b63*ak3[i]+b64*ak4[i]+b65*ak5[i]);

        // sixth step
        ak6=derivs(x+a6*h,ytemp);
        for (Size i=0;i<n;i++) {
            yout[i]=y[i]+h*(c1*dydx[i]+c3*ak3[i]+c4*ak4[i]+c6*ak6[i]);
            yerr[i]=h*(dc1*dydx[i]+dc3*ak3[i]+dc4*ak4[i]+dc5*ak5[i]+dc6*ak6[i]);
        }
    }

}

#endif