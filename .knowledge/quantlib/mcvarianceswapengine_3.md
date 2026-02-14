                                    seed_));
    }


    namespace detail {

        class Integrand {
          public:
            Integrand(Path path, ext::shared_ptr<GeneralizedBlackScholesProcess> process)
            : path_(std::move(path)), process_(std::move(process)) {}
            Real operator()(Time t) const {
                Size i =  static_cast<Size>(t/path_.timeGrid().dt(0));
                Real sigma = process_->diffusion(t,path_[i]);
                return sigma*sigma;
            }
          private:
            Path path_;
            ext::shared_ptr<GeneralizedBlackScholesProcess> process_;
        };

    }


    inline Real VariancePathPricer::operator()(const Path& path) const {
        QL_REQUIRE(!path.empty(), "the path cannot be empty");
        Time t0 = path.timeGrid().front();
        Time t = path.timeGrid().back();
        Time dt = path.timeGrid().dt(0);
        SegmentIntegral integrator(static_cast<Size>(t/dt));
        detail::Integrand f(path, process_);
        return integrator(f,t0,t)/t;
    }

}


#endif