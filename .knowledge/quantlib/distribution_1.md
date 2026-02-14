lated from x_i to infinity
        // cumulativeExcessProbability: integrated excessProbability from x = 0
        std::vector<Real> density_, cumulativeDensity_;
        std::vector<Real> excessProbability_, cumulativeExcessProbability_;
        // average loss in cell i
        std::vector<Real> average_;

        int overFlow_, underFlow_;
        bool isNormalized_;
    };

    class ManipulateDistribution {
    public:
        static Distribution convolve (const Distribution& d1,
                                      const Distribution& d2);
    };

}

#endif