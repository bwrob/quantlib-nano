athGenerator() const {

        Size dimensions = process_->factors();
        TimeGrid grid = this->timeGrid();
        typename RNG::rsg_type generator =
            RNG::make_sequence_generator(dimensions*(grid.size()-1),seed_);
        return ext::shared_ptr<path_generator_type>(
                   new path_generator_type(process_,
                                           grid, generator, brownianBridge_));
    }

}


#endif