UnitIdQueueName);
            message_queue mq(create_only, testUnitIdQueueName,
                tcc.numberOfTests() + nProc, sizeof(TestCaseId));

            message_queue::remove(testResultQueueName);
            message_queue rq(create_only, testResultQueueName, nProc,
                sizeof(QualifiedTestResults));

            message_queue::remove(testRuntimeLogName);
            message_queue lq(create_only, testRuntimeLogName, nProc,
                sizeof(RuntimeLog));

            // run root test cases in master process
            const std::list<test_unit_id> qlRoot = (tcc.map().count(tcc.testSuiteId())) != 0u ?
                                                       tcc.map().find(tcc.testSuiteId())->second :
                                                       std::list<test_unit_id>();

            // fork worker processes
            std::vector<std::thread> threadGroup;
            for (unsigned i = 0; i < nProc; ++i) {
                threadGroup.emplace_back([&]() { worker(argv[0], workerArgs); });
            }

            struct mutex_remove {
                ~mutex_remove() { named_mutex::remove(namesLogMutexName); }
            } mutex_remover;

            struct queue_remove {
                explicit queue_remove(const char* name) : name_(name) { }
                ~queue_remove() { message_queue::remove(name_); }

            private:
                const char* const name_;
            } queue_remover1(testUnitIdQueueName),
                queue_remover2(testResultQueueName),
                queue_remover3(testRuntimeLogName);

            std::multimap<Time, test_unit_id> testsSortedByRunTime;

            for (TestCaseCollector::id_map_t::const_iterator
                p_it = tcc.map().begin();
                p_it != tcc.map().end(); ++p_it) {

                if (p_it->first != tcc.testSuiteId()) {
                    for (std::list<test_unit_id>::const_iterator
                        it =  p_it->second.begin();
                        it != p_it->second.end(); ++it) {

                        const std::string name
                            = framework::get(*it, TUT_ANY).p_name;

                        if (runTimeLog.count(name) != 0u) {
                            testsSortedByRunTime.insert(
                                std::make_pair(runTimeLog[name], *it));
                        }
                        else {
                            testsSortedByRunTime.insert(
                                std::make_pair((std::numeric_limits<Time>::max)(), *it));
                        }
                    }
                }
            }

            std::list<test_unit_id> ids;
            for (std::multimap<Time, test_unit_id>::const_iterator
                iter = testsSortedByRunTime.begin();
                iter != testsSortedByRunTime.end(); ++iter) {

                ids.push_front(iter->second);
            }
            QL_REQUIRE(ids.size() + qlRoot.size() == tcc.numberOfTests(),
                "missing test case in distrubtion list");

            testsSortedByRunTime.clear();

            for (std::list<test_unit_id>::const_iterator iter = ids.begin();
                iter != ids.end(); ++iter) {
                const TestCaseId id = { *iter, false };
                mq.send(&id, sizeof(TestCaseId), 0);
            }

            const TestCaseId id = { 0, true };
            for (unsigned i = 0; i < nProc; ++i) {
                mq.send(&id, sizeof(TestCaseId), 0);
            }

            for(unsigned i = 0; i < ids.size(); ++i) {
                QualifiedTestResults remoteResults;

                rq.receive(&remoteResults,
                    sizeof(QualifiedTestResults), recvd_size, priority);

                boost::unit_test::s_rc_impl().m_results_store[remoteResults.id]
                    = remoteResults.results;
            }

            TestCaseReportAggregator tca;
            traverse_test_tree(framework::master_test_suite(), tca , true);

            res