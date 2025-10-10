class FeatureFlags:

    def __init__(self):
        self.flags={
            'create_flow':True,
            'edit_flow': False,
            'delete_flow': False,
        }

    def is_enabled(self, feature_name):
        """Check if a feature is enabled"""
        return self.flags.get(feature_name, False)
    
    def enable(self, feature_name):
        """Enable a feature"""
        if feature_name in self.flags:
            self.flags[feature_name]=True
            return True
        return False

    def disable(self, feature_name):
        """Disable a feature"""
        if feature_name in self.flags:
            self.flags[feature_name]=False
            return True
        return False
    
# Create a global instance
feature_flags=FeatureFlags()