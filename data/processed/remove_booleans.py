import pandas as pd

df = pd.read_csv(r'C:\Users\Kaden\Documents\GitHub\UFC-Prediction-NN\data\creating-the-final-dataset\final_merged_fight_stats.csv')
style_columns = [
    "Style_Boxing", "Style_Brawler", "Style_Brazilian Jiu-Jitsu", "Style_Freestyle", "Style_Grappler",
    "Style_Jiu-Jitsu", "Style_Judo", "Style_Karate", "Style_Kickboxer", "Style_Kung Fu", "Style_Kung-Fu",
    "Style_MMA", "Style_Muay Thai", "Style_Sambo", "Style_Striker", "Style_Wrestler", "Style_Wrestling",
    "Style_Taekwondo", "Style_Boxing_fighter2", "Style_Brawler_fighter2", "Style_Brazilian Jiu-Jitsu_fighter2",
    "Style_Freestyle_fighter2", "Style_Grappler_fighter2", "Style_Jiu-Jitsu_fighter2", "Style_Judo_fighter2",
    "Style_Karate_fighter2", "Style_Kickboxer_fighter2", "Style_Kung Fu_fighter2", "Style_Kung-Fu_fighter2",
    "Style_MMA_fighter2", "Style_Muay Thai_fighter2", "Style_Sambo_fighter2", "Style_Striker_fighter2",
    "Style_Wrestler_fighter2", "Style_Wrestling_fighter2", "Style_Taekwondo_fighter2", "fighter_1_ss_pct_1", "fighter_1_takedown_pct_1"
]

# Convert True/False to 1/0 and handle missing values
df[style_columns] = df[style_columns].fillna(0).astype(int)

# Save the updated dataframe
df.to_csv('final_merged_fight_stats_final.csv', index=False)