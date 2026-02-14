xtSamples(nextSampleSize_);
        }
    }
    #endif

    template <class T, class U>
    void ConvergenceStatistics<T,U>::reset() {
        T::reset();
        nextSampleSize_ = samplingRule_.initialSamples();
        table_.clear();
    }

    template <class T, class U>
    const typename ConvergenceStatistics<T,U>::table_type&
    ConvergenceStatistics<T,U>::convergenceTable() const {
        return table_;
    }

}


#endif
