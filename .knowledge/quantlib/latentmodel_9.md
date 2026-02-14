erter lambda
                trng_.push_back(PolarStudentTRng<urng_type>(2. / (1. - i * i), urng_));
        }
        const sample_type& nextSequence() const {
            Size i=0;
            for(; i<trng_.size(); i++)//systemic samples plus one idiosyncratic
                sequence_.value[i] = trng_[i].next().value;
            for(; i<sequence_.value.size(); i++)//rest of idiosyncratic samples
                sequence_.value[i] = trng_.back().next().value;
            return sequence_;
        }
    private:
        mutable sample_type sequence_;
        urng_type urng_;
        mutable std::vector<PolarStudentTRng<urng_type> > trng_;
    };

#endif

}


#endif
