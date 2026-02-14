t_holder(r);
        }

        inline detail::percent_holder volatility(Volatility v) {
            return detail::percent_holder(v);
        }

        template <class Container>
        inline detail::sequence_holder<typename Container::const_iterator>
        sequence(const Container& c) {
            return detail::sequence_holder<typename Container::const_iterator>(
                                                           c.begin(), c.end());
        }

    }

    namespace detail {

        template <typename T>
        inline std::ostream& operator<<(std::ostream& out,
                                        const null_checker<T>& checker) {
            if (checker.value == Null<T>())
                return out << "null";
            else
                return out << checker.value;
        }

        template <typename T>
        inline std::ostream& operator<<(std::ostream& out,
                                        const power_of_two_holder<T>& holder) {
            if (holder.n == Null<T>())
                return out << "null";

            T n = holder.n;
            Integer power = 0;
            if (n != 0) {
                while (!(n & 1UL)) {
                    power++;
                    n >>= 1;
                }
            }
            return out << n << "*2^" << power;
        }

        template <typename I>
        inline std::ostream& operator<<(std::ostream& out,
                                        const sequence_holder<I>& holder) {
            out << "( ";
            for (I i = holder.begin; i != holder.end; ++i)
                out << *i << " ";
            out << ")";
            return out;
        }

    }

}


#endif
