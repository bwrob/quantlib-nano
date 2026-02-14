gNPV_
        mutable Matrix errSpotCmsLegNPV_;

        // market mid prices of forward starting Cms Leg
        mutable Matrix mktFwdCmsLegNPV_;
        // model mid prices of forward starting Cms Leg
        mutable Matrix mdlFwdCmsLegNPV_;
        // Differences between mdlFwdCmsLegNPV_ and mktFwdCmsLegNPV_
        mutable Matrix errFwdCmsLegNPV_;

        std::vector<std::vector<ext::shared_ptr<Swap> > > spotSwaps_;
        std::vector<std::vector<ext::shared_ptr<Swap> > > fwdSwaps_;

     };

}

#endif
