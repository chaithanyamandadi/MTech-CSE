import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, f_oneway, chi2_contingency

# Load dataset
df = pd.read_excel('Marks Dataset.xlsx', sheet_name='Sheet0')

# Handle absentees marked by '-1'
df_valid = df[(df['INTERNALMARKS'] >= 0) & (df['EXTERNALMARKS'] >= 0)]

# 1. Overall Correlation Test (Internal vs External Marks)
correlation_coef, correlation_pvalue = pearsonr(df_valid['INTERNALMARKS'], df_valid['EXTERNALMARKS'])
print(f'Overall Correlation Coefficient: {correlation_coef:.2f}, P-value: {correlation_pvalue:.5f}')
sns.scatterplot(data=df_valid, x='INTERNALMARKS', y='EXTERNALMARKS')
plt.title('Overall Internal vs External Marks')
plt.xlabel('Internal Marks')
plt.ylabel('External Marks')
plt.show()

# Correlation Test for each subject separately
subjects = df_valid['SUBJECT_NAME'].unique()
for subject in subjects:
    subject_df = df_valid[df_valid['SUBJECT_NAME'] == subject]
    coef, pval = pearsonr(subject_df['INTERNALMARKS'], subject_df['EXTERNALMARKS'])
    print(f'Subject: {subject}')
    print(f'Correlation Coefficient: {coef:.2f}, P-value: {pval:.5f}')

    plt.figure()
    sns.scatterplot(data=subject_df, x='INTERNALMARKS', y='EXTERNALMARKS')
    plt.title(f'{subject}: Internal vs External Marks')
    plt.xlabel('Internal Marks')
    plt.ylabel('External Marks')
    plt.tight_layout()
    plt.show()

# 2. ANOVA Test (Total marks across different subjects)
anova_groups = [group['TOTALMARKS'].values for _, group in df_valid.groupby('SUBJECT_NAME')]
anova_result = f_oneway(*anova_groups)
print(f'ANOVA F-statistic: {anova_result.statistic:.2f}, P-value: {anova_result.pvalue:.5f}')

# Plotting ANOVA Results
plt.figure()
sns.boxplot(data=df_valid, x='SUBJECT_NAME', y='TOTALMARKS')
plt.xticks(rotation=45, ha='right')
plt.title('Total Marks Distribution Across Subjects')
plt.xlabel('Subjects')
plt.ylabel('Total Marks')
plt.tight_layout()
plt.show()

# 3. Chi-Square Test (Gender vs Grade)
chi2_table = pd.crosstab(df_valid['GENDER'], df_valid['GRADE'])
chi2_stat, chi2_pvalue, dof, expected = chi2_contingency(chi2_table)
print(f'Chi-square Statistic: {chi2_stat:.2f}, P-value: {chi2_pvalue:.5f}, Degrees of Freedom: {dof}')

# Plotting Chi-Square Crosstab Heatmap
sns.heatmap(chi2_table, annot=True, cmap='Blues', fmt='d')
plt.title('Grade Distribution by Gender')
plt.xlabel('Grade')
plt.ylabel('Gender')
plt.show()