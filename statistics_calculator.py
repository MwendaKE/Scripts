import numpy as np
import statistics

class DataAnalyzer:
    """A class to analyze statistical properties of data"""
    
    def __init__(self, mean=10, std=5, num_samples=500):
        """Initialize with default or custom parameters"""
        self.mean = mean
        self.std = std
        self.num_samples = num_samples
        self.data = None
        self.data_list = None
        
    def generate_data(self):
        """Generate random data using normal distribution"""
        self.data = np.random.normal(loc=self.mean, scale=self.std, size=self.num_samples)
        self.data_list = self.data.tolist()
        return self.data
    
    def calculate_mode(self):
        """Calculate the mode of the data"""
        try:
            return statistics.mode(self.data_list)
        except statistics.StatisticsError:
            return "No mode"
    
    def calculate_basic_stats(self):
        """Calculate basic statistics: mean, median, variance, std"""
        if self.data is None:
            self.generate_data()
            
        return {
            "mean": np.mean(self.data),
            "median": np.median(self.data),
            "variance": np.var(self.data, ddof=1),  # ddof=1 for sample variance
            "std": np.std(self.data, ddof=1)  # ddof=1 for sample std
        }
    
    def calculate_quartiles(self):
        """Calculate quartiles (Q1, Q2, Q3)"""
        if self.data is None:
            self.generate_data()
            
        return {
            "Q1": np.percentile(self.data, 25),
            "Q2": np.percentile(self.data, 50),  # Equal to median
            "Q3": np.percentile(self.data, 75)
        }
    
    def calculate_deciles(self):
        """Calculate all deciles (10th, 20th, ..., 90th percentiles)"""
        if self.data is None:
            self.generate_data()
            
        return np.percentile(self.data, range(10, 100, 10))
    
    def calculate_percentiles(self, percentiles=None):
        """Calculate specific percentiles (default: common ones)"""
        if self.data is None:
            self.generate_data()
            
        if percentiles is None:
            percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]
            
        return np.percentile(self.data, percentiles)
    
    def print_report(self):
        """Generate and print a comprehensive statistical report"""
        if self.data is None:
            self.generate_data()
        
        # Calculate all statistics
        basic_stats = self.calculate_basic_stats()
        mode_value = self.calculate_mode()
        quartiles = self.calculate_quartiles()
        deciles = self.calculate_deciles()
        percentiles = self.calculate_percentiles()
        
        # Print results
        print("\n=== STATISTICAL ANALYSIS REPORT ===")
        print(f"\nDataset: {self.num_samples} samples from N(μ={self.mean}, σ={self.std})")
        
        print("\n--- Basic Statistics ---")
        print(f" > Mean = {basic_stats['mean']:.4f}")
        print(f" > Median = {basic_stats['median']:.4f}")
        print(f" > Mode = {mode_value}")
        print(f" > Variance = {basic_stats['variance']:.4f}")
        print(f" > Standard Deviation = {basic_stats['std']:.4f}")
        
        print("\n--- Quartiles ---")
        print(f" > 1st Quartile (Q1) = {quartiles['Q1']:.4f}")
        print(f" > 2nd Quartile (Q2/Median) = {quartiles['Q2']:.4f}")
        print(f" > 3rd Quartile (Q3) = {quartiles['Q3']:.4f}")
        
        print("\n--- Deciles ---")
        for i, decile in enumerate(deciles, 1):
            print(f"  • D{i} ({i*10}th percentile) = {decile:.4f}")
        
        print("\n--- Selected Percentiles ---")
        percentile_labels = [1, 5, 10, 25, 50, 75, 90, 95, 99]
        for label, value in zip(percentile_labels, percentiles):
            print(f"  • P{label} = {value:.4f}")
        
        print("\n" + "="*40)
        print("Note: 7th decile = 70th percentile, 8th decile = 80th percentile")


# Example usage
if __name__ == "__main__":
    # Create analyzer with default parameters
    analyzer = DataAnalyzer()
    
    # Generate and analyze data
    analyzer.print_report()
    
    # Example with custom parameters
    print("\n\n" + "="*50)
    print("CUSTOM DATASET ANALYSIS")
    print("="*50)
    
    custom_analyzer = DataAnalyzer(mean=15, std=3, num_samples=1000)
    custom_analyzer.print_report()