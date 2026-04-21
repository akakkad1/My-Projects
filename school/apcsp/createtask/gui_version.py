from nicegui import ui

# --- YOUR ORIGINAL DICTIONARY & LOGIC (UNCHANGED) ---
gpa_points = {
    "a": 4,
    "b": 3,
    "c": 2,
    "d": 1,
    "f": 0
}

def calculate_grades(regulars, apibs, is_weighted):
    grade_points = [] 
    for grade in regulars:
        grade_points.append(gpa_points[grade])

    for grade in apibs:
        points = gpa_points[grade]
        if is_weighted and grade != "f":
            points += 1
        grade_points.append(points)
        
    final_gpa = sum(grade_points) / len(grade_points)
    return final_gpa

# --- UI STATE & HELPERS ---
letter_options = ['A', 'B', 'C', 'D', 'F']
apib_inputs = []
regular_inputs = []

def generate_fields():
    """Generates the input dropdowns based on the counts provided."""
    apib_container.clear()
    regular_container.clear()
    apib_inputs.clear()
    regular_inputs.clear()
    
    with apib_container:
        if apib_count.value > 0:
            ui.label('AP/IB Grades').classes('text-bold mt-4')
            for i in range(int(apib_count.value)):
                sel = ui.select(letter_options, label=f'AP/IB Course {i+1}')
                apib_inputs.append(sel)
                
    with regular_container:
        if (total_count.value - apib_count.value) > 0:
            ui.label('Regular Grades').classes('text-bold mt-4')
            for i in range(int(total_count.value - apib_count.value)):
                sel = ui.select(letter_options, label=f'Regular Course {i+1}')
                regular_inputs.append(sel)

def run_calculation():
    """Extracts values from UI and runs your original function."""
    try:
        # Convert UI selections to lowercase lists to match your logic
        reg_grades = [sel.value.lower() for sel in regular_inputs if sel.value]
        ap_grades = [sel.value.lower() for sel in apib_inputs if sel.value]
        
        if len(reg_grades) + len(ap_grades) == 0:
            ui.notify('Please select grades first!', color='negative')
            return

        w_gpa = calculate_grades(reg_grades, ap_grades, True)
        uw_gpa = calculate_grades(reg_grades, ap_grades, False)
        
        result_label.set_text(f'Weighted: {round(w_gpa, 2)} | Unweighted: {round(uw_gpa, 2)}')
    except Exception as e:
        ui.notify(f'Error: {e}', color='negative')

# --- MAIN UI LAYOUT ---
with ui.card().classes('w-96 mx-auto mt-10 shadow-lg'):
    ui.label('GPA Calculator').classes('text-h5 mb-2')
    
    with ui.row().classes('w-full'):
        total_count = ui.number('Total Courses', value=1, min=1, on_change=generate_fields).classes('w-20')
        apib_count = ui.number('AP/IB Count', value=0, min=0, on_change=generate_fields).classes('w-20')

    # Containers for the dynamic dropdowns
    apib_container = ui.column().classes('w-full')
    regular_container = ui.column().classes('w-full')
    
    ui.separator().classes('my-4')
    
    ui.button('Calculate GPA', on_click=run_calculation).classes('w-full')
    result_label = ui.label('').classes('text-h6 text-center text-primary mt-2')

# Initialize fields for the default values
generate_fields()

ui.run(title='GPA Calc')