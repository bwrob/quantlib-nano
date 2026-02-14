/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2016 Klaus Spanderen

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

/*
 Examples:
  1. Start with 12 worker processes
    ./quantlib-test-suite --log_level=message --report_level=short
                           --build_info=yes -- --nProc=12
  2. If parameter "--nProc" is omitted then the number
     of worker processes will be equal to the number of CPU cores.
 */


#ifndef quantlib_parallel_test_runner_hpp
#define quantlib_parallel_test_runner_hpp


#include <ql/types.hpp>
#include <ql/errors.hpp>

#ifdef VERSION
/* This comes from ./configure, and for some reason it interferes with
   the internals of the unit test library in Boost 1.63. */
#undef VERSION
#endif

#if BOOST_VERSION >= 108800
#include <boost/process/v1/system.hpp>
#include <boost/process/v1/args.hpp>
namespace bp = boost::process::v1;
#else
#include <boost/process.hpp>
namespace bp = boost::process;
#endif
#include <boost/algorithm/string.hpp>
#include <boost/interprocess/ipc/message_queue.hpp>
#include <boost/interprocess/sync/scoped_lock.hpp>
#include <boost/interprocess/sync/named_mutex.hpp>

#define BOOST_TEST_NO_MAIN 1
#include <boost/test/included/unit_test.hpp>

#include <map>
#include <list>
#include <sstream>
#include <utility>
#include <fstream>
#include <chrono>
#include <string>
#include <cstring>
#include <thread>
#include <limits>

using boost::unit_test::test_results;
using namespace boost::interprocess;
using namespace boost::unit_test_framework;


namespace {
    int worker(const char* exe, const std::vector<std::string>& args) {
        return bp::system(exe, bp::args=args);
    }

    counter_t test_enabled(test_unit_id id) {
        test_case_counter tcc;
        boost::unit_test::traverse_test_tree(id, tcc);

        return tcc.p_count;
    }

    class TestCaseCollector : public test_tree_visitor {
      public:
        typedef std::map<test_unit_id, std::list<test_unit_id> > id_map_t;

        const id_map_t& map() const { return idMap_; }
        test_unit_id testSuiteId() const { return testSuiteId_; }

        bool visit(test_unit const& tu) {
            if (tu.p_parent_id == framework::master_test_suite().p_id) {
                BOOST_TEST_MESSAGE(tu.p_name.get());
                QL_REQUIRE(!tu.p_name.get().compare("QuantLibTests"),
                           "could not find QuantLib test suite");

                testSuiteId_ = tu.p_id;
            }
            return test_tree_visitor::visit(tu);
        }

        void visit(test_case const& tc) {
            if (test_enabled(tc.p_id) != 0u)
                idMap_[tc.p_parent_id].push_back(tc.p_id);
        }

        std::list<test_unit_id>::size_type numberOfTests() {
            std::list<test_unit_id>::size_type n=0;
            for (id_map_t::const_iterator p_it = idMap_.begin();
                p_it != idMap_.end(); ++p_it) n+=p_it->second.size();

            return n;
        }
      private:
        id_map_t idMap_;
        test_unit_id testSuiteId_;
    };

    class TestCaseReportAggregator : public test_tree_visitor {
      public:
        void test_suite_finish( test_suite const& ts)  {
            results_collect_helper ch( s_rc_impl().m_results_store[ts.p_id], ts );
            traverse_test_tree( ts, ch );
        }
    };

    struct 