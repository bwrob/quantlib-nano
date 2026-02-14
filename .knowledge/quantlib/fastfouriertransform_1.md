_t k = j; k < N; k += m) {
                        complex t = w * (*(out + k + m/2));
                        complex u = *(out + k);
                        *(out + k) = u + t;
                        *(out + k + m/2) = u - t;
                    }
                    w *= wm;
                }
            }
        }

        static std::size_t bit_reverse(std::size_t x, std::size_t order) {
            std::size_t n = 0;
            for (std::size_t i = 0; i < order; ++i) {
                n <<= 1;
                n |= (x & 1);
                x >>= 1;
            }
            return n;
        }
    };

}

#endif
