nd largest bound
            Array bounds = upperBound - lowerBound;
            Real maxBound = bounds[0];
            for (Size j = 1; j < dim; j++) {
                if (bounds[j] > maxBound) maxBound = bounds[j];
            }
            //weights by dimension is the size of the bound
            //divided by the largest bound
            maxBound = 1.0 / maxBound;
            bounds *= maxBound;
            setDimension(dim, bounds);
        }
      protected:
        Engine engine_;
        Distribution distribution_;
        MersenneTwisterUniformRng rng_;
        Array weights_;
        Size dim_;
    };
}
#endif
