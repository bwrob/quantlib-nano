ve number of population members required");
                populationMembers = n;
                initialPopulation.clear();
                return *this;
            }

            Configuration& withInitialPopulation(const std::vector<Array>& c) {
                initialPopulation = c;
                populationMembers = c.size();
                return *this;
            }

            Configuration& withUpperBound(const Array& u) {
                upperBound = u;
                return *this;
            }
            
            Configuration& withLowerBound(const Array& l) {
                lowerBound = l;
                return *this;
            }

            Configuration& withSeed(unsigned long s) {
                seed = s;
                return *this;
            }

            Configuration& withAdaptiveCrossover(bool b = true) {
                crossoverIsAdaptive = b;
                return *this;
            }

            Configuration& withStepsizeWeight(Real w) {
                QL_ENSURE(w>=0 && w<=2.0,
                          "Step size weight ("<< w
                          << ") must be in [0,2] range");
                stepsizeWeight = w;
                return *this;
            }

            Configuration& withCrossoverType(CrossoverType t) {
                crossoverType = t;
                return *this;
            }

            Configuration& withStrategy(Strategy s) {
                strategy = s;
                return *this;
            }
        };


        DifferentialEvolution(const Configuration& configuration = Configuration())
        : configuration_(configuration), rng_(configuration.seed) {}

        EndCriteria::Type minimize(Problem& p, const EndCriteria& endCriteria) override;

        const Configuration& configuration() const {
            return configuration_;
        }

      private:
        Configuration configuration_;
        Array upperBound_, lowerBound_;
        mutable Array currGenSizeWeights_, currGenCrossover_;
        Candidate bestMemberEver_;
        MersenneTwisterUniformRng rng_;

        void fillInitialPopulation(std::vector<Candidate>& population,
                                   const Problem& p) const;

        void getCrossoverMask(std::vector<Array>& crossoverMask,
                              std::vector<Array>& invCrossoverMask,
                              const Array& mutationProbabilities) const;

        Array getMutationProbabilities(
                              const std::vector<Candidate>& population) const;

        void adaptSizeWeights() const;

        void adaptCrossover() const;

        void calculateNextGeneration(std::vector<Candidate>& population,
                                     Problem& costFunction) const;

        Array rotateArray(Array inputArray) const;

        void crossover(const std::vector<Candidate>& oldPopulation,
                       std::vector<Candidate> & population,
                       const std::vector<Candidate>& mutantPopulation,
                       const std::vector<Candidate>& mirrorPopulation,
                       Problem& costFunction) const;
    };

}

#endif