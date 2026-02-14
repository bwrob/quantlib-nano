ail::NoArbSabrModel::nu_min +
                        (detail::NoArbSabrModel::nu_max -
                         detail::NoArbSabrModel::nu_min) *
                            r[j++];
        if (!paramIsFixed[3])
            values[3] = detail::NoArbSabrModel::rho_min +
                        (detail::NoArbSabrModel::rho_max -
                         detail::NoArbSabrModel::rho_min) *
                            r[j++];
    }
    Array inverse(const Array &y, const std::vector<bool> &paramIsFixed,
                  const std::vector<Real> &params, const Real forward) {
        Array x(4);
        x[1] = std::tan((y[1] - detail::NoArbSabrModel::beta_min) /
                            (detail::NoArbSabrModel::beta_max -
                             detail::NoArbSabrModel::beta_min) *
                            M_PI +
                        M_PI / 2.0);
        x[0] = std::tan((y[0] * std::pow(forward, y[1] - 1.0) -
                         detail::NoArbSabrModel::sigmaI_min) /
                            (detail::NoArbSabrModel::sigmaI_max -
                             detail::NoArbSabrModel::sigmaI_min) *
                            M_PI -
                        M_PI / 2.0);
        x[2] = std::tan((y[2] - detail::NoArbSabrModel::nu_min) /
                            (detail::NoArbSabrModel::nu_max -
                             detail::NoArbSabrModel::nu_min) *
                            M_PI +
                        M_PI / 2.0);
        x[3] = std::tan((y[3] - detail::NoArbSabrModel::rho_min) /
                            (detail::NoArbSabrModel::rho_max -
                             detail::NoArbSabrModel::rho_min) *
                            M_PI +
                        M_PI / 2.0);
        return x;
    }
    Array direct(const Array &x, const std::vector<bool> &paramIsFixed,
                 const std::vector<Real> &params, const Real forward) {
        Array y(4);
        if (paramIsFixed[1])
            y[1] = params[1];
        else
            y[1] = detail::NoArbSabrModel::beta_min +
                   (detail::NoArbSabrModel::beta_max -
                    detail::NoArbSabrModel::beta_min) *
                       (std::atan(x[1]) + M_PI / 2.0) / M_PI;
        // we compute alpha from sigmaI using beta
        // if alpha is fixed we have to check if beta is admissable
        // and adjust if need be
        if (paramIsFixed[0]) {
            y[0] = params[0];
            Real sigmaI = y[0] * std::pow(forward, y[1] - 1.0);
            if (sigmaI < detail::NoArbSabrModel::sigmaI_min) {
                y[1] = (1.0 +
                        std::log(detail::NoArbSabrModel::sigmaI_min *
                                 (1.0 + eps()) / y[0]) /
                            std::log(forward));
            }
            if (sigmaI > detail::NoArbSabrModel::sigmaI_max) {
                y[1] = (1.0 +
                        std::log(detail::NoArbSabrModel::sigmaI_max *
                                 (1.0 - eps()) / y[0]) /
                            std::log(forward));
            }
        } else {
            Real sigmaI = detail::NoArbSabrModel::sigmaI_min +
                          (detail::NoArbSabrModel::sigmaI_max -
                           detail::NoArbSabrModel::sigmaI_min) *
                              (std::atan(x[0]) + M_PI / 2.0) / M_PI;
            y[0] = sigmaI / std::pow(forward, y[1] - 1.0);
        }
        if (paramIsFixed[2])
            y[2] = params[2];
        else
            y[2] = detail::NoArbSabrModel::nu_min +
                   (detail::NoArbSabrModel::nu_max -
                    detail::NoArbSabrModel::nu_min) *
                       (std::atan(x[2]) + M_PI / 2.0) / M_PI;
        if (paramIsFixed[3])
            y[3] = params[3];
        else
            y[3] = detail::NoArbSabrModel::rho_min +
                   (detail::NoArbSabrModel::rho_max -
                    detail::NoArbSabrModel::rho_min) *
                       (std::atan(x[3]) + M_PI / 2.0) / M_PI;
        