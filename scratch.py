"""
This is a scratch file generated for rough scripts
"""

# testing a widget

from ipywidgets import interact, FloatSlider

# Create a simple test function that will display the slider value
def test_widget(x):
    print(f"Slider value: {x}")

# Create a slider widget using ipywidgets
slider = FloatSlider(min=0, max=10, step=0.1, value=5)

# Use the interact function to link the slider to the test function
interact(test_widget, x=slider)

