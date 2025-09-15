'''
Generates secure passwords by intelligently 
combining username variations with random 
characters while ensuring minimum length requirements.
'''

import string
import random

class PasswordGenerator:
    """Generates secure random passwords with username integration"""
    
    def __init__(self, min_length=8):
        self.min_length = min_length
        self.special_chars = "&#!_@-$%=£"
    
    def mix_name_case(self, name):
        """Alternate case for each character in name"""
        return ''.join(char.upper() if i % 2 else char.lower() 
                      for i, char in enumerate(name))
    
    def generate_password(self, username):
        """Generate a secure password incorporating the username"""
        # Apply random case transformation to username
        case_options = [
            username.upper,
            username.lower,
            username.capitalize,
            lambda: self.mix_name_case(username)
        ]
        username = random.choice(case_options)()
        
        # Ensure password meets minimum length requirement
        if len(username) < self.min_length:
            needed_chars = self.min_length - len(username)
            extra_chars = random.choices(string.digits + string.ascii_letters + self.special_chars, 
                                        k=needed_chars)
            password = username + ''.join(extra_chars)
        else:
            password = username
        
        # Add mandatory character types if missing
        char_types = {
            'digit': string.digits,
            'upper': string.ascii_uppercase,
            'special': self.special_chars
        }
        
        for char_type, chars in char_types.items():
            if not any(c in chars for c in password):
                password += random.choice(chars)
        
        # Shuffle for randomness
        password_list = list(password)
        random.shuffle(password_list)
        
        return ''.join(password_list)


def main():
    generator = PasswordGenerator()
    
    print("\nSecure Password Generator")
    print("-------------------------")
    
    while True:
        print()
        username = input(" > Enter Your First/Last Name: ").strip()
        
        if not username:
            print("Please enter a valid name.")
            continue
            
        print("\n > Suggested Passwords:")
        print()
        
        for i in range(10):
            password = generator.generate_password(username)
            print(f"   {i+1:2d}. {password}")
        
        print()
        again = input(" > Generate more passwords? (y/n): ").lower()
        if again != 'y':
            print("Stay secure! Goodbye!")
            break


if __name__ == "__main__":
    main()