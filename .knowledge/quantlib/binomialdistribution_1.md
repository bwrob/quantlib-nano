                "n must be an odd number: " << n << " not allowed");

        Real result = (z/(n+1.0/3.0+0.1/(n+1.0)));
        result *= result;
        result = std::exp(-result*(n+1.0/6.0));
        result = 0.5 + (z>0 ? 1 : -1) * std::sqrt((0.25 * (1.0-result)));
        return result;
    }

}


#endif
