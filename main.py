import pandas as pd
import numpy as np
import statsmodels.api as sm
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from datetime import date
from scipy import stats

def select_file():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        file_entry.delete(0, END)
        file_entry.insert(0, file_path)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def toggle_current_date():
    if current_date_check.get():
        current_date_frame.pack(before=end_date_frame)
    else:
        current_date_frame.pack_forget()

def calculate_mileage_forecast():
    try:
        file_path = file_entry.get()
        if not file_path:
            raise ValueError("Please select an input data file.")
        
        # Read the input data from xlsx file
        data = pd.read_excel(file_path)
        if data.empty:
            raise ValueError("Input data is empty.")
        
        # Determine the remaining lease days
        end_date = end_date_entry.get()
        current_date = date.today().strftime("%Y-%m-%d")
        if current_date_check.get():
            if not current_date_entry.get():
                raise ValueError("Please enter the current date.")
            else:
                current_date = current_date_entry.get()
        if not end_date:
            raise ValueError("Please enter the lease end date.")
        remaining_lease_days = (pd.to_datetime(end_date) - pd.to_datetime(current_date)).days
        if remaining_lease_days <= 0:
            raise ValueError("Lease end date should be in the future.")
        filtered_data = data[pd.to_datetime(data['Date']) <= pd.to_datetime(end_date)]
        
        # Calculate the average daily mileage
        avg_daily_mileage = filtered_data['Miles Traveled'].mean()
        
        # Handle outliers using interquartile range (IQR)
        q1 = filtered_data['Miles Traveled'].quantile(0.25)
        q3 = filtered_data['Miles Traveled'].quantile(0.75)
        iqr = q3 - q1
        
        lower_bound = q1 - 0.1 * iqr
        upper_bound = q3 + 0.1 * iqr
        filtered_data['Miles Traveled'] = np.where((filtered_data['Miles Traveled'] < lower_bound) | (filtered_data['Miles Traveled'] > upper_bound), avg_daily_mileage, filtered_data['Miles Traveled'])
        
        # Fit an ARIMA model to the historical mileage data
        model = sm.tsa.ARIMA(filtered_data['Miles Traveled'], order=(1, 0, 0))
        model_fit = model.fit()
        
        # Generate a forecast for the remaining lease period
        forecast = model_fit.predict(start=len(filtered_data), end=len(filtered_data) + remaining_lease_days - 1)
        
        # Calculate the accuracy probability
        residuals = np.subtract(data['Miles Traveled'], model_fit.predict(start=0, end=len(data) - 1))
        mean_residuals = np.mean(residuals)
        std_residuals = np.std(residuals)

        z_score = abs(mean_residuals / std_residuals)
        
        accuracy_probability = (1 - stats.norm.cdf(abs(z_score))) * 2 * 100 if len(data) > 30 else 50
        
        # Display the result in the user interface
        if accuracy_probability >= 90:
            result_label.config(text=f"Forecasted Total Mileage: {forecast.sum() + data['Odometer - End'][len(data) - 1]:.2f} miles*")
        else:
            result_label.config(text=f"Forecasted Total Mileage: {forecast.sum() + data['Odometer - End'][len(data) - 1]:.2f} miles")
        accuracy_label.config(text=f"Accuracy Probability: {accuracy_probability:.4f}%")
        
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the user interface
root = Tk()
root.title("Mileage Forecast")
root.geometry("400x250")

# Style the user interface
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12))

file_frame = Frame(root, pady=10)
file_frame.pack()

file_label = Label(file_frame, text="Input Data File:")
file_label.pack(side=LEFT, padx=5)
file_entry = Entry(file_frame, width=30)
file_entry.pack(side=LEFT)
select_button = Button(file_frame, text="Select File", command=select_file)
select_button.pack(side=LEFT)

current_date_check = BooleanVar()
current_date_check.set(TRUE)
current_date_checkbutton = Checkbutton(root, text="Set Current Date", variable=current_date_check, command=toggle_current_date)
current_date_checkbutton.pack()

current_date_frame = Frame(root, pady=3)
current_date_frame.pack()

current_date_label = Label(current_date_frame, text="Current Date:")
current_date_label.pack(side=LEFT, padx=10)
current_date_entry = Entry(current_date_frame)
current_date_entry.pack(side=LEFT, padx=3)

end_date_frame = Frame(root, pady=3)
end_date_frame.pack()

end_date_label = Label(end_date_frame, text="Lease End Date:")
end_date_label.pack(side=LEFT, padx=5)
end_date_entry = Entry(end_date_frame)
end_date_entry.pack(side=LEFT, padx=3)

calculate_button = Button(root, text="Calculate", command=calculate_mileage_forecast)
calculate_button.pack()

result_label = Label(root, text="")
result_label.pack()

accuracy_label = Label(root, text="")
accuracy_label.pack()

root.mainloop()