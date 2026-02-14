         // Accept interpolation
                        d=p/q;
                    } else {
                        d=xMid;  // Interpolation failed, use bisection
                        e=d;
                    }
                } else {
                    // Bounds decreasing too slowly, use bisection
                    d=xMid;
                    e=d;
                }
                xMin_=root_;
                fxMin_=froot;
                if (std::fabs(d) > xAcc1)
                    root_ += d;
                else
                    root_ += sign(xAcc1,xMid);
                froot=f(root_);
                ++evaluationNumber_;
            }
            QL_FAIL("maximum number of function evaluations ("
                    << maxEvaluations_ << ") exceeded");
        }
      private:
        Real sign(Real a, Real b) const {
            return b >= 0.0 ? Real(std::fabs(a)) : Real(-std::fabs(a));
        }
    };

}

#endif