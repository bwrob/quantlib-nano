ng(2, 1); // middle price
        Real s2d = lattice->underlying(2, 0); // down (low) price

        // calculate gamma by taking the first derivate of the two deltas
        Real delta2u = (p2u - p2m)/(s2u-s2m);
        Real delta2d = (p2m-p2d)/(s2m-s2d);
        Real gamma = (delta2u - delta2d) / ((s2u-s2d)/2);

        // Rollback to second-last step, and get option values (p1) at
        // this point
        option.rollback(grid[1]);
        Array va(option.values());
        QL_ENSURE(va.size() == 2, "Expect 2 nodes in grid at first step");
        Real p1u = va[1];
        Real p1d = va[0];
        Real s1u = lattice->underlying(1, 1); // up (high) price
        Real s1d = lattice->underlying(1, 0); // down (low) price

        Real delta = (p1u - p1d) / (s1u - s1d);

        // Finally, rollback to t=0
        option.rollback(0.0);
        Real p0 = option.presentValue();

        // Store results
        results_.value = p0;
        results_.delta = delta;
        results_.gamma = gamma;
        // theta can be approximated by calculating the numerical derivative
        // between mid value at third-last step and at t0. The underlying price
        // is the same, only time varies.
        results_.theta = (p2m - p0) / grid[2];
    }

}


#endif
