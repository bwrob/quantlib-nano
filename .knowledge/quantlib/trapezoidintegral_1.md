            Real dx = (b-a)/N;
            Real x = a + dx/6.0;
            Real D = 2.0*dx/3.0;
            for (Size i=0; i<N; x += dx, ++i)
                sum += f(x) + f(x+D);
            return (I + dx*sum)/3.0;
        }
        static Size nbEvalutions(){ return 3;}
    };

}

#endif