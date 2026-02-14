sition(
            const Matrix& covarianceMatrix,
            Real tolerance = 1.0e-12);
        /*! returns the variances Array */
        const Array& variances() const { return variances_; }
        /*! returns the standard deviations Array */
        const Array& standardDeviations() const {return stdDevs_; }
        /*! returns the correlation matrix */
        const Matrix& correlationMatrix() const { return correlationMatrix_; }
      private:
        Array variances_, stdDevs_;
        Matrix correlationMatrix_;
    };

}


#endif