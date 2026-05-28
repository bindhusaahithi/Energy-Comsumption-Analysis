"""Compatibility package for deployment tooling.

Streamlit Cloud's Poetry-based build expects a package name derived from the
project name `energy-consumption-analysis`, which maps to the import path
`energy_consumption_analysis`. The app code lives in `energy_analytics`, so
this shim keeps packaging happy without changing the project structure.
"""

