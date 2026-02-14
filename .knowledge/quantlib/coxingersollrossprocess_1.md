l b2 = 2/psi-1+std::sqrt(2/psi*(2/psi-1));
            const Real b  = std::sqrt(b2);
            const Real a  = m/(1+b2);

            result = a*(b+dw)*(b+dw);
        }
        else {
            const Real p = (psi-1)/(psi+1);
            const Real beta = (1-p)/m;

            const Real u = CumulativeNormalDistribution()(dw);

            result = ((u <= p) ? 0.0 : Real(std::log((1-p)/(1-u))/beta));
        }

        return result;
    }

}

#endif