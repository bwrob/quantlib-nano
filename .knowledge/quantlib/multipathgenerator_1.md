tor_.lastSequence()
                           : generator_.nextSequence();

            Size m = process_->size();
            Size n = process_->factors();

            MultiPath& path = next_.value;

            Array asset = process_->initialValues();
            for (Size j=0; j<m; j++)
                path[j].front() = asset[j];

            Array temp(n);
            next_.weight = sequence_.weight;

            const TimeGrid& timeGrid = path[0].timeGrid();
            Time t, dt;
            for (Size i = 1; i < path.pathSize(); i++) {
                Size offset = (i-1)*n;
                t = timeGrid[i-1];
                dt = timeGrid.dt(i-1);
                if (antithetic)
                    std::transform(sequence_.value.begin()+offset,
                                   sequence_.value.begin()+offset+n,
                                   temp.begin(),
                                   std::negate<>());
                else
                    std::copy(sequence_.value.begin()+offset,
                              sequence_.value.begin()+offset+n,
                              temp.begin());

                asset = process_->evolve(t, asset, dt, temp);
                for (Size j=0; j<m; j++)
                    path[j][i] = asset[j];
            }
            return next_;
        }
    }

}

#endif