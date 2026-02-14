 = index / modulo;
        Size branch1 = branch % T::branches;
        Size branch2 = branch / T::branches;

        Real prob1 = tree1_->probability(i, index1, branch1);
        Real prob2 = tree2_->probability(i, index2, branch2);
        // does the 36 below depend on T::branches?
        return prob1*prob2 + rho_*(m_[branch1][branch2])/36.0;
    }

}


#endif
