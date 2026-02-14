   inline void RelinkableHandle<T>::reset() {
        this->link_->linkTo(nullptr, true);
    }

}

#endif
