 to model one or several magnitudes related to them
        through some function
        \f[
        \begin{array}{ccc}
        F_i(Y_i) & = &
            F_i(\sum_k M_k a_{i,k} + \sqrt{1-\sum_k a_{i,k}^2} Z_i )\nonumber \\
        & = & F_i(M_1,..., M_k, ..., M_K, Z_i)
        \end{array}
        \f]
        The transfer function can have a more generic form:
        \f$F_i(Y_1,....,Y_N)\f$ but here the model is restricted to a one to
        one relation between the latent variables and the modelled ones. Also
        it is assumed that \f$F_i(y_i; \tau)\f$ is monotonic in \f$y_i\f$; it
        can then be inverted and the relation of the cumulative probability of
        \f$F_i\f$ and \f$Y_i\f$ is simple:
        \f[
        \int_{\infty}^b \phi_{F_i} df =
            \int_{\infty}^{F_i^{-1}(b)} \phi_{Y_i} dy
        \f]
        If  \f$t\f$ is some value of the functional or modelled variable,
        \f$y\f$ is mapped to \f$t\f$ such that percentiles match, i.e.
        \f$F_Y(y)=Q_i(t)\f$ or \f$y=F_Y^{-1}(Q_i(t))\f$.
        The class provides an integration facility of arbitrary functions
        dependent on the model states. It also provides random number generation
        interfaces for usage of the model in monte carlo simulations.\par
        Now let \f$\Phi_Z(z)\f$ be the cumulated distribution function of (all
        equal as mentioned) \f$Z_i\f$. For a given realization of \f$M_k\f$,
        this determines the distribution of \f$y\f$:
        \f[
        Prob \,(Y_i < y|M_k) = \Phi_Z \left( \frac{y-\sum_k a_{i,k}\,M_k}
            {\sqrt{1-\sum_k a_{i,k}^2}}\right)
        \qquad
        \mbox{or}
        \qquad
        Prob \,(t_i < t|M) = \Phi_Z \left( \frac
            {F_{Y_{i}}^{-1}(Q_i(t))-\sum_k a_{i,k}\,M_k}
            {\sqrt{1-\sum_k a_{i,k}^2}}
        \right)
        \f]
        The distribution functions of \f$ M_k, Z_i \f$ are specified in
        specific copula template classes. The distribution function
        of \f$ Y_i \f$ is then given by the convolution
        \f[
        F_{Y_{i}}(y) = Prob\,(Y_i<y) =
        \int_{-\infty}^\infty\,\cdots\,\int_{-\infty}^{\infty}\:
        D_Z(z)\,\prod_k D_{M_{k}}(m_k) \quad
        \Theta \left(y - \sum_k a_{i,k}m_k -
            \sqrt{1-\sum_k a_{i,k}^2}\,z\right)\,d\bar{m}\,dz,
        \qquad
        \Theta (x) = \left\{
        \begin{array}{ll}
        1 & x \geq 0 \\
        0 & x < 0
        \end{array}\right.
        \f]
        where \f$ D_Z(z) \f$ and \f$ D_M(m) \f$ are the probability
        densities of \f$ Z\f$ and \f$ M, \f$ respectively.\par
        This convolution can also be written
        \f[
        F_{Y_{i}}(y) = Prob \,(Y_i < y) =
        \int_{-\infty}^\infty\,\cdots\,\int_{-\infty}^{\infty}
            D_{M_{k}}(m_k)\,dm_k\:
        \int_{-\infty}^{g(y,\vec{a},\vec{m})} D_Z(z)\,dz, \qquad
        g(y,\vec{a},\vec{m}) = \frac{y - \sum_k a_{i,k}m_k}
            {\sqrt{1-\sum_k a_{i,k}^2}}, \qquad \sum_k a_{i,k}^2 < 1
        \f]
        In general, \f$ F_{Y_{i}}(y) \f$ needs to be computed numerically.\par
        The policy class template separates the copula function (the
        distributions involved) and the functionality (i.e. what the latent
        model represents: a default probability, a recovery...). Since the
        copula methods for the
        probabilities are to be called repeatedly from an integration or a MC
        simulation, virtual tables are avoided and template parameter mechnics
        is preferred.\par
        There is nothing at this level enforncing the requirement
        on the factor distributions to be of zero mean and unit variance. Thats
        the user responsibility and the model fails to behave correctly if it
        is not the case.\par
        Derived classes should implement a modelled magnitude (default time,
        etc) and will provide probability distributions and conditional values.
        They could also provide functionality for the parameter in
