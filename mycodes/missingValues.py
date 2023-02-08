# Random Sample Imputation, 
'''The idea behind the random sample imputation is different from the previous ones and involves additional steps. 
First, it starts by creating two subsets from the original data. 
The first subset contains all the observations without missing data, and the second one contains those with missing data. 
Then, it randomly selects from each subset a random observation.
Furthermore, the missing data from the previously selected observation is replaced with the existing ones from the observation having all the data available.
Finally, the process continues until there is no more missing information.'''

def random_sample_imputation(df):
    # 미싱값 찾기 & 리스트 만들기
    cols_with_missing_values = df.columns[df.isna().any()].tolist()

    for var in cols_with_missing_values:

        # extract a random sample
        random_sample_df = df[var].dropna().sample(df[var].isnull().sum(),
                                                    random_state=0)
        # re-index the randomly extracted sample
        random_sample_df.index = df[
                df[var].isnull()].index

        # replace the NA
        df.loc[df[var].isnull(), var] = random_sample_df
    
    return df

# Multiple Imputation Method
'''This is a multivariate imputation technique, meaning that the missing information is 
filled by taking into consideration the information from the other columns. 
For instance, if the income value is missing for an individual, it is uncertain whether 
or not they have a mortgage. So, to determine the correct value, it is necessary 
to evaluate other characteristics such as credit score, occupation, and whether or not 
the individual owns a house.
Multiple Imputation by Chained Equations (MICE for short) is one of the most popular 
imputation methods in multivariate imputation. To better understand the MICE approach, 
let’s consider the set of variables X1, X2, … Xn, where some or all have missing values. 
The algorithm works as follows: 

For each variable, replace the missing value with a simple imputation strategy such as mean 
imputation, also considered as “placeholders.” The “placeholders” for the first variable, 
X1, are regressed by using a regression model where X1 is the dependent variable, and 
the rest of the variables are the independent variables. Then X2 is used as dependent 
variables and the rest as independent variables. The process continues as such until all 
the variables are considered at least once as the dependent variable. Those original 
“placeholders” are then replaced with the predictions from the regression model. The replacement 
process is repeated for a number of cycles which is generally ten, according to Raghunathan 
et al. 2002, and the imputation is updated at each cycle. At the end of the cycle, the missing 
values are ideally replaced with the prediction values that best reflect the relationships 
identified in the data.The implementation is performed using the miceforest library. 

First, we need to install the library using the pip.'''