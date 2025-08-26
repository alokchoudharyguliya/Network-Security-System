# Data Drifting should not be there so we need to ensure data validation
from network_security.entity.config_entity import DataValidationConfig
from network_security.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from scipy.stats import ks_2samp
import pandas as pd, os, sys
class DataValidation:
    def __init__(self):
        pass