ctor<Size> bestByClub_;
        std::vector<Size> worstByClub_;
        std::mt19937 generator_;
        std::uniform_int_distribution<QuantLib::Size> distribution_;
        using param_type = decltype(distribution_)::param_type;

        void leaveRandomClub(Size particle, Size currentClubs);
        void joinRandomClub(Size particle, Size currentClubs);
    };

}

#endif
