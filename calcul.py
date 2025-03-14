import tkinter as tk
from tkinter import ttk
import random

class MentalMathTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Mental Math Trainer")
        self.root.geometry("550x450")
        self.root.resizable(False, False)
        
        self.correct_count = 0
        self.wrong_count = 0
        self.current_problem = {"num1": 0, "num2": 0, "operation": "", "answer": 0}
        
        self.division_stats = {
            2: {"correct": 0, "total": 0},
            3: {"correct": 0, "total": 0},
            4: {"correct": 0, "total": 0},
            5: {"correct": 0, "total": 0},
            6: {"correct": 0, "total": 0},
            7: {"correct": 0, "total": 0},
            8: {"correct": 0, "total": 0},
            9: {"correct": 0, "total": 0}
        }
        
        self.multiplication_stats = {
            2: {"correct": 0, "total": 0},
            3: {"correct": 0, "total": 0},
            4: {"correct": 0, "total": 0},
            5: {"correct": 0, "total": 0},
            6: {"correct": 0, "total": 0},
            7: {"correct": 0, "total": 0},
            8: {"correct": 0, "total": 0},
            9: {"correct": 0, "total": 0}
        }
        
        self.show_solution = tk.BooleanVar(value=False)
        self.exercise_type = tk.StringVar(value="division")
        
        # Create widgets
        self.create_widgets()
        
        self.generate_problem()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Exercise type selector
        exercise_frame = ttk.Frame(main_frame)
        exercise_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(exercise_frame, text="Exercise type:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 10))
        
        division_radio = ttk.Radiobutton(exercise_frame, text="Division", variable=self.exercise_type, value="division", command=self.generate_problem)
        division_radio.pack(side=tk.LEFT, padx=5)
        
        multiplication_radio = ttk.Radiobutton(exercise_frame, text="Multiplication", variable=self.exercise_type, value="multiplication", command=self.generate_problem)
        multiplication_radio.pack(side=tk.LEFT, padx=5)
        
        # Problem display
        self.problem_var = tk.StringVar()
        problem_label = ttk.Label(main_frame, textvariable=self.problem_var, font=("Arial", 30))
        problem_label.pack(pady=(20, 30))
        
        # Answer entry
        answer_frame = ttk.Frame(main_frame)
        answer_frame.pack(pady=10)
        
        ttk.Label(answer_frame, text="Your answer:", font=("Arial", 12)).pack(side=tk.LEFT, padx=(0, 10))
        
        self.answer_var = tk.StringVar()
        # Add trace to the StringVar to check answer automatically when value changes
        self.answer_var.trace_add("write", self.on_answer_change)
        
        self.answer_entry = ttk.Entry(answer_frame, textvariable=self.answer_var, font=("Arial", 12), width=10)
        self.answer_entry.pack(side=tk.LEFT)
        self.answer_entry.bind("<Return>", self.check_answer)
        
        submit_btn = ttk.Button(answer_frame, text="Submit", command=self.check_answer)
        submit_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Show/Hide solution checkbox
        solution_check = ttk.Checkbutton(main_frame, text="Show solution method", variable=self.show_solution, command=self.update_solution_visibility)
        solution_check.pack(pady=(10, 0))
        
        # Solution frame
        self.solution_frame = ttk.LabelFrame(main_frame, text="Solution method")
        self.solution_frame.pack(fill=tk.X, pady=10)
        
        self.solution_var = tk.StringVar()
        solution_label = ttk.Label(self.solution_frame, textvariable=self.solution_var, font=("Arial", 10), wraplength=450)
        solution_label.pack(pady=5, padx=5)
        
        # Stats frame
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill=tk.X, pady=10)
        
        # Correct/Wrong count
        count_frame = ttk.Frame(stats_frame)
        count_frame.pack(side=tk.LEFT, anchor=tk.W)
        
        self.correct_var = tk.StringVar(value="Correct: 0")
        self.wrong_var = tk.StringVar(value="Wrong: 0")
        
        ttk.Label(count_frame, textvariable=self.correct_var, font=("Arial", 10, "bold"), foreground="green").pack(anchor=tk.W)
        ttk.Label(count_frame, textvariable=self.wrong_var, font=("Arial", 10, "bold"), foreground="red").pack(anchor=tk.W)
        
        # Achievement notebooks
        self.achievement_notebook = ttk.Notebook(stats_frame)
        self.achievement_notebook.pack(side=tk.RIGHT, anchor=tk.E)
        
        # Division achievements tab
        division_tab = ttk.Frame(self.achievement_notebook)
        self.achievement_notebook.add(division_tab, text="Division")
        
        # Create division achievement labels
        self.division_vars = {}
        # First row: divisors 2-5
        div_row1_frame = ttk.Frame(division_tab)
        div_row1_frame.pack(anchor=tk.W)
        for i in range(2, 6):
            self.division_vars[i] = tk.StringVar(value=f"÷{i}: 0%")
            ttk.Label(div_row1_frame, textvariable=self.division_vars[i], font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        # Second row: divisors 6-9
        div_row2_frame = ttk.Frame(division_tab)
        div_row2_frame.pack(anchor=tk.W)
        for i in range(6, 10):
            self.division_vars[i] = tk.StringVar(value=f"÷{i}: 0%")
            ttk.Label(div_row2_frame, textvariable=self.division_vars[i], font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        # Multiplication achievements tab
        multiplication_tab = ttk.Frame(self.achievement_notebook)
        self.achievement_notebook.add(multiplication_tab, text="Multiplication")
        
        # Create multiplication achievement labels
        self.multiplication_vars = {}
        # First row: multipliers 2-5
        mul_row1_frame = ttk.Frame(multiplication_tab)
        mul_row1_frame.pack(anchor=tk.W)
        for i in range(2, 6):
            self.multiplication_vars[i] = tk.StringVar(value=f"×{i}: 0%")
            ttk.Label(mul_row1_frame, textvariable=self.multiplication_vars[i], font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        # Second row: multipliers 6-9
        mul_row2_frame = ttk.Frame(multiplication_tab)
        mul_row2_frame.pack(anchor=tk.W)
        for i in range(6, 10):
            self.multiplication_vars[i] = tk.StringVar(value=f"×{i}: 0%")
            ttk.Label(mul_row2_frame, textvariable=self.multiplication_vars[i], font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        # Next button
        next_btn = ttk.Button(main_frame, text="Next Problem", command=self.generate_problem)
        next_btn.pack(pady=(10, 0))

    def generate_problem(self):
        """Generate a new problem based on the selected exercise type."""
        # Reset answer field and focus
        self.answer_var.set("")
        self.answer_entry.focus()
        
        # Get current exercise type
        exercise_type = self.exercise_type.get()
        
        if exercise_type == "division":
            self.generate_division_problem()
        else:  # multiplication
            self.generate_multiplication_problem()
            
        # Update solution method
        self.update_solution_method()
        
        # Update solution visibility
        self.update_solution_visibility()
    
    def generate_division_problem(self):
        """Generate a division problem with natural number result."""
        # Choose divisor (2-9)
        divisor = random.randint(2, 9)
        
        # Generate answer first (max 200 to avoid numbers > 1000)
        answer = random.randint(1, 200)
        
        # Calculate dividend
        dividend = answer * divisor
        
        # Set current problem
        self.current_problem = {
            "num1": dividend,
            "num2": divisor,
            "operation": "division",
            "answer": answer
        }
        
        # Update problem display
        self.problem_var.set(f"{dividend} ÷ {divisor} = ?")
    
    def generate_multiplication_problem(self):
        """Generate a multiplication problem with two factors."""
        # First factor (2-9)
        factor1 = random.randint(2, 9)
        
        # Second factor (2-19)
        factor2 = random.randint(2, 9)
        
        # Calculate answer
        answer = factor1 * factor2
        
        # Set current problem
        self.current_problem = {
            "num1": factor1,
            "num2": factor2,
            "operation": "multiplication",
            "answer": answer
        }
        
        # Update problem display
        self.problem_var.set(f"{factor1} × {factor2} = ?")

    def update_solution_method(self):
        """Generate solution method based on the problem type."""
        operation = self.current_problem["operation"]
        
        if operation == "division":
            self.update_division_solution()
        else:  # multiplication
            self.update_multiplication_solution()
    
    def update_division_solution(self):
        """Generate solution method for division using approximation approach."""
        dividend = self.current_problem["num1"]
        divisor = self.current_problem["num2"]
        
        # Find nearest easy multiple
        base_multiple = (dividend // divisor) * divisor
        if abs((base_multiple + divisor) - dividend) < abs(base_multiple - dividend):
            base_multiple += divisor
        
        if base_multiple == dividend:
            # No approximation needed
            self.solution_var.set(f"{dividend} ÷ {divisor} = {dividend // divisor}")
            return
            
        # Calculate solution method
        diff = base_multiple - dividend
        solution = ""
        
        if diff > 0:  # We approximated up
            solution = f"{dividend} ÷ {divisor}:\n"
            solution += f"- Approximate to {base_multiple} (nearest easy multiple of {divisor})\n"
            solution += f"- {base_multiple} ÷ {divisor} = {base_multiple // divisor}\n"
            solution += f"- Difference: {base_multiple} - {dividend} = {diff}\n"
            solution += f"- {diff} ÷ {divisor} = {diff // divisor}\n"
            solution += f"- Result: {base_multiple // divisor} - {diff // divisor} = {self.current_problem['answer']}"
        else:  # We approximated down
            diff = abs(diff)
            solution = f"{dividend} ÷ {divisor}:\n"
            solution += f"- Approximate to {base_multiple} (nearest easy multiple of {divisor})\n"
            solution += f"- {base_multiple} ÷ {divisor} = {base_multiple // divisor}\n"
            solution += f"- Difference: {dividend} - {base_multiple} = {diff}\n"
            solution += f"- {diff} ÷ {divisor} = {diff // divisor}\n"
            solution += f"- Result: {base_multiple // divisor} + {diff // divisor} = {self.current_problem['answer']}"
        
        self.solution_var.set(solution)
    
    def update_multiplication_solution(self):
        """Generate solution method for multiplication using mental math strategies."""
        factor1 = self.current_problem["num1"]
        factor2 = self.current_problem["num2"]
        answer = self.current_problem["answer"]
        
        # Different strategies based on the factors
        solution = f"{factor1} × {factor2}:\n"
        
        # Strategy 1: Break down into tens and ones
        if factor2 > 10:
            tens = (factor2 // 10) * 10
            ones = factor2 % 10
            solution += f"Strategy 1: Break down into tens and ones\n"
            solution += f"- {factor1} × {tens} = {factor1 * tens}\n"
            solution += f"- {factor1} × {ones} = {factor1 * ones}\n"
            solution += f"- Add: {factor1 * tens} + {factor1 * ones} = {answer}\n\n"
        
        # Strategy 2: Round and adjust
        round_factor = 0
        if factor2 < 10:
            if factor2 < 5:
                round_factor = 5
            else:
                round_factor = 10
        else:
            if factor2 < 15:
                round_factor = 15
            else:
                round_factor = 20
        
        diff = round_factor - factor2
        round_result = factor1 * round_factor
        adjustment = factor1 * diff
        
        solution += f"Strategy 2: Round and adjust\n"
        if diff > 0:  # We rounded up
            solution += f"- Round {factor2} up to {round_factor}\n"
            solution += f"- {factor1} × {round_factor} = {round_result}\n"
            solution += f"- Adjustment: {factor1} × {diff} = {adjustment}\n"
            solution += f"- Subtract: {round_result} - {adjustment} = {answer}"
        else:  # We rounded down
            diff = abs(diff)
            adjustment = factor1 * diff
            solution += f"- Round {factor2} down to {round_factor}\n"
            solution += f"- {factor1} × {round_factor} = {round_result}\n"
            solution += f"- Adjustment: {factor1} × {diff} = {adjustment}\n"
            solution += f"- Add: {round_result} + {adjustment} = {answer}"
        
        self.solution_var.set(solution)

    def update_solution_visibility(self):
        """Update solution visibility based on checkbox."""
        if self.show_solution.get():
            self.solution_frame.pack(fill=tk.X, pady=10)
        else:
            self.solution_frame.pack_forget()

    def check_answer(self, event=None):
        """Check if the user's answer is correct."""
        try:
            user_answer = int(self.answer_var.get())
            correct_answer = self.current_problem["answer"]
            operation = self.current_problem["operation"]
            
            if operation == "division":
                factor = self.current_problem["num2"]  # divisor
                stats_dict = self.division_stats
                vars_dict = self.division_vars
                self.achievement_notebook.select(0)  # Select division tab
            else:  # multiplication
                factor = self.current_problem["num1"]  # first factor (2-9)
                stats_dict = self.multiplication_stats
                vars_dict = self.multiplication_vars
                self.achievement_notebook.select(1)  # Select multiplication tab
            
            if user_answer == correct_answer:
                self.correct_count += 1
                stats_dict[factor]["correct"] += 1
                result_text = "Correct!"
                self.answer_entry.config(foreground="green")
                self.root.after(50, self.generate_problem)
            else:
                self.wrong_count += 1
                result_text = f"Wrong! The answer is {correct_answer}"
                self.answer_entry.config(foreground="red")
                self.root.after(50, self.generate_problem)
                
            # Update factor stat
            stats_dict[factor]["total"] += 1
            
            # Update stats display
            self.update_stats(vars_dict, stats_dict)
            
        except ValueError:
            self.problem_var.set("Please enter a valid number")
            operation = self.current_problem["operation"]
            if operation == "division":
                display_text = f"{self.current_problem['num1']} ÷ {self.current_problem['num2']}"
            else:  # multiplication
                display_text = f"{self.current_problem['num1']} × {self.current_problem['num2']}"
            self.root.after(1500, lambda: self.problem_var.set(display_text))

    def on_answer_change(self, *args):
        """Called whenever the answer entry changes."""
        if len(self.answer_var.get()) > 0:
            try:
                # Only auto-check if the answer is an integer
                user_answer = int(self.answer_var.get())
                correct_answer = self.current_problem["answer"]
                
                # If correct, verify the answer
                if user_answer == correct_answer:
                    self.check_answer()
            except ValueError:
                # Not a valid integer yet, do nothing
                pass

    def update_stats(self, vars_dict=None, stats_dict=None):
        """Update the statistics display."""
        self.correct_var.set(f"Correct: {self.correct_count}")
        self.wrong_var.set(f"Wrong: {self.wrong_count}")
        
        # Update achievement percentages if specified
        if vars_dict and stats_dict:
            for factor, stats in stats_dict.items():
                if stats["total"] > 0:
                    percentage = round((stats["correct"] / stats["total"]) * 100)
                    if self.current_problem["operation"] == "division":
                        vars_dict[factor].set(f"÷{factor}: {percentage}%")
                    else:  # multiplication
                        vars_dict[factor].set(f"×{factor}: {percentage}%")

        # Update all division stats
        for divisor, stats in self.division_stats.items():
            if stats["total"] > 0:
                percentage = round((stats["correct"] / stats["total"]) * 100)
                self.division_vars[divisor].set(f"÷{divisor}: {percentage}%")
        
        # Update all multiplication stats
        for factor, stats in self.multiplication_stats.items():
            if stats["total"] > 0:
                percentage = round((stats["correct"] / stats["total"]) * 100)
                self.multiplication_vars[factor].set(f"×{factor}: {percentage}%")

if __name__ == "__main__":
    root = tk.Tk()
    app = MentalMathTrainer(root)
    root.mainloop()
