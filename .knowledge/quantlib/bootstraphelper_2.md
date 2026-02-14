etail {

        class BootstrapHelperSorter {
          public:
            template <class Helper>
            bool operator()(
                    const ext::shared_ptr<Helper>& h1,
                    const ext::shared_ptr<Helper>& h2) const {
                return (h1->pillarDate() < h2->pillarDate());
            }
        };

    }

}

#endif