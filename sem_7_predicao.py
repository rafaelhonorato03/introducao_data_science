import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import kagglehub

path = kagglehub.dataset_download("rahmadadeakbar/california-housing-train")

dados = path

print(dados.head())
