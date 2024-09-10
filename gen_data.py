import csv
import random
import math
import numpy as np

B_5g = 20 # Bandwidth in MHz
B_wifi = 20
B_lifi = 10

class WirelessLink:
    def __init__(self, technology):
        self.technology = technology
        self.snr = None
        self.delay = None
        self.transmit_data_rate = None
        self.throughput = None
        self.capacity = None
        
    def simulate_link(self):
        # Simulate link parameters based on the technology
        if self.technology == '5G':
            self.snr = np.random.uniform(5, 55)  # Example: SNR in dB
            self.delay = np.random.uniform(1, 10)  # Example: Delay in milliseconds
            self.capacity = calculate_capacity(B_5g, self.snr)
            self.transmit_data_rate =  np.random.uniform(1, 500) 
        elif self.technology == 'WiFi':
            prob_distribution = np.exp(-np.arange(10, 50 + 1) / 10.0)
            prob_distribution /= prob_distribution.sum()  # 归一化确保概率和为1
            self.snr = np.random.choice(np.arange(10, 50 + 1),  p=prob_distribution)
            # self.snr = np.random.uniform(5, 20)
            self.delay = np.random.uniform(2, 13)
            self.capacity = calculate_capacity(B_wifi, self.snr)
            self.transmit_data_rate =  np.random.uniform(1, 400) 
        elif self.technology == 'LiFi':
            prob_distribution = np.exp(-np.arange(5, 45 + 1) / 10.0)
            prob_distribution /= prob_distribution.sum()  # 归一化确保概率和为1
            self.snr = np.random.choice(np.arange(5, 50 + 1), p=prob_distribution)
            self.delay = np.random.uniform(5, 15)
            self.capacity = calculate_capacity(B_lifi, self.snr)
            self.transmit_data_rate =  np.random.uniform(1, 200) 
        
        # Calculate throughput (Example: Assuming a simple formula)
        if self.snr < 15:
            self.throughput = 0
        else:
            self.throughput = min (self.transmit_data_rate, self.capacity)/ (1 + self.delay)
            
        
def calculate_capacity(B, SNR_dB):
    # 将信噪比从dBm转换为普通比例
    SNR = 10**(SNR_dB / 10.0)
    
    # 计算信道容量
    C = B * math.log2(1 + SNR)
    
    return C

def generate_multipath_data(num_entries):
    data = []
    link_5g = WirelessLink('5G')
    link_wifi = WirelessLink('WiFi')
    link_lifi = WirelessLink('LiFi')
    for _ in range(num_entries):
        time = _  # You can replace this with the actual timestamp logic
        # Simulate link parameters based on the technology
        #5G
        snr_5g = np.random.uniform(5, 55)  # Example: SNR in dB
        delay_5g = np.random.uniform(1, 10)  # Example: Delay in milliseconds
        capacity_5g = calculate_capacity(B_5g, snr_5g)
        data_rate_5g =  np.random.uniform(0, 500) 
        if snr_5g < 15:
            throughput_5g = 0
        else:
            throughput_5g = min (data_rate_5g, capacity_5g)/ (1 + delay_5g)
        #WiFi
        prob_distribution_wifi = np.exp(-np.arange(10, 50 + 1) / 10.0)
        prob_distribution_wifi /= prob_distribution_wifi.sum()  # 归一化确保概率和为1
        snr_wifi = np.random.choice(np.arange(10, 50 + 1),  p=prob_distribution_wifi)
        # self.snr = np.random.uniform(5, 20)
        delay_wifi = np.random.uniform(2, 13)
        capacity_wifi = calculate_capacity(B_wifi, snr_wifi)
        data_rate_wifi =  np.random.uniform(0, 400) 
        if snr_wifi < 15:
            throughput_wifi = 0
        else:
            throughput_wifi = min (data_rate_wifi, capacity_wifi)/ (1 + delay_wifi)
        #LiFi
        prob_distribution_lifi = np.exp(-np.arange(5, 40 + 1) / 10.0)
        prob_distribution_lifi /= prob_distribution_lifi.sum()  # 归一化确保概率和为1
        snr_lifi = np.random.choice(np.arange(5, 40 + 1), p=prob_distribution_lifi)
        delay_lifi = np.random.uniform(5, 15)
        capacity_lifi = calculate_capacity(B_lifi, snr_lifi)
        data_rate_lifi =  np.random.uniform(0, 200) 
        if snr_lifi < 15:
            throughput_lifi = 0
        else:
            throughput_lifi = min (data_rate_lifi, capacity_lifi)/ (1 + delay_lifi)

        row = [time, snr_5g, snr_wifi, snr_lifi, delay_5g, delay_wifi, delay_lifi,
               data_rate_5g, data_rate_wifi, data_rate_lifi, throughput_5g, throughput_wifi, throughput_lifi]

        data.append(row)

    return data

def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ["Time", "SNR_5G", "SNR_WiFi", "SNR_LiFi", "Delay_5G", "Delay_WiFi", "Delay_LiFi",
                      "DataRate_5G", "DataRate_WiFi", "DataRate_LiFi", "Throughput_5G", "Throughput_WiFi", "Throughput_LiFi"]

        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        writer.writerows(data)

if __name__ == "__main__":
    num_entries = 100000  # Replace with the desired number of entries
    output_filename = "multipath_data.csv"

    data = generate_multipath_data(num_entries)
    write_to_csv(data, output_filename)
    print(f"CSV file '{output_filename}' generated successfully.")