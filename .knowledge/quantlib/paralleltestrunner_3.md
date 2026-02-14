ults_reporter::make_report();

            RuntimeLog log;
            for (unsigned i=0; i < ids.size(); ++i) {
                lq.receive(&log, sizeof(RuntimeLog), recvd_size, priority);
                runTimeLog[std::string(log.testCaseName)] = log.time;
            }

            std::ofstream out(
                profileFileName, std::ios::out | std::ios::trunc);
            out << std::setprecision(6);
            for (std::map<std::string, QuantLib::Time>::const_iterator
                iter = runTimeLog.begin(); iter != runTimeLog.end(); ++iter) {
                out << iter->first << ":" << iter->second << std::endl;
            }
            out.close();

            for (auto& thread : threadGroup) {
                thread.join();
            }
        }
        else {
            std::stringstream logBuf;
            std::streambuf* const oldBuf = log_stream().rdbuf();
            log_stream().rdbuf(logBuf.rdbuf());

            framework::init(init_unit_test_suite, argc-1, argv );
            framework::finalize_setup_phase();

            framework::impl::s_frk_state().deduce_run_status(
                framework::master_test_suite().p_id);

            logBuf.str(std::string());

            message_queue mq(open_only, testUnitIdQueueName);

            TestCaseId id;
            mq.receive(&id, sizeof(TestCaseId), recvd_size, priority);

            typedef std::list<std::pair<std::string, QuantLib::Time> >
                run_time_list_type;
            run_time_list_type runTimeLogs;

            message_queue rq(open_only, testResultQueueName);

            while (!id.terminate) {
                auto startTime = std::chrono::steady_clock::now();

                #if BOOST_VERSION < 106200
                    BOOST_TEST_FOREACH( test_observer*, to,
                        framework::impl::s_frk_state().m_observers )
                        framework::impl::s_frk_state().m_aux_em.vexecute([&](){ to->test_start(1); });

                    framework::impl::s_frk_state().execute_test_tree( id.id );

                    BOOST_TEST_REVERSE_FOREACH( test_observer*, to,
                        framework::impl::s_frk_state().m_observers )
                        to->test_finish();
                #else
                    // works for BOOST_VERSION > 106100, needed for >106500
                    framework::run(id.id, false);
                #endif

                auto stopTime = std::chrono::steady_clock::now();
                double T = std::chrono::duration_cast<std::chrono::microseconds>(stopTime - startTime).count() * 1e-6;
                runTimeLogs.push_back(std::make_pair(
                    framework::get(id.id, TUT_ANY).p_name, T));

                output_logstream(log_stream(), oldBuf, logBuf);

                QualifiedTestResults results
                    = { id.id,
                        boost::unit_test::results_collector.results(id.id) };

                rq.send(&results, sizeof(QualifiedTestResults), 0);

                mq.receive(&id, sizeof(TestCaseId), recvd_size, priority);
            }


            output_logstream(log_stream(), oldBuf, logBuf);
            log_stream().rdbuf(oldBuf);

            RuntimeLog log;
            log.testCaseName[sizeof(log.testCaseName)-1] = '\0';

            message_queue lq(open_only, testRuntimeLogName);
            for (run_time_list_type::const_iterator iter = runTimeLogs.begin();
                iter != runTimeLogs.end(); ++iter) {
                log.time = iter->second;

                std::strncpy(log.testCaseName, iter->first.c_str(),
                    sizeof(log.testCaseName)-1);

                lq.send(&log, sizeof(RuntimeLog), 0);
            }
        }
    }
    catch(QuantLib::Error &ex) {
        std::cerr << "QuantLib exception: " << ex.what() << std::endl;
        return boost::exit_exception_failure;
    }
    catch(interprocess_exception &ex){
        std::cerr << "interprocess exception: " << ex.what() << std::endl;
        r
