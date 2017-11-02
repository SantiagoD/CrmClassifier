#!-*- coding: utf8 -*-

import pandas as pd
from collections import Counter
import numpy as np
from sklearn.cross_validation import cross_val_score
import nltk
import log_writer as log

classificacoes = pd.read_csv('forums_rand_multilabel', encoding = 'utf-8')
 