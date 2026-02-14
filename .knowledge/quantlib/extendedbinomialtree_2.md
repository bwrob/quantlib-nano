               Size steps,
                       Real strike);

        Real underlying(Size i, Size index) const;
        Real probability(Size, Size, Size branch) const;
      protected:
        Real computeUpProb(Real k, Real dj) const;
        Time end_;
        Size oddSteps_;
        Real strike_, up_, down_, pu_, pd_;
    };


}


#endif