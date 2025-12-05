# Taximetro (v1.0.0)

A simple command-line taximeter that tracks trip states, calculates fare based on duration, and validates user input.

## Features

- Start/stop/move/arrive trip flow
- Time-based fare calculation  
  - Moving: €0.05 per second  
  - Stopped: €0.02 per second
- Input validation (Y/N and options 1–3)
- Clear state transitions (prev → curr)
- Clean, modular logic for future expansion
