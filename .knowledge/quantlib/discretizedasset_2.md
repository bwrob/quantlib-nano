 // discard negative times...
        auto i = std::find_if(exerciseTimes_.begin(), exerciseTimes_.end(),
                              [](Time t){ return t >= 0.0; });
        // and add the positive ones
        times.insert(times.end(), i, exerciseTimes_.end());
        return times;
    }

    inline void DiscretizedOption::applyExerciseCondition() {
        for (Size i=0; i<values_.size(); i++)
            values_[i] = std::max(underlying_->values()[i], values_[i]);
    }


}


#endif
