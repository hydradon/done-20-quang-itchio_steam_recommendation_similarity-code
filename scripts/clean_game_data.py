import pandas as pd
import numpy as np
import os

df2 = pd.read_csv('../dataset/game_details_raw.csv')

df2.dropna(subset=['game_developers'], inplace=True)

# Encoding categorical variables
df2 = pd.concat([df2,
                df2.game_platforms.str.get_dummies().add_prefix('platform_'),
                df2.game_genres.str.get_dummies().add_prefix('genre_'),
                df2.game_inputs.str.get_dummies().add_prefix('input_'),
                df2.game_ave_session.str.get_dummies().add_prefix('aveSession_'),
                df2.game_made_with.str.get_dummies().add_prefix('madeWith_')
                ],
                axis=1)