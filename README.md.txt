Route Optimization Project
Overview

This Python project calculates the shortest delivery route for multiple customers and generates a Google Maps link to visualize the optimized route. It is useful for logistics, delivery planning, and route optimization tasks.

Features

Read customer data from an Excel file (customers.xlsx)

Calculate distances between customers

Find the optimal route using OR-Tools

Generate a Google Maps link for the optimized route

Requirements

Python 3.x

Packages:

pandas

geopy

ortools

openpyxl

Install packages using:

pip install pandas geopy ortools openpyxl

How to Use

Prepare a customers.xlsx file with columns like: CustomerID, Name, Address, Latitude, Longitude, DeliveryWindow, PackageWeight.

Run the Python script:

python route_optimization.py


Check the terminal output and open the generated Google Maps link to view the optimized route.