from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

from network_security.entity.config_entity import DataIngestionConfig
import os,sys, pymongo,numpy as np
from sklearn.model_selection import train_test_split