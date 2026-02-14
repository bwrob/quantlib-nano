 compare two objects by date
    /*! There is no generic implementation of this struct.
        Template specializations will have to be defined for
        each needed type (see CashFlow for an example.)
    */
    template <class T> struct earlier_than;

    /* partial specialization for shared pointers, forwarding to their
       pointees. */
    template <class T>
    struct earlier_than<ext::shared_ptr<T> > {
        bool operator()(const ext::shared_ptr<T>& x,
                        const ext::shared_ptr<T>& y) const {
            return earlier_than<T>()(*x,*y);
        }
    };

}


#endif
