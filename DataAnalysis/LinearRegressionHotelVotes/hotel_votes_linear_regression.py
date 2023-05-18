import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
import xlsxwriter

# Load the dataset
df = pd.read_excel('linear_regression_data.xlsx')

# Winsorize the data to remove extreme outliers
lower = df.quantile(0.05)
upper = df.quantile(0.95)
df = df.apply(lambda x: np.clip(x, lower[x.name], upper[x.name]))

# Calculate descriptive statistics
stats = pd.DataFrame({'Mean': df.mean(), 'Standard Deviation': df.std(), 'Range': df.max()-df.min()})
print(stats)


# Split the data into training and testing sets
X = df[['Customer Rating', 'Number of Words in Review', 'Number of Sentences in Review', 'Manager Response', 'Sustainabilty Score', 
        'Contributions']] # independent variables
y = df['Helpful Vote'] # dependent variable
# test_size=0.3 means that 30% of the data will be used for testing and the remaining 70% will be used for training.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Fit a linear regression model to the training data
X_train = sm.add_constant(X_train) # add constant term to the model
model = sm.OLS(y_train, X_train).fit()

# Evaluate the model on the testing data
X_test = sm.add_constant(X_test) # add constant term to the test data
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
# MSE stands for Mean Squared Error, which is a common metric used to evaluate the performance of a regression model. 
# It measures the average squared difference between the actual and predicted values of the target variable.
print('MSE:', mse)
# coefficient of determination, is a statistical measure that represents the proportion of variance in the dependent variable (y) 
# that is explained by the independent variables (X) in a regression model. 
print('R-squared:', r2)

# Print summary of the model to obtain p-values
print(model.summary())

# Identify the significant predictors
coefficients = pd.DataFrame(model.params, columns=['Coefficient'])
pvalues = model.pvalues
coefficients['p-values'] = pvalues
print(coefficients)

# Create a new Excel file
workbook = xlsxwriter.Workbook('linear_regression_results.xlsx')
worksheet = workbook.add_worksheet()

# Write the results to the Excel file
worksheet.write('A1', 'Independent Variable')
worksheet.write('B1', 'Coefficient')
worksheet.write('C1', 'p-value')
worksheet.write('D1', 'Significance')


# Coefficient is close to zero, we can set a threshold value and check if the absolute value of the coefficient is below that threshold.
for i, (name, coef, pvalue) in enumerate(zip(X.columns, model.params[1:], pvalues[1:])):
    # If the p-value is below 0.05, we can consider the independent variable to have a significant effect on the dependent variable.
    if pvalue < 0.05:
        effect = 'Significant predictor'
    else:
        effect = 'Little or no effect'
    worksheet.write(i+1, 0, name)
    worksheet.write(i+1, 1, coef)
    worksheet.write(i+1, 2, pvalue)
    worksheet.write(i+1, 3, effect)

# Write the model performance metrics to the worksheet
worksheet.write('A8', 'MSE')
worksheet.write('B8', mse)
worksheet.write('A9', 'R-squared')
worksheet.write('B9', r2)

workbook.close()

# Plot the actual vs. predicted values
plt.scatter(y_test, y_pred, alpha=0.5) # Alpha adjusts transparency of points
plt.plot(y_test, y_test, 'r-')
plt.xlabel('Actual Helpful Votes')
plt.ylabel('Predicted Helpful Votes')
plt.title('Linear Regression Model')

# add text to the plot
plt.text(50, 200, f'MSE = {mse:.2f}\nR-squared = {r2:.2f}', fontsize=12)
# add legend to the plot
plt.legend(['Predicted Values', 'Actual Values'], loc='upper left')
# Save graph as .png
plt.savefig('regression_plot.png')
plt.show()

# # can be answered with regression of the individual consumer review --- 
# # IV = the number of mentions of the indicative keywords of an online review, plus start rating, number of words, etc.
# #  (see some variable used in my other paper attached). DV = helpfulness votes an online review received. 
# #  (we can also use the mentions of sustainability keywords to predict “value” besides helpfulness votes)
# import pandas as pd
# import numpy as np
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error, r2_score
# import statsmodels.api as sm
# import xlsxwriter
# import matplotlib.pyplot as plt



# # Load the dataset
# df = pd.read_excel('linear_regression_data.xlsx')

# # Winsorize the data to remove extreme outliers
# lower = df.quantile(0.05)
# upper = df.quantile(0.95)
# df = df.apply(lambda x: np.clip(x, lower[x.name], upper[x.name]))


# # Split the data into training and testing sets
# X = df[['Customer Rating', 'Number of Words in Review', 'Number of Sentences in Review', 'Manager Response', 'Sustainabilty Score', 
#         'Contributions']] # independent variables
# y = df['Helpful Vote'] # dependent variable
# # test_size=0.3 means that 30% of the data will be used for testing and the remaining 70% will be used for training.
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# # Fit a linear regression model to the training data
# model = LinearRegression()
# model.fit(X_train, y_train)


# # Evaluate the model on the testing data
# y_pred = model.predict(X_test)
# mse = mean_squared_error(y_test, y_pred)
# r2 = r2_score(y_test, y_pred)
# # MSE stands for Mean Squared Error, which is a common metric used to evaluate the performance of a regression model. 
# # It measures the average squared difference between the actual and predicted values of the target variable.
# print('MSE:', mse)
# # coefficient of determination, is a statistical measure that represents the proportion of variance in the dependent variable (y) 
# # that is explained by the independent variables (X) in a regression model. 
# print('R-squared:', r2)


# # Identify the significant predictors
# coefficients = pd.DataFrame(model.coef_, X.columns, columns=['Coefficient'])
# print('COEFF', coefficients)
# significant_predictors = coefficients[coefficients['Coefficient'] != 0]
# print(significant_predictors)

# # Interpret the coefficients
# for name, coef in zip(X.columns, model.coef_):
#     print(f'{name}: {coef:.2f}')



# # Create a new Excel file
# workbook = xlsxwriter.Workbook('linear_regression_results.xlsx')
# worksheet = workbook.add_worksheet()

# # Write the results to the Excel file
# worksheet.write('A1', 'Independent Variable')
# worksheet.write('B1', 'Coefficient')
# worksheet.write('C1', 'Significance')
# # Coefficient is close to zero, we can set a threshold value and check if the absolute value of the coefficient is below that threshold.
# for i, (name, coef) in enumerate(zip(X.columns, model.coef_)):
#     # If it is below the threshold, we can consider the independent variable to have little or no effect on the dependent variable.
#     if abs(coef) < 0.1:
#         effect = 'Little or no effect'
#     else:
#         effect = 'Significant predictor'
#     worksheet.write(i+1, 0, name)
#     worksheet.write(i+1, 1, coef)
#     worksheet.write(i+1, 2, effect)

# worksheet.write('A8', 'MSE')
# worksheet.write('B8', mse)
# worksheet.write('A9', 'R-squared')
# worksheet.write('B9', r2)

# workbook.close()


# # Plot the actual vs. predicted values
# plt.scatter(y_test, y_pred, alpha=0.5) # Alpha adjusts transparency of points
# plt.plot(y_test, y_test, 'r-')
# plt.xlabel('Actual Helpful Votes')
# plt.ylabel('Predicted Helpful Votes')
# plt.title('Linear Regression Model')

# # # # Set the axis limits to increase the scale
# # # plt.xlim(0, 0.001)
# # # plt.ylim(0, 0.001)


# # add text to the plot
# plt.text(50, 200, f'MSE = {mse:.2f}\nR-squared = {r2:.2f}', fontsize=12)
# # add legend to the plot
# plt.legend(['Predicted Values', 'Actual Values'], loc='upper left')
# # Save graph as .png
# plt.savefig('regression_plot.png')
# plt.show()

# # # Make predictions on new data
# # new_data = pd.DataFrame({'Customer Rating': [1, 2, 3], 'Number of Words in Review': [4, 5, 6], 'Number of Sentences in Review': [7, 8, 9], 
# #                          'Manager Response': [10, 11, 12], 'Sustainabilty Score': [13, 14, 15]})
# # predictions = model.predict(new_data)
# # print(predictions)



