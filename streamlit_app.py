import math
import matplotlib.pyplot as plt

# Constants for conversion
INCH_TO_CM = 2.54
LB_TO_KG = 0.453592

def calculate_best_carton(product_dims, product_weight):
    max_carton_side = 25  # inches
    max_carton_weight = 50  # lbs
    max_units_per_carton = 150  # Amazon limit per carton

    product_length, product_width, product_height = product_dims

    best_carton = None
    max_units_carton = 0
    best_carton_weight = 0
    packing_config = None

    # Iterate over all possible carton dimensions
    for carton_length in range(math.ceil(product_length), max_carton_side + 1):
        for carton_width in range(math.ceil(product_width), max_carton_side + 1):
            for carton_height in range(math.ceil(product_height), max_carton_side + 1):
                # Calculate units per carton
                units_length = carton_length // product_length
                units_width = carton_width // product_width
                units_height = carton_height // product_height
                total_units = units_length * units_width * units_height
                carton_weight = total_units * product_weight

                # Check constraints
                if carton_weight > max_carton_weight or total_units > max_units_per_carton or total_units <= 1:
                    continue

                # Update the best carton configuration
                if total_units > max_units_carton:
                    max_units_carton = total_units
                    best_carton = (carton_length, carton_width, carton_height)
                    best_carton_weight = carton_weight
                    packing_config = (int(units_length), int(units_width), int(units_height))

    return {
        "best_carton": best_carton,
        "max_units_carton": max_units_carton,
        "best_carton_weight": best_carton_weight,
        "packing_config": packing_config
    }

def plot_carton_2d(carton_dims, packing_config, product_dims, title):
    carton_length, carton_width, carton_height = carton_dims
    units_length, units_width, units_height = packing_config
    product_length, product_width, product_height = product_dims

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title(title)
    ax.set_xlabel("Length (inches)")
    ax.set_ylabel("Width (inches)")

    # Draw the carton boundary
    ax.plot([0, carton_length, carton_length, 0, 0], [0, 0, carton_width, carton_width, 0], 'k-', lw=2)

    # Draw the products inside the carton (2D top-down view)
    for i in range(units_length):
        for j in range(units_width):
            x = i * product_length
            y = j * product_width
            ax.add_patch(plt.Rectangle((x, y), product_length, product_width, edgecolor='blue', facecolor='cyan', alpha=0.5))

    ax.set_xlim(0, carton_length)
    ax.set_ylim(0, carton_width)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def main():
    print("Welcome to the Amazon Master Carton Optimizer!")
    try:
        # Get user inputs
        product_length = float(input("Enter the product length (in inches): "))
        product_width = float(input("Enter the product width (in inches): "))
        product_height = float(input("Enter the product height (in inches): "))
        product_weight = float(input("Enter the product weight (in lbs): "))

        # Calculate the best carton configuration
        results = calculate_best_carton(
            (product_length, product_width, product_height),
            product_weight
        )

        if results["best_carton"]:
            # Convert results to cm and kg
            best_carton_cm = tuple(dim * INCH_TO_CM for dim in results["best_carton"])
            best_carton_weight_kg = results["best_carton_weight"] * LB_TO_KG

            # Output the best carton configuration
            print("\nBest Master Carton Size (inches):")
            print(f"Carton Dimensions (L x W x H): {results['best_carton']}")
            print(f"Units Per Carton: {results['max_units_carton']}")
            print(f"Carton Weight: {results['best_carton_weight']:.2f} lbs")
            print(f"Packing Configuration (L x W x H): {results['packing_config']}")

            print("\nBest Master Carton Size (cm):")
            print(f"Carton Dimensions (L x W x H): {tuple(round(dim, 2) for dim in best_carton_cm)}")
            print(f"Carton Weight: {best_carton_weight_kg:.2f} kg")

            # Plot 2D visualization
            plot_carton_2d(
                results["best_carton"],
                results["packing_config"],
                (product_length, product_width, product_height),
                "2D Visualization - Best Carton"
            )
        else:
            print("No valid carton configuration found.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()