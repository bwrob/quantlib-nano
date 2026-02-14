(intermediateTimeStep);
        trapezoidalScheme_->step(fStar, t);

        bcSet_.setTime(std::max(0.0, t-dt_));
        bcSet_.applyBeforeSolving(*map_, fn);

        const array_type f =
            (1/alpha_*fStar - squared(1-alpha_)/alpha_*fn)/(2-alpha_);

        if (map_->size() == 1) {
            fn = map_->solve_splitting(0, f, -beta_);
        }
        else {
            auto preconditioner = [&](const Array& _a){ return map_->preconditioner(_a, -beta_); };
            auto applyF = [&](const Array& _a){ return apply(_a); };

            if (solverType_ == BiCGstab) {
                const BiCGStabResult result =
                    QuantLib::BiCGstab(applyF, std::max(Size(10), fn.size()),
                        relTol_, preconditioner).solve(f, f);

                (*iterations_) += result.iterations;
                fn = result.x;
            } else if (solverType_ == GMRES) {
                const GMRESResult result =
                    QuantLib::GMRES(applyF, std::max(Size(10), fn.size() / 10U), relTol_,
                                    preconditioner)
                        .solve(f, f);

                (*iterations_) += result.errors.size();
                fn = result.x;
            }
            else
                QL_FAIL("unknown/illegal solver type");
        }

        bcSet_.applyAfterSolving(fn);
    }
}

#endif