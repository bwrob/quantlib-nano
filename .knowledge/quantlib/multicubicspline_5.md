st std::vector<Real> &v = grid_[j];
            if((dim = v.size() - 1) > 2) {
                std::vector<Real> tmp1(dim);
                x[j].swap(tmp1);
                std::vector<Real> tmp2(dim - 1);
                y[j].swap(tmp2);
                for(; k < dim; ++k) {
                    if((x[j][k] = v[k + 1] - v[k]) <= 0.0) break;
                    if (k != 0U)
                        y[j][k - 1] = 2.0 * (v[k + 1] - v[k - 1]);
                }
            }
            QL_REQUIRE(dim >= 3,
                       "Dimension " << j
                       << " : not enough points for interpolation");
            QL_REQUIRE(k >= dim,
                       "Dimension " << j << " : invalid data");
        }

        typename c_splint::data tmp1(x), tmp2(y);
        d_.swap(tmp1);
        d2_.swap(tmp2);
    }

    #ifndef __DOXYGEN__
    // the argument value is checked and, in out of boundaries case,
    // exception is thrown BEFORE the main body of interpolation begins
    template <Size i>
    void MultiCubicSpline<i>::set_shared_coefficients(
                 const typename MultiCubicSpline<i>::argument_type &x) const {
        for(Size j = 0; j < i; ++j) {
            Size &k = i_[j], sz = grid_[j].size() - 1;
            const std::vector<Real> &v = grid_[j];
            if(x[j] < v[0] || x[j] >= v[sz]) {
                QL_REQUIRE(ae_[j],
                           "Dimension " << j << ": extrapolation is not allowed.");
                a_[j] = 1.0, a2_[j] = b_[j] = b2_[j] = 0.0;
                k =  x[j] < v[0] ? 0 : sz;
            }
            else {
                k = v[k] <= x[j] && x[j] < v[k + 1] ? k :
                    std::upper_bound(v.begin(),v.end(),x[j])-v.begin()-1;
                Real h = v[k + 1] - v[k];
                a_[j] = (v[k + 1] - x[j]) / h, b_[j] = (x[j] - v[k]) / h;
                a2_[j] = (a_[j] * a_[j] * a_[j] - a_[j]) * h * h / 6.0,
                    b2_[j] = (b_[j] * b_[j] * b_[j] - b_[j]) * h * h / 6.0;
            }
        }
    }
    #endif

}


#endif
