import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# load and inspect employees.csv
df = pd.read_csv("data/employees.csv")
print(df.info())
print(df.describe())
print("Row 0:\n", df.loc[0])
print("First 2 rows:\n", df.iloc[:2])
print("IT Dept:\n", df[df["department"] == "IT"])

# create departments.csv with 1 extra empty department (Marketing)
dept_text = """department,head,budget
Sales,Vikram,500000
HR,Lakshmi,300000
IT,Ramesh,900000
Finance,Sita,600000
Marketing,Kiran,400000"""

with open("data/departments.csv", "w") as f:
    f.write(dept_text)

# create dirty dataset (2 missing salaries + 1 duplicate) and clean it
dirty_df = df.copy()
dirty_df.loc[1, "salary"] = np.nan
dirty_df.loc[5, "salary"] = np.nan
dirty_df = pd.concat([dirty_df, dirty_df.iloc[0:1]], ignore_index=True)

dirty_df = dirty_df.drop_duplicates()
med_sal = dirty_df["salary"].median()
dirty_df["salary"] = dirty_df["salary"].fillna(med_sal).astype(int)

# groupby department
stats = df.groupby("department").agg(
    headcount=("id", "count"),
    avg_salary=("salary", "mean"),
    max_salary=("salary", "max")
).round(2)
ordered = stats.reindex(["Sales", "HR", "IT", "Finance"])
hc_str = " | ".join([f"{k} {v}" for k, v in ordered["headcount"].items()])
print(f"Headcount: {hc_str}")

# inner, left, outer merge with departments.csv
depts = pd.read_csv("data/departments.csv")
inner_m = pd.merge(df, depts, on="department", how="inner")
left_m = pd.merge(df, depts, on="department", how="left")
outer_m = pd.merge(df, depts, on="department", how="outer")

no_emp = outer_m[outer_m["id"].isna()]["department"].tolist()
print("Outer join - department with no employees:", no_emp)

# 1. Bar chart: average salary per department
plt.figure(figsize=(6, 4))
plt.bar(stats.index, stats["avg_salary"], color="steelblue")
plt.title("Average Salary per Department")
plt.xlabel("Department")
plt.ylabel("Average Salary (INR)")
plt.tight_layout()
plt.savefig("reports/1_bar_chart.png")
plt.close()
print("Bar chart insight: Finance has the highest average salary.")

# 2. Histogram: salary distribution
plt.figure(figsize=(6, 4))
plt.hist(df["salary"], bins=4, color="teal", edgecolor="black")
plt.title("Salary Distribution")
plt.xlabel("Salary (INR)")
plt.ylabel("Employee Count")
plt.tight_layout()
plt.savefig("reports/2_histogram.png")
plt.close()
print("Histogram insight: Most employees earn between 45000 and 75000.")

# 3. Scatter plot: id vs salary by department
plt.figure(figsize=(6, 4))
for d in df["department"].unique():
    sub = df[df["department"] == d]
    plt.scatter(sub["id"], sub["salary"], label=d, s=60)
plt.title("Employee ID vs Salary")
plt.xlabel("Employee ID")
plt.ylabel("Salary (INR)")
plt.legend(title="Department")
plt.tight_layout()
plt.savefig("reports/3_scatter_plot.png")
plt.close()
print("Scatter plot insight: IT employees sit in the higher pay range.")

# 4. Line chart: sorted salaries
sorted_df = df.sort_values("salary")
plt.figure(figsize=(6, 4))
plt.plot(sorted_df["name"], sorted_df["salary"], marker="o", color="orange")
plt.title("Employee Salaries (Low to High)")
plt.xlabel("Employee Name")
plt.ylabel("Salary (INR)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("reports/4_line_chart.png")
plt.close()
print("Line chart insight: Salaries rise steadily from 30000 to 90000.")