import numpy as np
import statistics

class DataAnalyzer:
    """A class to analyze statistical properties of data using various distributions"""
    
    def __init__(self, distribution_type="normal", mean=10, std=5, num_samples=500, 
                 low=0, high=100, lam=5, n=10, p=0.5):
        """Initialize with distribution parameters"""
        self.distribution_type = distribution_type
        self.mean = mean
        self.std = std
        self.num_samples = num_samples
        self.low = low
        self.high = high
        self.lam = lam  # lambda for Poisson
        self.n = n      # number of trials for Binomial
        self.p = p      # probability of success for Binomial
        self.data = None
        self.data_list = None
        
    def generate_data(self):
        """Generate random data using the selected distribution"""
        if self.distribution_type == "normal":
            self.data = np.random.normal(loc=self.mean, scale=self.std, size=self.num_samples)
        elif self.distribution_type == "uniform":
            self.data = np.random.uniform(low=self.low, high=self.high, size=self.num_samples)
        elif self.distribution_type == "exponential":
            self.data = np.random.exponential(scale=self.mean, size=self.num_samples)
        elif self.distribution_type == "poisson":
            self.data = np.random.poisson(lam=self.lam, size=self.num_samples)
        elif self.distribution_type == "binomial":
            self.data = np.random.binomial(n=self.n, p=self.p, size=self.num_samples)
        else:
            raise ValueError("Unknown distribution type")
            
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
            "variance": np.var(self.data, ddof=1),
            "std": np.std(self.data, ddof=1)
        }
    
    def calculate_quartiles(self):
        """Calculate quartiles (Q1, Q2, Q3)"""
        if self.data is None:
            self.generate_data()
            
        return {
            "Q1": np.percentile(self.data, 25),
            "Q2": np.percentile(self.data, 50),
            "Q3": np.percentile(self.data, 75)
        }
    
    def calculate_deciles(self):
        """Calculate all deciles (10th, 20th, ..., 90th percentiles)"""
        if self.data is None:
            self.generate_data()
            
        return np.percentile(self.data, range(10, 100, 10))
    
    def calculate_percentiles(self, percentiles=None):
        """Calculate specific percentiles"""
        if self.data is None:
            self.generate_data()
            
        if percentiles is None:
            percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]
            
        return np.percentile(self.data, percentiles)
    
    def display_distribution_menu(self):
        """Display the distribution selection menu"""
        print("\n=== SELECT DISTRIBUTION TYPE ===")
        print("1. Normal Distribution (Bell Curve)")
        print("2. Uniform Distribution (All values equally likely)")
        print("3. Exponential Distribution (Time between events)")
        print("4. Poisson Distribution (Count data)")
        print("5. Binomial Distribution (Success/Failure outcomes)")
        print("6. Keep current distribution")
    
    def display_analysis_menu(self):
        """Display the analysis options menu"""
        print(f"\n=== STATISTICAL ANALYSIS OPTIONS ({self.distribution_type.upper()} DISTRIBUTION) ===")
        print("1. Basic Statistics (Mean, Median, Mode, Variance, Std)")
        print("2. Quartiles (Q1, Q2, Q3)")
        print("3. Deciles (D1 to D9)")
        print("4. Percentiles (P1, P5, P10, P25, P50, P75, P90, P95, P99)")
        print("5. Full Report (All statistics)")
        print("6. Change Distribution Type")
        print("7. Change Distribution Parameters")
        print("8. Exit")
    
    def get_distribution_parameters(self):
        """Get parameters for the selected distribution"""
        print(f"\nCurrent distribution: {self.distribution_type}")
        
        if self.distribution_type == "normal":
            self.mean = float(input(f"Enter mean (default {self.mean}): ") or self.mean)
            self.std = float(input(f"Enter standard deviation (default {self.std}): ") or self.std)
            
        elif self.distribution_type == "uniform":
            self.low = float(input(f"Enter lower bound (default {self.low}): ") or self.low)
            self.high = float(input(f"Enter upper bound (default {self.high}): ") or self.high)
            
        elif self.distribution_type == "exponential":
            self.mean = float(input(f"Enter scale (mean, default {self.mean}): ") or self.mean)
            
        elif self.distribution_type == "poisson":
            self.lam = float(input(f"Enter lambda (mean, default {self.lam}): ") or self.lam)
            
        elif self.distribution_type == "binomial":
            self.n = int(input(f"Enter number of trials (default {self.n}): ") or self.n)
            self.p = float(input(f"Enter probability of success (default {self.p}): ") or self.p)
        
        self.num_samples = int(input(f"Enter number of samples (default {self.num_samples}): ") or self.num_samples)
        self.data = None  # Reset data to regenerate with new parameters
        
        print(f"Parameters set for {self.distribution_type} distribution")
    
    def run_analysis(self):
        """Main method to run the interactive analysis"""
        print("Welcome to the Statistical Data Analyzer!")
        print("This tool generates random data and calculates various statistics.")
        
        # First, let user choose distribution type
        self.choose_distribution()
        
        while True:
            self.display_analysis_menu()
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if self.data is None:
                self.generate_data()
                print(f"\nGenerated {self.num_samples} samples from {self.distribution_type} distribution")
            
            if choice == "1":
                self.show_basic_stats()
            elif choice == "2":
                self.show_quartiles()
            elif choice == "3":
                self.show_deciles()
            elif choice == "4":
                self.show_percentiles()
            elif choice == "5":
                self.show_full_report()
            elif choice == "6":
                self.choose_distribution()
            elif choice == "7":
                self.get_distribution_parameters()
            elif choice == "8":
                print("Thank you for using the Statistical Data Analyzer!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 8.")
            
            # Ask if user wants to continue
            if choice != "8":
                cont = input("\nWould you like to perform another analysis? (y/n): ").strip().lower()
                if cont != 'y':
                    print("Thank you for using the Statistical Data Analyzer!")
                    break
    
    def choose_distribution(self):
        """Let user choose distribution type"""
        self.display_distribution_menu()
        dist_choice = input("\nSelect distribution type (1-6): ").strip()
        
        distributions = {
            "1": "normal",
            "2": "uniform", 
            "3": "exponential",
            "4": "poisson",
            "5": "binomial"
        }
        
        if dist_choice in distributions:
            self.distribution_type = distributions[dist_choice]
            print(f"Selected {self.distribution_type} distribution")
            self.get_distribution_parameters()
        elif dist_choice == "6":
            print("Keeping current distribution type")
        else:
            print("Invalid choice. Using normal distribution.")
            self.distribution_type = "normal"
    
    def show_basic_stats(self):
        """Display basic statistics"""
        print("\n--- Basic Statistics ---")
        stats = self.calculate_basic_stats()
        mode_val = self.calculate_mode()
        print(f"Mean = {stats['mean']:.4f}")
        print(f"Median = {stats['median']:.4f}")
        print(f"Mode = {mode_val}")
        print(f"Variance = {stats['variance']:.4f}")
        print(f"Standard Deviation = {stats['std']:.4f}")
    
    def show_quartiles(self):
        """Display quartiles"""
        print("\n--- Quartiles ---")
        quartiles = self.calculate_quartiles()
        print(f"1st Quartile (Q1) = {quartiles['Q1']:.4f}")
        print(f"2nd Quartile (Q2/Median) = {quartiles['Q2']:.4f}")
        print(f"3rd Quartile (Q3) = {quartiles['Q3']:.4f}")
    
    def show_deciles(self):
        """Display deciles"""
        print("\n--- Deciles ---")
        deciles = self.calculate_deciles()
        for i, decile in enumerate(deciles, 1):
            print(f"D{i} ({i*10}th percentile) = {decile:.4f}")
    
    def show_percentiles(self):
        """Display percentiles"""
        print("\n--- Percentiles ---")
        percentiles = self.calculate_percentiles()
        percentile_labels = [1, 5, 10, 25, 50, 75, 90, 95, 99]
        for label, value in zip(percentile_labels, percentiles):
            print(f"P{label} = {value:.4f}")
    
    def show_full_report(self):
        """Display full statistical report"""
        print(f"\n=== FULL STATISTICAL REPORT ({self.distribution_type.upper()} DISTRIBUTION) ===")
        print(f"Dataset: {self.num_samples} samples")
        
        # Basic stats
        self.show_basic_stats()
        
        # Quartiles
        self.show_quartiles()
        
        # Deciles
        self.show_deciles()
        
        # Percentiles
        self.show_percentiles()


# Run the analysis
if __name__ == "__main__":
    analyzer = DataAnalyzer()
    analyzer.run_analysis()