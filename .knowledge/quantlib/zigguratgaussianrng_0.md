/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2024 Ralf Konrad Eckel

 This file is part of QuantLib, a free-software/open-source library
 for financial quantitative analysts and developers - http://quantlib.org/

 QuantLib is free software: you can redistribute it and/or modify it
 under the terms of the QuantLib license.  You should have received a
 copy of the license along with this program; if not, please email
 <quantlib-dev@lists.sf.net>. The license is also available online at
 <https://www.quantlib.org/license.shtml>.

 This program is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the license for more details.
*/

/*! \file zigguratgaussianrng.hpp
    \brief Ziggurat Gaussian random-number generator
*/

#ifndef quantlib_ziggurat_gaussian_rng_h
#define quantlib_ziggurat_gaussian_rng_h

#include <ql/methods/montecarlo/sample.hpp>
#include <cstdint>

namespace QuantLib {

    //! Gaussian random number generator
    /*! It uses the Ziggurat transformation to return a
        normal distributed Gaussian deviate with average 0.0 and
        standard deviation of 1.0, from a random integer
        in the [0,0xffffffffffffffffULL]-interval like.

        For a more detailed description see the article
        "An Improved Ziggurat Method to Generate Normal Random Samples"
        by Jurgen A. Doornik
        (https://www.doornik.com/research/ziggurat.pdf).

        The code here is inspired by the rust implementation in
        https://github.com/rust-random/rand/blob/d42daabf65a3ceaf58c2eefc7eb477c4d5a9b4ba/rand_distr/src/normal.rs
        and
        https://github.com/rust-random/rand/blob/d42daabf65a3ceaf58c2eefc7eb477c4d5a9b4ba/rand_distr/src/utils.rs.

        Class RNG must implement the following interface:
        \code
            Real nextReal() const;
            std::uint64_t nextInt64() const;
        \endcode
        Currently, Xoshiro256StarStarUniformRng is the only RNG supporting this.
    */
    template <class RNG>
    class ZigguratGaussianRng {
      public:
        typedef Sample<Real> sample_type;

        explicit ZigguratGaussianRng(const RNG& uint64Generator)
        : uint64Generator_(uint64Generator) {}

        //! returns a sample from a Gaussian distribution
        sample_type next() const { return {nextReal(), 1.0}; }

        //! return a random number from a Gaussian distribution
        Real nextReal() const;

      private:
        RNG uint64Generator_;

        typedef Real ZigguratTable[257];

        Real pdf(Real x) const;

        //! compute a random number in the tail by hand
        Real zeroCase(Real u) const;

        Real normR() const;
        Real normX(int i) const;
        Real normF(int i) const;
    };

    template <class RNG>
    inline Real ZigguratGaussianRng<RNG>::nextReal() const {
        while (true) {
            // As an optimisation we re-implement the conversion
            // to a double in the interval (-1,1).
            // From the remaining 12 most significant bits we use 8 to construct `i`.
            //
            // This saves us generating a whole extra random number, while the added
            // precision of using 64 bits for double does not buy us much.
            std::uint64_t randomU64 = uint64Generator_.nextInt64();
            Real u = 2.0 * (Real(randomU64 >> 11) + 0.5) * (1.0 / Real(1ULL << 53)) - 1.0;
            auto i = (int)(randomU64 & 0xff);

            Real x = u * normX(i);

            if (std::abs(x) < normX(i + 1)) {
                return x;
            }
            if (i == 0) {
                // compute a random number in the tail by hand
                return zeroCase(u);
            }
            if (normF(i + 1) + (normF(i) - normF(i + 1) * uint64Generator_.nextReal()) < pdf(x)) {
                return x;
            }
        }
    }

    t