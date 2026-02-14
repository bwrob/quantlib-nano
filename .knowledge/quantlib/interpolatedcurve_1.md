                 "two passed dates (" << dates[i-1] << " and " << dates[i]
                           << ") correspond to the same time "
                           << "under this curve's day count convention (" << dayCounter << ")");
            }
        }

        void setupInterpolation() {
            interpolation_ = interpolator_.interpolate(times_.begin(),
                                                       times_.end(),
                                                       data_.begin());
        }
        //@}

        mutable std::vector<Time> times_;
        mutable std::vector<Real> data_;
        mutable Interpolation interpolation_;
        Interpolator interpolator_;
        // Usually, the maximum date is the one corresponding to the
        // last node. However, it might happen that a bit of
        // extrapolation is used by construction; for instance, when a
        // curve is bootstrapped and the last relevant date for an
        // instrument is after the corresponding pillar.
        // We provide here a slot to store this information, so that
        // it's available to all derived classes (we should have
        // probably done the same with the dates_ vector, but moving
        // it here might not be entirely backwards-compatible).
        Date maxDate_;
    };

}

#endif